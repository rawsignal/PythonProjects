import os
import sys
import datetime

def out_to_file(report_Name, data, ext=".txt", testconfig) :
    date = datetime.datetime.now()
    formatted_date = str(date.isoformat()).replace(":", "")
    if not os.path.exists(testconfig.get_outputpath()) :
        os.makedirs(testconfig.get_outputpath())
    new_Path = os.path.join(testconfig.get_outputpath(), report_Name + formatted_date + ext)
    output = open(new_Path , "w")
    if type(data) == list :
        for element in data :
            output.write(element.rstrip("\n") + "\n")
        output.close()
    elif type(data) == str :
            output.write(data.rstrip("\n") + "\n")
        output.close()


    
