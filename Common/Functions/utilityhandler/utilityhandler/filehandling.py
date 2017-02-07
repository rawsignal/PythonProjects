import os
import sys
import datetime

def fetch_Files(prepath, exclude=[]) :
    returned_List = []
    list_Files = os.listdir(prepath)

    for files in list_Files :
        if files in exclude :
            os.remove(os.path.join(prepath, files))
        else :
            returned_List.append(os.path.join(preapth, files))

    return returned_List

    
