#!/usr/local/bin/python
# -*- coding: utf-8 -*-

'''
Created on 2014��11��3��

@author: Administrator
'''

import unittest
import TestplanParser

class SampleTC(unittest.TestCase):
    '''
    classdocs
    '''

    def test_sample(self):
        at = TestplanParser.Webapitest('Testplan.xml')
        at.runTestCase()
    
    def setUp(self):
        print "Running test case:", unittest.TestCase.id(self)
        
    def tearDown(self):
        print "\n---------------------------------------------"
        print ""
        