import unittest, doctest

from DateTime.DateTime import DateTime
from Testing.ZopeTestCase import FunctionalDocFileSuite as Suite

from Products.PloneTestCase.PloneTestCase import FunctionalTestCase, \
    setupPloneSite
setupPloneSite()

optionflags = doctest.REPORT_ONLY_FIRST_FAILURE | doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE

def setUp(self):
    pass

def test_suite():    
    tests = (
        Suite(
            'README.txt', 
            package="upfront.simplereferencefield",
            setUp=setUp,
            optionflags=optionflags,
            test_class=FunctionalTestCase
        ),
    )    
    return unittest.TestSuite(tests)
