# rolne\__init__.py
#
# rolne datatype class: Recursive Ordered List of Named Elements
#
# Version 0.1.16
    
import copy
<<<<<<< HEAD
import xml
=======
import support_library as lib
>>>>>>> feature/properties

TNAME = 0
TVALUE = 1
TLIST = 2
TSEQ = 3

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

    #############################
    #
    #   STANDARD CLASS METHODS
    #
    #############################

    def __init__(self, in_list=None, in_tuple=None, ancestor=None):
        self.ref_name = None
        self.ref_value = None
        self.ref_seq = None
        if in_list is None:
            if in_tuple is None:
                self.data = []
            else:
                (self.ref_name, self.ref_value, self.data, self.ref_seq) = in_tuple
        else:
            self.data = in_list
        if ancestor is None:
            self.ancestor = self.data
        else:
            self.ancestor = ancestor

    def __str__(self, detail=False):
        result = ""
        if detail:
            result += "<rolne datatype object:\n"
        else:
            result += "%rolne:\n"
        result += lib.mards(self, detail=detail)
        if detail:
            result += ">"
        return result

    def _explicit(self):
        return self.__str__(detail=True)

    def __len__(self):
        return len(self.data)
        
    def __getitem__(self, tup):
        if isinstance(tup, slice):
            ###################
            # handle a 'slice'
            ###################
            (start_name, start_value, start_index) = (None, None, 0)
            startlen = 0
            if tup.start:
                if not isinstance(tup.start, tuple):
                    tup_start = (tup.start,)
                else:
                    tup_start = tup.start
                startlen = len(tup_start)
                if startlen>0:
                    start_name = tup_start[0]
                if startlen>1:
                    start_value = tup_start[1]
                if startlen>2:
                    start_index = tup_start[2]
            (stop_name, stop_value, stop_index) = (None, None, 0)
            stoplen = 0
            if tup.stop:
                if not isinstance(tup.stop, tuple):
                    tup_stop = (tup.stop,)
                else:
                    tup_stop = tup.stop
                stoplen = len(tup_stop)
                if stoplen>0:
                    stop_name = tup_stop[0]
                if stoplen>1:
                    stop_value = tup_stop[1]
                if stoplen>2:
                    stop_index = tup_stop[2]
            if tup.step:
                if tup.step<1:
                    raise KeyError, "Step cannot be less than 1"
                step = int(tup.step)
            else:
                step = 1
            #
            if tup.start:
                start_flag = False
            else:
                start_flag = True
            start_ctr = 0
            stop_ctr = 0
            step_ctr = 0
            new_list = []
            for entry in self.data:
                if start_flag:
                    if stoplen==1 and stop_name==entry[TNAME]:
                        break
                    if stoplen==2 and stop_name==entry[TNAME] and stop_value==entry[TVALUE]:
                        break
                    if stoplen==3 and stop_name==entry[TNAME] and stop_value==entry[TVALUE] and stop_index==stop_ctr:
                        break
                    if (step_ctr % step)==0:
                        new_list.append(entry)
                    step_ctr += 1
                else:
                    if startlen==1 and start_name==entry[TNAME]:
                        start_flag = True
                        new_list.append(entry)
                        step_ctr += 1
                    if startlen==2 and start_name==entry[TNAME] and start_value==entry[TVALUE]:
                        start_flag = True
                        new_list.append(entry)
                        step_ctr += 1
                    if startlen==3 and start_name==entry[TNAME] and start_value==entry[TVALUE] and start_index==start_ctr:
                        start_flag = True
                        new_list.append(entry)
                        step_ctr += 1
                # do the counters seperately
                if startlen==3 and start_name==entry[TNAME] and start_value==entry[TVALUE]:
                    start_ctr += 1
                if stoplen==3 and stop_name==entry[TNAME] and stop_value==entry[TVALUE]:
                    stop_ctr += 1
            else:
                if start_flag:
                    if tup.stop:
                        raise KeyError, repr(tup.stop)+" not found"
                else:
                    raise KeyError, repr(tup.start)+" not found"
            return rolne(in_tuple = (self.ref_name, self.ref_value, new_list, self.ref_seq), ancestor=self.ancestor)
        else:
            ###################
            # handle a tuple (non-slice)
            ###################
            if not isinstance(tup, tuple):
                tup = (tup,)
            arglen = len(tup)
            (name, value, index) = (None, None, 0)
            if arglen>0:
                name = tup[0]
            if arglen>1:
                value = tup[1]
            if arglen>2:
                index = tup[2]
            start_ctr = 0
            if index<0:
                search_data = reversed(list(enumerate(self.data)))
                index = -index - 1
            else:
                search_data = enumerate(self.data)
            for i, entry in search_data:
                if entry[TNAME]==name:
                    if arglen==1 or entry[TVALUE]==value:
                        if start_ctr==index:
                            return rolne(in_tuple = self.data[i], ancestor=self.ancestor)
                        else:
                            start_ctr += 1
        raise KeyError, repr(tup)+" not found"
        return None

    def __setitem__(self, tup, value):
        if not isinstance(tup, tuple):
            tup = tuple([tup])
        if not self.press(*tup, value=value):
            if len(tup):
                self.append(tup[TNAME], value)
            else:
                raise KeyError, repr(tup)+" not found"
        return None

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
            x = rolne(in_tuple = entry, ancestor=self.ancestor)
            yield x


    #############################
    #
    # PROPERTY METHODS
    #
    #############################

    #-------------------
    #  PROPERTY: NAME
    #-------------------
    @property
    def name(self):
        return self.ref_name

    @name.setter
    def name(self, value):
        self.change(name=name)
        return None

    @name.deleter
    def name(self):
        raise KeyError, "It is not possible to delete just a name. If you want to delete an entry, try to delete the entry itself."
        return None

    #-------------------
    #  PROPERTY: VALUE
    #-------------------
    @property
    def value(self):
        return self.ref_value

    @value.setter
    def value(self, value):
        self.change(value=value)
        return None

    @value.deleter
    def value(self):
        if self.ref_seq is None:
            # you can't change the 'value' of SELF at the very
            # top of the tree. (doing so breaks a lot of stuff)
            # But, since a 'del' in this scenario sets it to None, there
            # is no error to throw.
            return None
        else:
            self.change(value=None)
        return None

    #-------------------
    #  PROPERTY: SEQ
    #-------------------
    @property
    def seq(self):
        return self.ref_seq

    @seq.setter
    def seq(self, seq):
        self.change(seq=seq)
        return None

    @seq.deleter
    def seq(self):
        raise KeyError, "It is not possible to delete a seq."
        return None


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


    def append(self, name, value=None, sublist=None, seq=None):
        """Add one name/value entry to the main context of the rolne.

        Unlike most 'append' methods, this one DOES return a value:
        the newly assigned seq string.

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
        new_seq = lib._seq(self, seq)
        new_tuple = (name, value, sublist, new_seq)
        self.data.append(new_tuple)
        return new_seq

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
        new_tuple = (name, value, sublist, lib._seq(self, seq))
        self.data.append(new_tuple)
        index = len(self.list_values(name, value)) - 1
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
        new_tuple = (name, value, [], lib._seq(self, seq))
        self.data.append(new_tuple)
        return True

    def extend(self, new_rolne, prefix=""):
        for child in new_rolne:
            new_list = []
            new_list = lib._extend(self, child.rlist(), prefix)
            tup = (child.name(), child.value(), new_list, prefix+lib._seq(self))
            self.data.append(tup)
        return

        
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
        return lib._flattened_list(self, self.data, args, name=name, value=value, index=index, seq=seq)

    def dump(self):
        return lib._dump(self, self.data)


    def copy(self, seq_prefix="copy_", seq_suffix=""):
        seq_prefix = str(seq_prefix)
        seq_suffix = str(seq_suffix)
        return rolne(in_tuple=(None, None, lib._copy(self, seq_prefix, seq_suffix, self.data), None))


    #
    #
    #   GET name/value/index/seq/key/tuple SECTION
    #
    #
        
    # if called as x.name(), it returns it's own name
    # if called as x.name(name,...), it returns the name of the first matching entry
    #    IF found (otherwise None)
    def get_name(self, *args):
        (name, _, _, _, _) = lib.ref_super_tuple(self, *args)
        return name
    
    # if called as x.value(), it returns it's own value
    # if called as x.value(name,...), it returns the value of the first matching entry
    #    found (otherwise None)
    def get_value(self, *args):
        (_, value, _, _, _) = lib.ref_super_tuple(self, *args)
        return value

    # if called as x.index(), it returns it's own value
    # if called as x.name(name,...), it returns the value of the first matching entry
    #    found (otherwise None)
    def get_index(self, *args):
        (_, _, index, _, _) = lib.ref_super_tuple(self, *args)
        return index

    # if called as x.seq(), it returns it's own sequence id
    # if called as x.seq(name, value, index), it returns the value of the first name entry
    #    found (otherwise None)
    def get_seq(self, *args):
        (_, _, _, seq, _) = lib.ref_super_tuple(self, *args)
        return seq

    def get_key(self, *args):
        (name, value, index, _, _) = lib.ref_super_tuple(self, *args)
        return (name, value, index)

    def get_tuple(self, *args):
        (name, value, index, seq, _) = lib.ref_super_tuple(self, *args)
        return (name, value, index, seq)

    #
    #
    # CHANGE (generic)
    #
    #
    def change(self, *args, **kwargs):
        if 'seq' in kwargs and kwargs['seq'] is None:
            raise KeyError, "It is not possible to set a seq to None."
        list_ptr = self.data
        index = lib._ref_index(self, *args)
        if index is None:
            raise KeyError, repr(args)+" not found"
        if index==-1:
            # set the name of the SELF
            # which, to make globally true, requires access
            # to ancestry
            if self.ref_seq is None:
                # you can't change the name of SELF at the very
                # top of the tree. (doing so breaks a lot of stuff)
                if 'name' in kwargs and kwargs['name'] is not None:
                    raise ValueError("The name, value, and seq of an ancestral root of a rolne can only be None.")
                if 'value' in kwargs and kwargs['value'] is not None:
                    raise ValueError("The name, value, and seq of an ancestral root of a rolne can only be None.")
                if 'seq' in kwargs and kwargs['seq'] is not None:
                    raise ValueError("The name, value, and seq of an ancestral root of a rolne can only be None.")
                return None
            else:
                (list_ptr, index) = lib.list_ref_to_seq(self.ancestor, self.ref_seq)
                if 'name' in kwargs: self.ref_name = kwargs['name']
                if 'value' in kwargs: self.ref_value = kwargs['value']
                if 'seq' in kwargs: self.ref_seq = kwargs['seq']
        (en, ev, el, es) = list_ptr[index]
        if 'name' in kwargs: en = kwargs['name']
        if 'value' in kwargs: ev = kwargs['value']
        if 'seq' in kwargs: es = kwargs['seq']
        list_ptr[index] = (en, ev, el, es)
        return None

    # 'press' and 'change' are almost identical. 'change' simply never generates
    # an exception. It is more of a 'if it's okay, then do it.'
    # returns True if change made, otherwise returns False
    def press(self, *args, **kwargs):
        if 'seq' in kwargs and kwargs['seq'] is None:
            return False
        list_ptr = self.data
        index = lib._ref_index(self, *args)
        if index is None:
            return False
        if index==-1:
            # set the name of the SELF
            # which, to make globally true, requires access
            # to ancestry
            if self.ref_seq is None:
                # you can't change the name of SELF at the very
                # top of the tree. (doing so breaks a lot of stuff)
                return False
            else:
                (list_ptr, index) = lib.list_ref_to_seq(self.ancestor, self.ref_seq)
                if 'name' in kwargs: self.ref_name = kwargs['name']
                if 'value' in kwargs: self.ref_value = kwargs['value']
                if 'seq' in kwargs: self.ref_seq = kwargs['seq']
        (en, ev, el, es) = list_ptr[index]
        if 'name' in kwargs: en = kwargs['name']
        if 'value' in kwargs: ev = kwargs['value']
        if 'seq' in kwargs: es = kwargs['seq']
        list_ptr[index] = (en, ev, el, es)
        return True

    #
    #
    #   GET/CHANGE PARENT SECTION
    #
    #

    def parent(self):
        the_line = self.seq_lineage(self.ref_seq)
        if len(the_line)==0:
            return None
        elif len(the_line)==1:
            # I am a progenitor, my "parent" is root; return myself
            return rolne(in_tuple=(None, None, self.ancestor, None), ancestor=self.ancestor)
        else:
            parent_seq = the_line[-2]
            return self.at_seq(parent_seq)
        
    def parent_name(self):
        (name, _, _, _) = parent_tuple(self)
        return name

    def parent_value(self):
        (_, value, _, _) = parent_tuple(self)
        return value

    def parent_index(self):
        (_, _, index, _) = parent_tuple(self)
        return index

    def parent_seq(self):
        (_, _, _, seq) = parent_tuple(self)
        return seq

    def parent_key(self):
        (name, value, index, _) = parent_tuple(self)
        return (name, value, index)

    def parent_tuple(self):
        my_parent = self.parent()
        if my_parent is None:
            return False
        else:
            return my_parent.get_tuple()

    #def parent_change(self, **kwargs):
    #    return None

    #
    #
    #   LIST name/value/index/seq SECTION
    #
    #

    #("Command 'get_list' deprecated. Use 'list_values'.")

    def list_values(self, *args):
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

    #("Command 'get_names' deprecated. Use 'list_names'.")
    
    def list_names(self, *args):
        arg_count = len(args)
        result = []
        ctr = 0
        for entry in self.data:
            if arg_count==0:
                result.append(entry[TNAME])
            if arg_count==1:
                if entry[TNAME]==args[0]:
                    result.append(entry[TNAME])
            if arg_count==2:
                if entry[TNAME]==args[0] and entry[TVALUE]==args[1]:
                    result.append(entry[TNAME])
            if arg_count==3:
                if entry[TNAME]==args[0] and entry[TVALUE]==args[1]:
                    if ctr==args[2]:
                        result.append(entry[TNAME])
                    ctr += 1
        return result

    def list_seq(self, *args):
        arg_count = len(args)
        result = []
        ctr = 0
        for entry in self.data:
            if arg_count==0:
                result.append(entry[TSEQ])
            if arg_count==1:
                if entry[TNAME]==args[0]:
                    result.append(entry[TSEQ])
            if arg_count==2:
                if entry[TNAME]==args[0] and entry[TVALUE]==args[1]:
                    result.append(entry[TSEQ])
            if arg_count==3:
                if entry[TNAME]==args[0] and entry[TVALUE]==args[1]:
                    if ctr==args[2]:
                        result.append(entry[TSEQ])
                    ctr += 1
        return result

    #
    #
    #   SEQUENCE ANCESTRY SUPPORT
    #
    #

    def at_seq(self, seq):
        # return the rolne located with the seq
        tup = lib.ptr_to_seq(self, seq)
        if tup is None:
            return None
        return rolne(in_tuple=tup, ancestor=self.ancestor)
        

    def seq_replace(self, seq, src, prefix="rep"):
        # locating the entry with 'seq', replace the contents
        # of seq with a COPY of the entry seen at src.
        # If src is a string, the it is a sequence id of the data
        #  in the same rolne.
        # if src is a tuple, then it is a tuple of the new actual data.
        # the original entry retains it's seq string, but the
        # name, value, and subtending list all change.
        # the subtending entries get new seq ids
        # returns True is successful, else False
        dest_ref = lib.list_ref_to_seq(self, seq)
        if dest_ref[0] is None:
            return False
        (dest_list, dest_index) = dest_ref
        ro_dest_tup = dest_list[dest_index]
        if type(src) is tuple:
            src_tup = src
        else:
            src_tup = lib.ptr_to_seq(self, src)
        if src_tup is None:
            return False
        new_sub_list = lib._copy_sublist_with_new_seq(self, src_tup[TLIST], prefix)
        new_tup = (copy.deepcopy(src_tup[TNAME]), copy.deepcopy(src_tup[TVALUE]), new_sub_list, ro_dest_tup[TSEQ])
        dest_list[dest_index] = new_tup
        return True


    def seq_lineage(self, seq):
        # return a parental list of seq that are represented by a seq
        # TODO add a param to return keys rather than seq
        return lib._seq_lineage(self.ancestor, seq)

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
        ref = lib.list_ref_to_seq(self.data, seq)
        if ref[0] is None:
            return None
        (rl, ri) = ref
        del rl[ri]
        return seq


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

        x_var = rolne()
        x_var.append("item", "zingo")
        x_var["item", "zingo"].upsert("size", "4b")
        x_var["item", "zingo"].upsert("color", "redb")
        x_var["item", "zingo"]["color", "redb"].upsert("intensity", "44%b")
        x_var["item", "zingo"].upsert("color", "yellowb")

<<<<<<< HEAD

        #print "a", my_var._explicit()
        #print "a2", x_var._explicit()
        #print "aa", my_var["zoom_flag"]
        #c_var = my_var.copy()
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
        #seq = "120"
        #new_var = my_var.at_seq("ln1")
        #if new_var is not None:
        #    print "h2", new_var._explicit()
        #    print "h2b", new_var.name()
        #    print "h2c", new_var.value()
        #    print "h2d", new_var.value("*")
        #    print "h2e", new_var.list_names()
        #    print "h2f1", new_var.list_values()
        #    print "h2f2", my_var["code_seq"].list_values("*")
        #    print "h2f2", my_var["code_seq"].get_list("*")
        #    print "h2g", new_var.list_seq()
        #else:
        #    print "h2", None
        #new_tup = c_var.ptr_to_seq("copy_ln1")
        #print "h3", new_tup
        #new_ptr = my_var.list_ref_to_seq(seq)
        #print "h4", new_ptr
        #print "h5",my_var.seq_replace(seq, c_var.ptr_to_seq("copy_ln1"), "xx")
        #print "k1 line",my_var.seq_lineage(seq)
        #print "k2 prnt",my_var.seq_parent(seq)
        #print "k3 prog",my_var.seq_progenitor(seq)
        #print "k4  del",my_var.seq_delete(seq)
        #print my_var.append_index("item", "broom")
        #print "mn1", my_var.name()
        #print "mn2", my_var.name("system_title")
        #print "mn3", my_var["system_title"].name()
        #print "mn4", my_var["item", "broom"].name("size")
        #print "mv1", my_var.value()
        #print "mv2", my_var.value("system_title")
        #print "mv3", my_var["system_title"].value()
        #print "mv4", my_var["item", "broom"].value("size")
        #print "mr1", my_var.rlist()
        #print "mr2", my_var.rlist("system_title")
        #print "mr3", my_var["system_title"].rlist()
        #print "mr4", my_var["item", "broom"].rlist("size")
        #print "ms1", my_var.seq()
        #print "ms2", my_var.seq("system_title")
        #print "ms3", my_var["system_title"].seq()
        #print "ms4", my_var["item", "broom"].seq("size")
        #print "ms5", my_var["code_seq"].seq()
        #print "ms5", my_var["code_seq"].seq("*", "r3")
        #print "ms5", my_var["code_seq"].seq("*", "r3", 1)
        #print "nn1", my_var.set_name("zip")
        #print "nn2", my_var.set_name("new_title", "system_title")
        #print "nn3", my_var["zoom_flag"].set_name("new_flag")
        #print "nn4",  my_var["item", "broom"].set_name("new_size", "size")
        #print "nn4b", my_var["item", "broom"].set_name("new_size", "size")
        #print "nv1", my_var.set_value("zip")
        #print "nv2", my_var.set_value("spook", "new_title")
        #print "nv3", my_var["new_flag"].set_value("True")
        #print "nv4",  my_var["item", "broom"].set_value("1000", "new_size")
        #print "ns1", my_var.set_seq("2000")
        #print "ns2", my_var.set_seq("3000", "new_title")
        #print "ns3", my_var["new_flag"].set_seq("4000")
        #print "ns4",  my_var["item", "broom"].set_seq("5000", "new_size")
        #print "ns4b", my_var["item", "broom"]["new_size"].name()
        #print "ns4c", my_var["item", "broom"]["new_size"].value()
        #print "ns4d", my_var["item", "broom"]["new_size"].seq()
        #print "o",my_var[("item", "zing") : ("item", "broom", 2)]
        #print "o2",my_var[("zoom_flag") : ("system_title") : 1]
        #print "o3",my_var[ : : 2]
        #my_var.extend(x_var, prefix="blah")
        
        #print "z",my_var._explicit()
        #print "z1", c_var._explicit()
        #print "z2",my_var.dump()
        #print "z3",x_var._explicit()

        #TODO: add '.del_decendants()'
        #TODO: add '.del_ancestral_branch()'
        #TODO: add '.change_name()'
=======
        print "my_var", my_var._explicit()
        #print "x_var", my_var._explicit()

        print "a",my_var["item"]
        print "b",my_var["item"].value
        my_var["item"].value="newval"
        print "c",my_var["item"].value
        # my_var.value = "blah"  #should generate a ValueError
        del my_var["item"].value
        print "d",my_var["item"].value
        del my_var.value
        print "e",my_var.value
        my_var.change("item", "bam", name="zomp", value="zig", seq="zap")
        print "f",my_var.press("item", "bam", name="zomp", value="zig", seq="zap")
        #print "g",my_var.change(name="Jim") # should generate a Value Error
        my_var["zoom_flag"]="temp"
        my_var["howsa"]="world"
        my_var["zoom_flag", "temp"]="nuther"
        my_var.press("zoom_flag", "nuther", name="nuther nuther")
        print "h", my_var["item", "broom", 1]["size"].parent_tuple()
        
        print "zmy",my_var._explicit()
        print (str(my_var))
        #print "zx",x_var._explicit()
>>>>>>> feature/properties


        my_xml = '''\
<catalog>
   <book id="bk101">
      <author>Gambardella, Matthew</author>
      <title>XML Developer's Guide</title>
      <genre>Computer</genre>
      <price>44.95</price>
      <publish_date>2000-10-01</publish_date>
      <description>An in-depth look at creating applications 
      with XML.</description>
   </book>
   <book id="bk102">
      <author>Ralls, Kim</author>
      <title>Midnight Rain</title>
      <genre>Fantasy</genre>
      <price>5.95</price>
      <publish_date>2000-12-16</publish_date>
      <description>A former architect battles corporate zombies, 
      an evil sorceress, and her own childhood to become queen 
      of the world.</description>
   </book>
</catalog>
'''
        r = xml.parse_xml(my_xml)
        print "ZZ1", r._explicit()

    else:
        print "==================================="
        print
        import doctest
        print "Testing begins. Errors found:"
        print doctest.run_docstring_examples(rolne.find, None)
        print doctest.run_docstring_examples(rolne.append, None)
        print doctest.run_docstring_examples(rolne.append_index, None)
        print doctest.run_docstring_examples(rolne.upsert, None)
        
