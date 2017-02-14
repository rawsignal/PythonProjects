def testvaluesprecise(val1, val2, unittest) :
    return unittest.assertEqual(val1, val2)

def testvalueexists(expected, actual, unittest) :
    #This is a less precise test, where "expected" could be within actual, though obfuscated by other characters.
    if type(actual) == list :
        for item in actual :
            return unittest.assertIn(expected, item)

    elif type(actual) == str :
        return unittest.assertIn(expected, actual)

def testvalueexistsprecise(expected, actual, unittest, strdelim = "") :
    if type(actual) == list :
        for item in actual :
            return unittest.assertEqual(expected, item)

    elif type(actual) == str :
        container = actual.split(strdelim)
        for item in container :
            return unittest.assertEqual(expected, item)

