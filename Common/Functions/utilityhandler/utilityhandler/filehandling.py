import os
import sys

def fetch_files(prepath=os.getcwd(), exclude=[]) :
    returned_List = []
    list_Files = os.listdir(prepath)

    for files in list_Files :
        if files in exclude :
            os.remove(os.path.join(prepath, files))
        else :
            returned_List.append(os.path.join(prepath, files))

    return returned_List

fetch_Files()

    
