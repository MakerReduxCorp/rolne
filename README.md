rolne
=====

rolne data type: Recursive Ordered Lists of Named Elements

Internally, the rolne data type is stored as a list of three-item tuples. Each tuple being:

    (name, value, tuple_list)
    
each tuple_list is a list of tuples of the same type. Structurally, the following MARDS text:

    item "zing"
        size 4
        color red
        color yellow
    item "womp"
        size 5
        color blue
    item "bam"
    item "broom"
        size 7
    zoom_flag
    system_title "hello"
    
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
    my_var["item", "zing"].append("color", "blue")
    my_var.append("item", "womp")
    

To get the list of items:

    >>> print my_var["item"]
    ["zing", "womp", "bam", "broom"]
    
To get the 'colors' of 'item zing':

    >>> print my_var["item", "zing"]["color"]
    ["red", "blue"]
    
    
To get the 'colors' of 'item bam':

    >>> print my_var["item", "bam"]
    []
    
To get the 'size' of 'item zing':

    >>> print my_var["item", "zing"].first("size")
    4

Of course, one could also do:

    >>> print my_var["item", "zing"]["size"][0]
    4

But only do this if you are confident there is a size value. Otherwise you could get a key error.

To get the 'size' of 'item bam':

    >>> print my_var["item", "bam"].first("size")
    None
    
