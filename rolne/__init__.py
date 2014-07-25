# rolne\__init__.py
#
# rolne datatype class: Recursive Ordered List of Named Elements
#
# Version 0.1.0
    
import copy

class rolne(object):

    def __init__(self, in_list=[]):
        self.data = in_list

    def __str__(self):
        result = "<rolne datatype object>\n"
        result += self.mards()
        return result

    def __getitem__(self, tup):
        name, value = tup
        for entry in self.data:
            if entry[0]==name:
                if entry[1]==value:
                    return(rolne(entry[2]))
        raise KeyError, "name and value not found"
        return None

    def __setitem__(self, tup, value):
        name, cur_value = tup
        for i,(entry_name, entry_value, entry_list) in enumerate(self.data):
            if entry_name==name:
                if entry_value==cur_value:
                    new_tuple = (entry_name, value, entry_list)
                    self.data[i] = new_tuple
                    return True
        self.append(name, value)
        return True

    def mards(self):
        result = ""
        # return repr(self.data)
        if self.data:
            for entry in self.data:
                result += entry[0]
                if entry[1] is not None:
                    printable = str(entry[1])
                    quote_flag = False
                    if '"' in printable:
                        quote_flag = True
                    if len(printable) != len(printable.strip()):
                        quote_flag = True
                    if quote_flag:
                        result += " "+'"'+str(entry[1])+'"'
                    else:
                        result += " "+str(entry[1])
                result += "\n"
                if entry[2]:
                    # result += "*"
                    temp = rolne(entry[2]).mards()
                    for line in temp.split("\n"):
                        if line:
                            result += "    "+line
                            result += "\n"
        else:
            result = "None\n"
        return result

    def append(self, name, value=None):
        new_tuple = (name, value, [])
        for entry in self.data:
            if entry[0]==name:
                if entry[1]==value:
                    return False
        self.data.append(new_tuple)
        return True

    def get_list(self, name):
        result = []
        for entry in self.data:
            if entry[0]==name:
                result.append(entry[1])
        return result

    def value(self, name):
        for (en, ev, el) in self.data:
            if en==name:
                return ev
        return None

    def reset_value(self, name, value):
        for (en, ev, el) in self.data:
            if en==name:
                return self.__setitem__((en, ev), value)
        return False
    
if __name__ == "__main__":

    if True:

        my_var = rolne()

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

        print "a", my_var
        #print "b", my_var["item", "zing"]
        #print "c", my_var.get_list("item")
        #my_var["item", "broom"]["size", "7"] = '9'
        #print "d", my_var
        #print "e", my_var["item", "bam"].value("size")
        my_var["item", "zing"].reset_value("color", "white")
        print "f", my_var

    else:
        print "==================================="
        print
        import doctest
        print "Testing begins. Errors found:"
