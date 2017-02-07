import os
import sys

def get_Status(start, end, i) :
	if end < i :
		return "Processing Complete!"
	else:
		status = start/end * i
		sys.stdout.write("\r")
		sys.stdout.write("{0:.1f}% complete.".format(status))
		sys.stdout.flush()
		i+=1
		return i
