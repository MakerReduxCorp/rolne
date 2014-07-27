rolne
=====

rolne data type: Recursive Ordered Lists of Named Elements

Internally, the rolne data type is stored as a list of three-item tuples. Each tuple being:

    (name, value, tuple_list)
    
each tuple_list is a list of tuples of the same type. Structurally, the following MARDS text:

    item zing
        size 4
        color red
            intensity 44%
        color yellow
    item womp
        size 5
        color blue
    item bam
    item broom
        size 7
        title "The "big" thing"
    zoom_flag
    code_seq
        * r9
        * r3
        * r2
        * r3
    system_title hello

becomes:

    [
        ("item", "zing", [
            ("size", "4", []), ("color", "red", []), ("color", "yellow", [])
        ]),
        ("item", "womp", [
            ("size", "5", []), ("color", "blue", [])
        ]),
        ("item", "bam", []),
        ("item", "broom", [("size", "7", [])]),
        ("zoom_flag", None, []),
        ("system_title", "hello", [])
    ]
    
One could parse a rolne data type without this library as python already supports tuples and lists.

Usage
-----

Simply use the class for the declaration:

    test = rolne()

To simply add a name/value pair, use either the 'append' or 'upsert' method.

The 'append' method adds the name/value pair to the end of the list.

    test.append("aa", "1")
    test.append("aa", "1")

which results in:

    aa 1
    aa 1
    bb 2
    
The 'upsert' method only adds the name/value pair to the list if it does not exist elsewhere.

    test.upsert("bb", "2")
    test.upsert("bb", "2")
   
which results in:

    aa 1
    aa 1
    bb 2

As a general rule, use upsert when you want a particular name/value pair to exist in only one place. Use append when
duplicates are just fine.

To reference the _first_ occurance of a name/value pair in the list, one can either use the 'first' method or directly reference with with the name/value tuple enclosed in brackets. For example:

    test.first("aa", "1")
    
and

    test["aa", "1"]
    
both refer to the first occurance of _aa 1_.

Using such a reference, one could 'append' or 'upsert' name/value children:

    test["aa", "1"].upsert("z", "5")
    
which results in:

    aa 1
        z 5
    aa 1
    bb 2

To build the example from the intro:

    my_var = rolne()
    my_var.upsert("item", "zing")
    my_var["item", "zing"].upsert("size", "4")
    my_var["item", "zing"].upsert("color", "red")
    my_var["item", "zing"]["color", "red"].upsert("intensity", "44%")
    my_var["item", "zing"].upsert("color", "yellow")
    my_var.upsert("item", "womp")
    my_var["item", "womp"].upsert("size", "5")
    my_var["item", "womp"].upsert("color", "blue")
    my_var.upsert("item", "bam")
    my_var.upsert("item", "broom")
    my_var["item", "broom"].upsert("size", "7")
    my_var["item", "broom"].upsert("title", 'The "big" thing')
    my_var.upsert("zoom_flag")
    my_var.upsert("code_seq")
    my_var["code_seq", None].append("*", "r9")
    my_var["code_seq", None].append("*", "r3")
    my_var["code_seq", None].append("*", "r2")
    my_var["code_seq", None].append("*", "r3")
    my_var.upsert("system_title", "hello")

To get the list of items:

    >>> print my_var.get_list("item")
    ["zing", "womp", "bam", "broom"]
    
To get the list of entries in 'code_seq':

    >>> print my_var["code_seq", None].get_list("*")
    ["r9", "r3", "r2", "r3"]
    
To get the 'colors' of 'item zing':

    >>> print my_var["item", "zing"].get_list("color")
    ["red", "blue"]
    
To get the 'colors' of 'item bam':

    >>> print my_var["item", "bam"].get_list("color")
    []
    
To get the 'size' of 'item zing':

    >>> print my_var["item", "zing"].value("size")
    4

Of note: the 'value' method returns the first entry that matches, if there are any matches. Later entries are ignored. If no entries match, then None is returned.

Of course, one could also do:

    >>> print my_var["item", "zing"].get_list("size")[0]
    4

But only do this if you are confident there is a size value. Otherwise you could get a key error.

To get the 'size' of 'item bam':

    >>> print my_var["item", "bam"].value("size")
    None
    
To change a value of an existing entry:

    >>> my_var["item", "zing"]="zong"
    >>> print my_var.get_list("item")
    ["zong", "womp", "bam", "broom"]
    
Another example:

    >>> my_var["item", "broom"]["size", "7"] = "9"
    >>> print my_var["item", "broom"].value("size")
    9
    
An example that assumes we do not know the current size:

    >>> size = my_var["item", "broom"].value("size")
    >>> my_var["item", "broom"]["size", size] = "11"
    >>> print my_var["item", "broom"].value("size")
    11
    
Or, even simpler:

    >>> my_var["item", "broom"].reset_value("size", "13")
    >>> print my_var["item", "broom"].value("size")
    13

Just like the 'value' method, the 'reset_value' method only operates on the first entry found.
