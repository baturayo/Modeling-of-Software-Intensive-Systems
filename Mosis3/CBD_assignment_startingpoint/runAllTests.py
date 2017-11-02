#!/usr/bin/env python

import unittest

from CBDMultipleOutput.Test.basicCBDTest import BasicCBDTestCase
from CBDMultipleOutput.Test.hierarchyCBDTest import HierarchyCBDTest
from CBDMultipleOutput.Test.sortedGraphCBDTest import SortedGraphCBDTest
from CBDMultipleOutput.Test.flattenCBDTest import FlattenCBDTest


allTests = [ (BasicCBDTestCase, "all CBD basic blocks"), 
             (HierarchyCBDTest, "hierarchical CBD simulator"),
             (SortedGraphCBDTest, "sorting CBD simulator"),
             (FlattenCBDTest, "flattening CBD simulator"),
            ]

for (testCase, testCaseDescription) in allTests:
  testSuite = unittest.TestLoader().loadTestsFromTestCase(testCase)
  print("")
  print(70*"+")
  print("++  running unit tests for %s" % testCaseDescription)
  print("")
  unittest.TextTestRunner(verbosity=2).run(testSuite)

