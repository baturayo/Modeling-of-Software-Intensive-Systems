__author__ = 'joachimdenil'

import unittest
from CBDMultipleOutput.Source.CBD import *
from CBDMultipleOutput.Source.plot import ScopeWindow
from basicCBDTest import BasicCBDTestCase

NUM_DISCR_TIME_STEPS = 10

class FlattenCBDTest(unittest.TestCase):
    def setUp(self):
        self.CBD = CBD("block_under_test")

    def _run(self, num_steps=1, step = 1):
        self.CBD.run(num_steps, step)

    def _getSignal(self, blockname, output_port = None):
        foundBlocks = [ block for block in self.CBD.getBlocks() if block.getBlockName() == blockname ]
        signal =  foundBlocks[0].getSignal(name_output = output_port)
        if len(foundBlocks) == 1:
            return [x.value for x in signal]
        else:
            raise Exception("No single block with name " + blockname + " found")

    def testCounter(self):
        self.CBD.addBlock(ConstantBlock(block_name="zero", value=0.0))
        self.CBD.addBlock(DelayBlock(block_name="s"))
        self.CBD.addConnection("zero", "s", input_port_name="IC")
        self.CBD.addBlock(ConstantBlock(block_name="one", value=1.0))
        self.CBD.addBlock(AdderBlock(block_name="plusOne"))
        self.CBD.addConnection("one", "plusOne")
        self.CBD.addConnection("s", "plusOne")
        self.CBD.addConnection("plusOne", "s")

        self._run(NUM_DISCR_TIME_STEPS)
        ScopeWindow([self._getSignal("zero"), self._getSignal("one"), self._getSignal("s")],
            ["zero", "one", "s"] )
        self.assertEquals(self._getSignal("s"), [float(x) for x in range(NUM_DISCR_TIME_STEPS)])

def suite():
    """Returns a suite containing all the test cases in this module."""
    suite1 = unittest.makeSuite(BasicCBDTestCase)

    return unittest.TestSuite((suite1))

if __name__ == '__main__':
    # When this module is executed from the command-line, run all its tests
    unittest.main()
