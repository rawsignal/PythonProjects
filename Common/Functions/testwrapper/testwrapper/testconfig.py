import sys
import datetime

class testconfig(object) :
    def __init__(self, inputpath, outputpath, inputfilenames) :
        self.inputpath = inputpath
        self.outputpath = outputpath
        self.inputfilenames = inputfilenames
        date = datetime.datetime.now()
        formatted_date = str(date.isoformat()).replace(":", "")
        sys.stdout = open(self.outputpath+"test_results"+formatted_date+".txt", "w")


    def get_inputpath(self) :
        return self.inputpath

    def get_outputpath(self) :
        return self.outputpath

    def get_inputfilenames(self) :
        return self.inputfilenames

    def __exit__(self) :
        sys.stdout.close()

    
