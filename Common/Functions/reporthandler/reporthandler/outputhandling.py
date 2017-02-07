import os
import sys
import datetime

def out_To_File(report_Name, data, ext=".txt", prepath, subpath="") :
    date = datetime.datetime.now()
    formatted_date = str(date.isoformat()).replace(":", "")
    final_path = prepath + subpath
    if not os.path.exists(final_path) :
        os.makedirs(final_path)
    new_Path = os.path.join(final_path, report_Name + formatted_date + ext)
    output = open(new_Path , "w")
    for element in data :
        output.write(element.rstrip("\n") + "\n")
    output.close()


    
