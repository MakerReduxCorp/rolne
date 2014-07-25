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
