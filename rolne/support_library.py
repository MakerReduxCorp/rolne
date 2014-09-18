# rolne\support_library.py
#
# SUPPORT LIBRARY FOR ROLNE
#
    
import copy
from rolne import rolne

TNAME = 0
TVALUE = 1
TLIST = 2
TSEQ = 3

NS = 101

def _seq(self, seq=None):
    global NS
    if seq:
        result = str(seq)
    else:
        result = str(NS)
        NS += 1
    return result

def mards(self, detail=False):
    # this is NOT, of course, a _real_ MARDS representation.
    # for example, it is possible for a 'rolne' name to be a string with spaces.
    #  but that is not possible in MARDS. Here, we simply put quotes around the name.
    #  Plus, MARDS only does strings. A rolne can do anything.
    #  Here, we add a equals sign to non-None scenarios.
    return _mards(self.data, detail)
    
def _mards(data, detail):
    result = ""
    # return repr(self.data)
    if data:
        for entry in data:
            if detail==True:
                result += "[{}] ".format(str(entry[TSEQ]))
            result += poss_quotes(entry[TNAME])
            if entry[TVALUE] is None:
                result += " is None"
            else:
                result += " = "+poss_quotes(entry[TVALUE])
            result += "\n"
            if entry[TLIST]:
                temp = _mards(entry[TLIST], detail)
                for line in temp.split("\n"):
                    if line:
                        result += "    "+line
                        result += "\n"
    else:
        result = "%empty\n"
    return result

def poss_quotes(value):
    printable = str(value)
    quote_flag = False
    if len(printable)==0:
        quote_flag = True
    if '"' in printable:
        quote_flag = True
    if ' ' in printable:
        quote_flag = True
    if '=' in printable:
        quote_flag = True
    if len(printable) != len(printable.strip()):
        quote_flag = True
    if quote_flag:
        return '"'+printable+'"'
    return printable

def _extend(self, sublist, prefix):
    new_list = []
    for entry in sublist:
        (en, ev, el, es) = entry
        sub_list = _extend(self, el, prefix)
        tup = (en, ev, sub_list, prefix+_seq(self))
        new_list.append(tup)
    return new_list
        

def _flattened_list(self, data, args, name, value, index, seq):
    arg_count = len(args)
    result = []
    ctr = {}
    for entry in data:
        # the counter function
        if (entry[TNAME], entry[TVALUE]) in ctr:
            ctr[(entry[TNAME], entry[TVALUE])] += 1
        else:
            ctr[(entry[TNAME], entry[TVALUE])] = 0
        # make the tuple
        items = []
        if name:
            items.append(entry[TNAME])
        if value:
            items.append(entry[TVALUE])
        if index:
            items.append(ctr[(entry[TNAME], entry[TVALUE])])
        if seq:
            items.append(entry[TSEQ])
        tup = tuple(items)
        # insert as dictated by args given
        if arg_count==0:
            result.append(tup)
        if arg_count==1:
            if entry[TNAME]==args[0]:
                result.append(tup)
        if arg_count==2:
            if entry[TNAME]==args[0] and entry[TVALUE]==args[1]:
                result.append(tup)
        if arg_count==3:
            if entry[TNAME]==args[0] and entry[TVALUE]==args[1]:
                if ctr[(entry[TNAME], entry[TVALUE])]==args[2]:
                    result.append(tup)
        if entry[TLIST]:
            result.extend(_flattened_list(self, entry[TLIST], args, name, value, index, seq) )
    return result
    
def _dump(self, data):
    result = []
    for entry in data:
        tup = (entry[TNAME], entry[TVALUE], _dump(self, entry[TLIST]))
        result.append(tup)
    return result

