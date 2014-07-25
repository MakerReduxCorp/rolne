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

    my_var = rolne()

To build the above example:

    my_var.append("item", "zing")
    my_var["item", "zing"].append("size", "4")
    my_var["item", "zing"].append("color", "red")
    my_var["item", "zing"]["color", "red"].append("intensity", "44%")
    my_var["item", "zing"].append("color", "yellow")
    my_var.append("item", "womp")
    my_var["item", "womp"].append("size", "5")
    my_var["item", "womp"].append("color", "blue")
    my_var.append("item", "bam")
    my_var.append("item", "broom")
    my_var["item", "broom"].append("size", "7")
    my_var["item", "broom"].append("title", 'The "big" thing')
    my_var.append("zoom_flag")
    my_var.append("system_title", "hello")


To get the list of items:

    >>> print my_var.get_list("item")
    ["zing", "womp", "bam", "broom"]
    
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
