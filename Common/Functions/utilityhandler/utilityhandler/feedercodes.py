import os
import sys
from collections import OrderedDict

def feeder_simulator(off_Feeders) :
    off_Feeder_List = off_Feeders.replace(" ", "").split(",")

    group1 = OrderedDict([("SIG4", 1), ("SIG3", 1), ("SIG2", 1), ("SIG1", 1)])
    group2 = OrderedDict([("4", 1), ("3", 1), ("2", 1), ("1", 1)])
    group3 = OrderedDict([("8", 1), ("7", 1), ("6", 1), ("5", 1)])
    group4 = OrderedDict([("12", 1), ("11", 1), ("10", 1), ("9", 1)])
    group5 = OrderedDict([("16", 1), ("15", 1), ("14", 1), ("13", 1)])
    group6 = OrderedDict([("20", 1), ("19", 1), ("18", 1), ("17", 1)])
    group7 = OrderedDict([("24", 1), ("23", 1), ("22", 1), ("21", 1)])
    group8 = OrderedDict([("NB", 1), ("NA", 1), ("PR2", 1), ("PR1", 1)])

    collator = [group1, group2, group3, group4, group5, group6, group7, group8]
        
    for x in off_Feeder_List :
        for i, item in enumerate(collator) :
            if x in collator[i] :
                collator[i][x] = 0

    groupings = []

    for x in collator :
        tmp = ""
        for key, value in x.items() :
            tmp += str(value)
        groupings.append(tmp)

    feeder = ""
    for x in groupings :
        feeder += chr(int(x,2)+65)

    print(feeder)

def feeder_decode_internal(feeder_Code, basic = False) :
    group1 = OrderedDict([("SIG4", 1), ("SIG3", 1), ("SIG2", 1), ("SIG1", 1)])
    group2 = OrderedDict([("4", 1), ("3", 1), ("2", 1), ("1", 1)])
    group3 = OrderedDict([("8", 1), ("7", 1), ("6", 1), ("5", 1)])
    group4 = OrderedDict([("12", 1), ("11", 1), ("10", 1), ("9", 1)])
    group5 = OrderedDict([("16", 1), ("15", 1), ("14", 1), ("13", 1)])
    group6 = OrderedDict([("20", 1), ("19", 1), ("18", 1), ("17", 1)])
    group7 = OrderedDict([("24", 1), ("23", 1), ("22", 1), ("21", 1)])
    group8 = OrderedDict([("NB", 1), ("NA", 1), ("PR2", 1), ("PR1", 1)])

    collator = [group1, group2, group3, group4, group5, group6, group7, group8]
    

    groupings = []
    for x in feeder_Code :
        group_Val = format(ord(x)-65, 'b')
            
        if len(group_Val) < 4 :
            missing = 4 - len(group_Val)
            tmp = "0"*missing + group_Val
            group_Val = tmp
        groupings.append(group_Val)
    print(groupings)   
    for i, group in enumerate(groupings) :
        y = 0
        for key, value in collator[i].items() :
                
            collator[i][key] = int(group[y])
            y+=1

    report_String = ""

    if basic == False: 
        for x in collator :
            for key, value in x.items() :
                if value == 1 :
                    value = "ON"
                if value == 0 :
                    value = "OFF"
                report_String += "FEEDER ID: {0}, STATE: {1}\n".format(key, value)
    if basic == True :
        for x in collator :
            for key, value in x.items() :
                if value == 1 :
                    value = "ON"
                if value == 0 :
                    value = "OFF"
                if value == "OFF" :
                    report_String += "FEEDER ID: {0}, STATE: {1}\n".format(key, value)
                

    return report_String