# an internal routine to get self or an element based on flexible args
# returns (name, value, index, seq, list)
def ref_super_tuple(self, *args):
    arglen = len(args)
    (name, value, index) = (None, None, 0)
    if arglen>0:
        name = args[0]
    if arglen>1:
        value = args[1]
    if arglen>2:
        index = args[2]
    ctr = 0
    if arglen==0:
        super_tup = super_tuple_search_seq(self.ref_seq, self.ancestor)
        return super_tup
    else:
        for entry in self.data:
            (en, ev, el, es) = entry
            if en==name:
                if arglen==1:
                    return (en, ev, ctr, es, el)
                elif ev==value:
                    if ctr==index:
                        return (en, ev, ctr, es, el)
                    ctr += 1
    return (None, None, None, None, None)


def super_tuple_search_seq(seq, data):
    ctr = 0
    for entry in data:
        (en, ev, el, es) = entry
        if es==seq:
            target_name = en
            target_value = ev
            for (tn, tv, _, ts) in data:
                if target_name==tn and target_value==tv:
                    if ts==seq:
                        break
                    ctr += 1
            return (en, ev, ctr, es, el)
        if el:
            result = super_tuple_search_seq(seq, el)
            if result:
                return result
    return None


# an internal routine to get data index based on flexible args
#   -1 = self
#   None = not found
#   else returns index number
def _ref_index(self, *args):
    arglen = len(args)
    (name, value, index) = (None, None, 0)
    if arglen>0:
        name = args[0]
    if arglen>1:
        value = args[1]
    if arglen>2:
        index = args[2]
    ctr = 0
    if arglen==0:
        return -1
    else:
        for i, entry in enumerate(self.data):
            (en, ev, el, es) = entry
            if en==name:
                if arglen==1 or ev==value:
                    if ctr==index:
                        return i
                    ctr += 1
    return None

# this routine creates a 'temporary' rolne that points to the
# 'top-level' rolne list.
# Any changes to self.ref_seq, ref_name, or ref_value are bogus
# and are lost when the rolne is garbage collected. But changes
# to children in TLIST survive.
# TODO: delete this function; I strongly suspect that it is an unneeded later
def _point_ancestry(self):
    return rolne(in_tuple=(None, None, self.ancestor, None))
    
def ptr_to_seq(self, seq):
    # this is an interesting one: return a reference to
    # the direct tuple with this sequence. Use with care.
    (target_list, target_index) = list_ref_to_seq(self.ancestor, seq)
    if target_list is None:
        return None
    return target_list[target_index]

def _seq_lineage(data, seq):
    for index, entry in enumerate(data):
        (en, ev, el, es) = entry
        if es==seq:
           return [es]
        if el:
            result = _seq_lineage(el, seq)
            if result:
                return [es]+result
    return []
        

def list_ref_to_seq(orig_data, seq):
    # this one REALLY jumps down the rabbit hole.
    #
    # returns a tuple containing the original list containing the
    # sequence and the index pointing to the entry that
    # has the sequence.
    #
    # (list, index)
    #
    # this is useful for for routines that, in turn, modify
    # an entry. One cannot "change" a tuple. So a pointer
    # to a tuple has no value. This combo allows true change
    # because lists are mutable.
    #
    return _list_ref_to_seq(orig_data, seq)

def _list_ref_to_seq(data, seq):
    result = (None, None)
    for index, entry in enumerate(data):
        (en, ev, el, es) = entry
        if es==seq:
           return (data, index)
        if el:
            result = _list_ref_to_seq(el, seq)
            if result[0] is not None:
                return result
    return (None, None)

def _copy_sublist_with_new_seq(self, source, prefix):
    dest = []
    for (ev, en, el, es) in source:
        new_seq = prefix+_seq(self) # called before next to make seq look logical
        new_list = _copy_sublist_with_new_seq(self, el, prefix)
        new_tup = (copy.copy(ev), copy.copy(en), new_list, new_seq)
        dest.append(new_tup)
    return dest

def _copy(self, seq_prefix, seq_suffix, data):
    new_list = []
    for (ev, en, el, es) in data:
        sub = _copy(self, seq_prefix, seq_suffix, el)
        new_list.append((copy.copy(ev), copy.copy(en), sub, seq_prefix+es+seq_suffix))
    return new_list
