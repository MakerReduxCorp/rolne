# rolne\__init__.py
#
# rolne datatype class: Recursive Ordered List of Named Elements
#
# Version 0.1.12
    
import copy

TNAME = 0
TVALUE = 1
TLIST = 2
TSEQ = 3
NS = 101

'''
Internal Notes:

    self.data is the actual place where the rolne data is stored.
    It is a list of tuples, where each tuple is:
    
          (name, value, list, seq)
          
    where:
    
        name is a string; part of the name/value pair being stored
        value is a string; part of the name/value pair being stored
        list is any subtending data under the name/value pair. Essentially
            is is another list of tuples.
        seq is a tracking string for historic and diagnostic data

    There are 4 globals in the doc: TNAME, TVALUE, TLIST, TSEQ to make the
    numeric index of each of these tuple elements easier to read.
        
'''

class rolne(object):

    def __init__(self, in_list=None):
        if in_list is None:
            self.data = []
        else:
            self.data = in_list

    def __str__(self, detail=False):
        result = ""
        if detail:
            result += "<rolne datatype object:\n"
        else:
            result += "%rolne:\n"
        result += self.mards(detail=detail)
        if detail:
            result += ">"
        return result

    def _explicit(self):
        return self.__str__(detail=True)


    def __len__(self):
        return len(self.data)
        
    def __getitem__(self, tup):
        if isinstance(tup, slice):
            (start_name, start_value, start_index) = (None, None, 0)
            if tup.start:
                if len(tup.start)>0:
                    start_name = tup.start[0]
                if len(tup.start)>1:
                    start_value = tup.start[1]
                if len(tup.start)>2:
                    start_index = tup.start[2]
            (stop_name, stop_value, stop_index) = (None, None, 0)
            if tup.stop:
                if len(tup.stop)>0:
                    stop_name = tup.stop[0]
                if len(tup.stop)>1:
                    stop_value = tup.stop[1]
                if len(tup.stop)>2:
                    stop_index = tup.stop[2]
            if tup.step:
                if tup.step==0:
                    raise KeyError, "Step cannot be zero"
                step = int(tup.step)
            else:
                step = 1
            #
            if tup.start:
                start_flag = False
            else:
                start_flag = True
            start_ctr = 0
            step_ctr = 0
            new_list = []
            for entry in self.data:
                if start_flag:
                    if tup.stop and stop_name==entry[TNAME] and stop_value==entry[TVALUE]:
                        break
                    if (step_ctr % step)==0:
                        new_list.append(entry)
                    step_ctr += 1
                else:
                    if start_name==entry[TNAME] and start_value==entry[TVALUE]:
                        if start_ctr==start_index:
                            start_flag = True
                            new_list.append(entry)
                            step_ctr += 1
                        else:
                            start_ctr += 1
            else:
                if start_flag:
                    if tup.stop:
                        raise KeyError, repr(tup.stop)+" not found"
                else:
                    raise KeyError, repr(tup.start)+" not found"
            return rolne(new_list)
        else:
            if not isinstance(tup, tuple):
                tup = (tup, None)
            (name, value, index) = (None, None, 0)
            if len(tup)>0:
                name = tup[0]
            if len(tup)>1:
                value = tup[1]
            if len(tup)>2:
                index = tup[2]
            start_ctr = 0
            if index<0:
                search_data = reversed(list(enumerate(self.data)))
                index = -index - 1
            else:
                search_data = enumerate(self.data)
            for i, entry in search_data:
                if entry[TNAME]==name:
                    if entry[TVALUE]==value:
                        if start_ctr==index:
                            return(rolne(self.data[i][TLIST]))
                        else:
                            start_ctr += 1
        raise KeyError, repr(tup)+" not found"
        return None

    def __setitem__(self, tup, value):
        if not isinstance(tup, tuple):
            tup = tuple([tup])
        arglen = len(tup)
        (name, cur_value, index) = (None, None, 0)
        index_flag = False
        if arglen==1:
            name = tup[TNAME]
        elif arglen==2:
            name = tup[TNAME]
            cur_value = tup[TVALUE]
        elif arglen==3:
            name = tup[TNAME]
            cur_value = tup[TVALUE]
            index = tup[2]
        elif arglen==0:
            raise KeyError, repr(tup)+" is empty"
        else:
            raise KeyError, repr(tup)+" has too many items"
        start_ctr = 0
        for i,(entry_name, entry_value, entry_list, entry_seq) in enumerate(self.data):
            if entry_name==name:
                if entry_value==cur_value or arglen==1:
                    if start_ctr==index:
                        new_tuple = (entry_name, value, entry_list, entry_seq)
                        self.data[i] = new_tuple
                        return True
                    else:
                        start_ctr += 1
        if arglen==3:
            raise KeyError, repr(tup)+" not found"
        else:
            self.append(name, value)
        return True

    def __delitem__(self, tup):
        if not isinstance(tup, tuple):
            tup = tuple([tup])
        arglen = len(tup)
        (name, value, index) = (None, None, 0)
        index_flag = False
        if arglen==1:
            name = tup[TNAME]
        elif arglen==2:
            name = tup[TNAME]
            value = tup[TVALUE]
        elif arglen==3:
            name = tup[TNAME]
            value = tup[TVALUE]
            index = tup[2]
        elif arglen==0:
            raise KeyError, repr(tup)+" is empty"
        else:
            raise KeyError, repr(tup)+" has too many items"
        start_ctr = 0
        for i,(entry_name, entry_value, entry_list, entry_seq) in enumerate(self.data):
            if entry_name==name:
                if entry_value==value or arglen==1:
                    if start_ctr==index:
                        del self.data[i]
                        return
                    else:
                        start_ctr += 1
        raise KeyError, repr(tup)+" not found"


    def __contains__(self, target):
        target_value_missing = True
        target_name = target
        target_index = 0
        if isinstance(target, tuple):
            if len(target)>0:
                target_name = target[0]
            if len(target)>1:
                target_value = target[1]
                target_value_missing = False
            if len(target)>2:
                target_index = target[2]
        ctr = 0
        for i,(entry_name, entry_value, entry_list) in enumerate(self.data):
                if (entry_name==target_name):
                    if target_value_missing:
                        return True
                    else:
                        if entry_value==target_value:
                            if ctr==target_index:
                                return True
                            else:
                                ctr += 1
        return False

    def __iter__(self):
        for entry in self.data:
            x = rolne([entry])
            yield x

    def _seq(self, seq=None):
        global NS
        if seq:
            result = str(seq)
        else:
            result = str(NS)
            NS += 1
        return result

    def find(self, *argv):
        """Locate a single rolne entry.

        This function is very similar to simply doing a dictionary-style
        lookup. For example:

            new_rolne = my_var.find("test", "zoom", 4)

        is effectively the same as:

            new_rolne = my_var["test", "zoom", 4]

        The biggest difference is that if entry at ["test", "zoom", 4] does
        not exist, the dictionary-style lookup generates a key error. Whereas
        this method simply returns None.

        Example of use:

        >>> # setup an example rolne first
        >>> my_var = rolne()
        >>> my_var.append("item", "zing")
        >>> my_var["item", "zing"].append("size", "4")
        >>> my_var["item", "zing"].append("color", "red")
        >>> my_var["item", "zing"]["color", "red"].append("intensity", "44%")
        >>> my_var["item", "zing"].append("reverse", None)
        >>> my_var.append("item", "broom")
        >>> my_var["item", "broom", -1].append("size", "1")
        >>> my_var["item", "broom", -1].append("title", 'The "big" thing')
        >>> my_var.append("item", "broom")
        >>> my_var["item", "broom", -1].append("size", "2")
        >>> my_var["item", "broom", -1].append("title", 'Other thing')
        >>> my_var.append("code_seq")
        >>> my_var["code_seq", None].append("*", "r9")
        >>> my_var["code_seq", None].append("*", "r3")
        >>> my_var["code_seq", None].append("*", "r2")
        >>> my_var["code_seq", None].append("*", "r3")
        >>> my_var.append("system_title", "hello")
        >>> #
        >>> print my_var.find("item","broom",1)
        %rolne:
        size 2
        title Other thing
        <BLANKLINE>
        >>> print my_var.find("item","broom",2)
        None
        >>> print my_var["code_seq", None].find("*","r3")
        %rolne:
        %empty
        <BLANKLINE>

        .. versionadded:: 0.1.2
        
        :param name:
           The key name of the name/value pair.
        :param value:
           The key value of the name/value pair. If not passed, then the value
           is assumed to be empty (None).
        :param index:
           The index of the name/value pair. if not passed, then the index is
           assumed to be 0.
        :returns:
           Returns either a rolne that points to the located entry or None if
           that entry is not found.
        """
        try:
            return self.__getitem__(argv)
        except KeyError:
            return None
        return None

    def mards(self, detail=False):
        result = ""
        # return repr(self.data)
        if self.data:
            for entry in self.data:
                if detail==True:
                    result += "[{}] ".format(str(entry[TSEQ]))
                result += str(entry[TNAME])
                if entry[TVALUE] is not None:
                    printable = str(entry[TVALUE])
                    quote_flag = False
                    if '"' in printable:
                        quote_flag = True
                    if len(printable) != len(printable.strip()):
                        quote_flag = True
                    if quote_flag:
                        result += " "+'"'+str(entry[TVALUE])+'"'
                    else:
                        result += " "+str(entry[TVALUE])
                result += "\n"
                if entry[TLIST]:
                    temp = rolne(entry[TLIST]).mards(detail=detail)
                    for line in temp.split("\n"):
                        if line:
                            result += "    "+line
                            result += "\n"
        else:
            result = "%empty\n"
        return result

    def append(self, name, value=None, sublist=None, seq=None):
        """Add one name/value entry to the main context of the rolne.

        Example of use:

        >>> # setup an example rolne first
        >>> my_var = rolne()
        >>> my_var.append("item", "zing")
        >>> my_var["item", "zing", -1].append("size", "4")
        >>> my_var["item", "zing", -1].append("color", "red")
        >>> print my_var
        %rolne:
        item zing
            size 4
            color red
        <BLANKLINE>
        >>> my_var.append("item", "zing")
        >>> my_var["item", "zing", -1].append("size", "2")
        >>> my_var["item", "zing", -1].append("color", "blue")
        >>> print my_var
        %rolne:
        item zing
            size 4
            color red
        item zing
            size 2
            color blue
        <BLANKLINE>

        .. versionadded:: 0.1.1
        
        :param name:
           The key name of the name/value pair.
        :param value:
           The key value of the name/value pair. If not passed, then the value
           is assumed to be None.
        :param sublist:
           An optional parameter that also appends a subtending list of entries.
           It is not recommended that this parameter be used.
        """
        if sublist is None:
            sublist = []
        new_tuple = (name, value, sublist, self._seq(seq))
        self.data.append(new_tuple)

    def append_index(self, name, value=None, sublist=None, seq=None):
        """Add one name/value entry to the main context of the rolne and
        return the index number for the new entry.

        Example of use:

        >>> # setup an example rolne first
        >>> my_var = rolne()
        >>> index = my_var.append_index("item", "zing")
        >>> print index
        0
        >>> my_var["item", "zing", index].append("size", "4")
        >>> my_var["item", "zing", index].append("color", "red")
        >>> print my_var
        %rolne:
        item zing
            size 4
            color red
        <BLANKLINE>
        >>> index = my_var.append_index("item", "zing")
        >>> print index
        1
        >>> my_var["item", "zing", index].append("size", "2")
        >>> my_var["item", "zing", index].append("color", "blue")
        >>> print my_var
        %rolne:
        item zing
            size 4
            color red
        item zing
            size 2
            color blue
        <BLANKLINE>

        .. versionadded:: 0.1.4
        
        :param name:
           The key name of the name/value pair.
        :param value:
           The key value of the name/value pair. If not passed, then the value
           is assumed to be None.
        :param sublist:
           An optional parameter that also appends a subtending list of entries.
           It is not recommended that this parameter be used.
        :returns:
           An integer representing the index of the newly inserted name/pair.
        """
        if sublist is None:
            sublist = []
        new_tuple = (name, value, sublist, self._seq(seq))
        self.data.append(new_tuple)
        index = len(self.get_list(name, value)) - 1
        return index

    def upsert(self, name, value=None, seq=None):
        """Add one name/value entry to the main context of the rolne, but
        only if an entry with that name does not already exist.

        If the an entry with name exists, then the first entry found has it's
        value changed.

        NOTE: the upsert only updates the FIRST entry with the name found.

        The method returns True if an insertion occurs, otherwise False.

        Example of use:

        >>> # setup an example rolne first
        >>> my_var = rolne()
        >>> my_var.upsert("item", "zing")
        True
        >>> my_var["item", "zing"].append("color", "blue")
        >>> print my_var
        %rolne:
        item zing
            color blue
        <BLANKLINE>
        >>> my_var.upsert("item", "zing")
        False
        >>> print my_var
        %rolne:
        item zing
            color blue
        <BLANKLINE>
        >>> my_var.upsert("item", "broom")
        False
        >>> print my_var
        %rolne:
        item broom
            color blue
        <BLANKLINE>

        .. versionadded:: 0.1.1
        
        :param name:
           The key name of the name/value pair.
        :param value:
           The key value of the name/value pair. If not passed, then the value
           is assumed to be None.
        :returns:
           Returns True if the name/value was newly inserted. Otherwise, it
           returns False indicated that an update was done instead.
        """
        for ctr, entry in enumerate(self.data):
            if entry[TNAME]==name:
                new_tuple = (name, value, entry[TLIST], entry[TSEQ])
                self.data[ctr]=new_tuple
                return False
        new_tuple = (name, value, [], self._seq(seq))
        self.data.append(new_tuple)
        return True

    def get_list(self, *args):
        arg_count = len(args)
        result = []
        ctr = 0
        for entry in self.data:
            if arg_count==0:
                result.append(entry[TVALUE])
            if arg_count==1:
                if entry[TNAME]==args[0]:
                    result.append(entry[TVALUE])
            if arg_count==2:
                if entry[TNAME]==args[0] and entry[TVALUE]==args[1]:
                    result.append(entry[TVALUE])
            if arg_count==3:
                if entry[TNAME]==args[0] and entry[TVALUE]==args[1]:
                    if ctr==args[2]:
                        result.append(entry[TVALUE])
                    ctr += 1
        return result

    def get_names(self):
        result = []
        for entry in self.data:
            result.append(entry[TNAME])
        return result

    def get_tuples(self, *args):
        arg_count = len(args)
        result = []
        ctr = 0
        for entry in self.data:
            if arg_count==0:
                result.append((entry[TNAME], entry[TVALUE]))
            if arg_count==1:
                if entry[TNAME]==args[0]:
                    result.append((entry[TNAME], entry[TVALUE]))
            if arg_count==2:
                if entry[TNAME]==args[0] and entry[TVALUE]==args[1]:
                    result.append((entry[TNAME], entry[TVALUE]))
            if arg_count==3:
                if entry[TNAME]==args[0] and entry[TVALUE]==args[1]:
                    if ctr==args[2]:
                        result.append((entry[TNAME], entry[TVALUE]))
                    ctr += 1
        return result

    def keys(self, *args):
        return self.dump_list(args, name=True, value=True, index=True)

    def dump_list(self, args, name=False, value=True, index=False, seq=False):
        if not isinstance(args, tuple):
            args = tuple([args])
        arg_count = len(args)
        result = []
        ctr = {}
        for entry in self.data:
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
        return result

        
    def flattened_list(self, args, name=False, value=True, index=False, seq=False):
        if not isinstance(args, tuple):
            args = tuple([args])
        return self._flattened_list(self.data, args, name=name, value=value, index=index, seq=seq)

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
                result.extend(self._flattened_list( entry[TLIST], args, name, value, index, seq) )
        return result
        
    def dump(self):
        return self._dump(self.data)

    def _dump(self, data):
        result = []
        for entry in data:
            tup = (entry[TNAME], entry[TVALUE], self._dump(entry[TLIST]))
            result.append(tup)
        return result
        
    def value(self, name):
        for (en, ev, el, es) in self.data:
            if en==name:
                return ev
        return None

    def seq(self, name, value, index=None):
        if index is None:
            index=0
        ctr = 0
        for (en, ev, el, es) in self.data:
            if en==name and ev==value:
                if ctr==index:
                    return es
                ctr += 1
        return None

    def summarize(self, name, *args):
        # we are using *args for 'value' because None is a valid value parameter that
        # must be distinquished from a _missing_ parameter.
        if args:
            value = args[0]
            value_missing = False
        else:
            value = None
            value_missing = True
        value_list = []
        summary = []
        for (en, ev, el, es) in self.data:
            if en==name:
                if value_missing or ev==value:
                    value_list.append(ev)
                    summary.append((en, ev, el, es))
        return (name, value_list, rolne(in_list = summary))

    def filter(self, *argv):
        return self.summarize(*argv)[2]

    def at_seq(self, seq=None):
        # return the rolne located with the seq
        tup = self.ptr_to_seq(seq)
        if tup is None:
            return None
        return rolne(in_list=tup[TLIST])
        
    def ptr_to_seq(self, seq):
        # this is an interesting one: return a reference to
        # the direct tuple with this sequence. Use with care.
        (target_list, target_index) = self.list_ref_to_seq(seq)
        if target_list is None:
            return None
        return target_list[target_index]

    def list_ref_to_seq(self, seq):
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
        return self._list_ref_to_seq(self.data, seq)

    def _list_ref_to_seq(self, data, seq):
        result = (None, None)
        for index, entry in enumerate(data):
            (en, ev, el, es) = entry
            if es==seq:
               return (data, index)
            if el:
                result = self._list_ref_to_seq(el, seq)
                if result[0] is not None:
                    return result
        return (None, None)

    def seq_replace(self, seq, src_seq, prefix="rep"):
        # locating the entry with 'seq', replace the contents
        # of seq with a COPY of the entry seen at src_seq.
        # the original entry retains it's seq string, but the
        # name, value, and subtending list all change.
        # the subtending entries get new seq ids
        # returns True is successful, else False
        dest_ref = self.list_ref_to_seq(seq)
        if dest_ref[0] is None:
            return False
        (dest_list, dest_index) = dest_ref
        ro_dest_tup = dest_list[dest_index]
        src_tup = self.ptr_to_seq(src_seq)
        if src_tup is None:
            return False
        new_sub_list = self._copy_sublist_with_new_seq(src_tup[TLIST], prefix)
        new_tup = (copy.deepcopy(src_tup[TNAME]), copy.deepcopy(src_tup[TVALUE]), new_sub_list, ro_dest_tup[TSEQ])
        dest_list[dest_index] = new_tup
        return True

    def _copy_sublist_with_new_seq(self, source, prefix):
        dest = []
        for (ev, en, el, es) in source:
            new_seq = prefix+self._seq() # called before next to make seq look logical
            new_list = self._copy_sublist_with_new_seq(el, prefix)
            new_tup = (copy.copy(ev), copy.copy(en), new_list, new_seq)
            dest.append(new_tup)
        return dest

    def seq_lineage(self, seq):
        # return a parental list of seq that are represented by a seq
        # TODO add a param to return keys rather than seq
        return self._seq_lineage(self.data, seq)

    def _seq_lineage(self, data, seq):
        for index, entry in enumerate(data):
            (en, ev, el, es) = entry
            if es==seq:
               return [es]
            if el:
                result = self._seq_lineage(el, seq)
                if result:
                    return [es]+result
        return []
        
    def seq_parent(self, seq):
        # seq of immediate parent
        the_line = self.seq_lineage(seq)
        if len(the_line)>1:
            return the_line[-2]
        return None

    def seq_progenitor(self, seq):
        # seq of top ancestor
        the_line = self.seq_lineage(seq)
        if the_line:
            return the_line[0]
        return None

    def seq_delete(self, seq):
        # delete the entry pointed to by the sequence
        ref = self.list_ref_to_seq(seq)
        if ref[0] is None:
            return None
        (rl, ri) = ref
        del rl[ri]
        return seq

    def copy(self, seq_prefix="copy_", seq_suffix=""):
        seq_prefix = str(seq_prefix)
        seq_suffix = str(seq_suffix)
        return rolne(in_list=self._copy(seq_prefix, seq_suffix, self.data))

    def _copy(self, seq_prefix, seq_suffix, data):
        new_list = []
        for (ev, en, el, es) in data:
            sub = self._copy(seq_prefix, seq_suffix, el)
            new_list.append((copy.copy(ev), copy.copy(en), sub, seq_prefix+es+seq_suffix))
        return new_list
        
