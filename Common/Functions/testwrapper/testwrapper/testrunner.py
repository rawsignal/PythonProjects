import unittest
import sys

def runtest(*args) :
    for test in args:
        suite = unittest.TestLoader().loadTestsFromTestCase(test)
        unittest.TextTestRunner(stream=sys.stdout, verbosity=2).run(suite)
