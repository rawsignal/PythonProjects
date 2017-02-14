from collections import OrderedDict

class fixed_object(object) :
    def __init__(self, line, **kwargs) :
        self.line = line
        args_sorted_by_value = OrderedDict(sorted(kwargs.items(), key=lambda x: x[1]))
        start_pos=0
        for key, value in args_sorted_by_value.items() :
            setattr(self, key, line[start_pos:value].strip(" "))
            start_pos=value

class delimited_object(object) :
    def __init__(self, line, delimiter, *args) :
        self.line = line
        new = line.split(delimiter)
        x=0
        for element in new :
            setattr(self, args[x], element)
            x+=1


def return_input_fixed(testconfig, **kwargs) :
    #kwargs is the name and location of vital fields for testing
    #pass field name as it would be in sybase, with the first field being in the first position. the value to pass is the ending position for that field.
    start_pos = 0
    all_items = []
    args_sorted_by_value = OrderedDict(sorted(kwargs.items(), key=lambda x: x[1]))

    if type(testconfig.get_inputfilenames()) == str :
        file_tmp = open(testconfig.get_inputpath() + testconfig.get_inputfilenames(), "r")
        objs = []
        for record in file_tmp :
            objs.append(fixed_object(record, **kwargs))
        all_items.append(objs)
    else :
        for inputfile in testconfig.get_inputfilenames() :
            file_tmp = open(testconfig.get_inputpath() + inputfile, "r")
            objs = []
            for record in file_tmp :
                objs.append(fixed_object(record, **kwargs))
        all_items.append(objs)

    return all_items


def return_input_delimited(testconfig, delimiter, *args) :
    all_items = []

    if type(testconfig.get_inputfilenames()) == str :
        file_tmp = open(testconfig.get_inputpath() + testconfig.get_inputfilenames(), "r")
        objs = []
        for record in file_tmp :
            objs.append(delimited_object(record, delimiter, *args))

        all_items.append(objs)
    else: 
        for inputfile in testconfig.get_inputfilenames() :
            file_tmp = open(testconfig.get_inputpath() + inputfile, "r")
            objs = []
            for record in file_tmp :
                objs.append(delimited_object(record, delimiter, *args))

            all_items.append(objs)

    return all_items

def clear_whitespace(all_items) :
    new_items = []
    for element in all_items:
        new_items.append(element.strip(" "))

    return new_items
        
        
            