if __name__ == "__main__":

    if True:

        my_var = rolne()
        my_var.append("item", "zing")
        my_var["item", "zing"].upsert("size", "4")
        my_var["item", "zing"].upsert("color", "red")
        my_var["item", "zing"]["color", "red"].upsert("intensity", "44%")
        my_var["item", "zing"].upsert("color", "yellow")
        my_var.append("item", "womp")
        my_var["item", "womp"].upsert("size", "5")
        my_var["item", "womp"].upsert("color", "blue")
        my_var.append("item", "bam")
        my_var.append("item", "broom")
        my_var["item", "broom", -1].upsert("size", "1")
        my_var["item", "broom", -1].upsert("title", 'The "big" thing')
        my_var.append("item", "broom")
        my_var["item", "broom", -1].upsert("size", "2")
        my_var["item", "broom", -1].upsert("title", 'The "big" thing')
        my_var.append("item", "broom")
        my_var["item", "broom", -1].upsert("size", "3")
        my_var["item", "broom", -1].upsert("title", 'The "big" thing')
        my_var.upsert("zoom_flag")
        my_var.upsert("code_seq", seq="ln1")
        my_var["code_seq", None].append("*", "r9", seq="ln2")
        my_var["code_seq", None].append("*", "r3")
        my_var["code_seq", None].append("*", "r2")
        my_var["code_seq", None].append("*", "r3")
        my_var.upsert("system_title", "hello")

        print "a", my_var._explicit()
        #print "aa", my_var["zoom_flag"]
        c_var = my_var.copy(seq_prefix="a", seq_suffix=None)
        #print "b", my_var["code_seq"]
        #print "bb", my_var.find("code_seq")
        #print "c1", my_var.dump_list( ( ), name=True, value=True, index=True, seq=True)
        #print "cz", my_var.flattened_list( ("title"), name=True, value=True, index=True, seq=True)
        #print "c2", my_var.get( ("item"), name=True, value=True, index=True, seq=True)
        #print "c3", my_var.get( ("item", "broom"), name=True, value=True, index=True, seq=True)
        #print "c4", my_var.get( ("item", "broom", 2), name=True, value=True, index=True, seq=True)
        #print "c5", my_var.get( ("item", "broom", 9), name=True, value=True, index=True, seq=True)
        #print "c6", my_var.keys("item", "broom")
        #my_var["code_seq"]["*", None] = 'zings'
        #print "d", my_var._explicit()
        #print "e", my_var["item", "zing"].value("size")
        #print "f", my_var
        #print "g", my_var["item", "broom", -1]
        seq = "120"
        #new_var = my_var.at_seq(seq)
        #if new_var is not None:
        #    print "h2", new_var._explicit()
        #else:
        #    print "h2", None
        #new_tup = my_var.ptr_to_seq(seq)
        #print "h3", new_tup
        #new_ptr = my_var.list_ref_to_seq(seq)
        #print "h4", new_ptr
        #print "h5",my_var.replace_using_seq(seq, "ln1", "xx")
        print "k1 line",my_var.seq_lineage(seq)
        print "k2 prnt",my_var.seq_parent(seq)
        print "k3 prog",my_var.seq_progenitor(seq)
        print "k4  del",my_var.seq_delete(seq)
        #print my_var.append_index("item", "broom")

        print "z",my_var._explicit()
        print "z1", c_var._explicit()
        #print "z2",my_var.dump()

        #TODO: add '.del_decendants()'
        #TODO: add '.del_ancestral_branch()'
        #TODO: add '.change_name()'

    else:
        print "==================================="
        print
        import doctest
        print "Testing begins. Errors found:"
        print doctest.run_docstring_examples(rolne.find, None)
        print doctest.run_docstring_examples(rolne.append, None)
        print doctest.run_docstring_examples(rolne.append_index, None)
        print doctest.run_docstring_examples(rolne.upsert, None)
        
