#!/usr/bin/env python
#
# Unit tests for all the basic CBD blocks, discrete-time CBD. 

import unittest

from CBDMultipleOutput.Source.CBD import *

NUM_DISCR_TIME_STEPS = 5

class BasicCBDTestCase(unittest.TestCase):
  def setUp(self):
    self.CBD = CBD("CBD_for_block_under_test")    
    
  def _run(self, num_steps=1, delta_t = 1.0):
    self.CBD.run(num_steps, delta_t)      
      
  def _getSignal(self, blockname, output_port = None):
    foundBlocks = [ block for block in self.CBD.getBlocks() if block.getBlockName() == blockname ]
    numFoundBlocks = len(foundBlocks)  
    if numFoundBlocks == 1:
      signal =  foundBlocks[0].getSignal(name_output = output_port)
      return [x.value for x in signal]
    else:
      raise Exception(str(numFoundBlocks) + " blocks with name " + blockname + " found.\nExpected a single block.")  
  
  def testConstantBlock(self):
    self.CBD.addBlock(ConstantBlock(block_name="c1", value=3.3))

    self._run(NUM_DISCR_TIME_STEPS)
    self.assertEquals(self._getSignal("c1"), [3.3] * NUM_DISCR_TIME_STEPS)
    
  def testNegatorBlockPos(self):
    self.CBD.addBlock(ConstantBlock(block_name="c1", value=6.0))
    self.CBD.addBlock(NegatorBlock(block_name="n"))
    self.CBD.addConnection("c1", "n")

    self._run(NUM_DISCR_TIME_STEPS)
    self.assertEquals(self._getSignal("n"), [-6.0] * NUM_DISCR_TIME_STEPS)  
  
  def testNegatorBlockNeg(self):
    self.CBD.addBlock(ConstantBlock(block_name="c1", value=-6.0))
    self.CBD.addBlock(NegatorBlock(block_name="n"))
    self.CBD.addConnection("c1", "n")

    self._run(NUM_DISCR_TIME_STEPS)
    self.assertEquals(self._getSignal("n"), [6.0] * NUM_DISCR_TIME_STEPS)  
    
  def testNegatorBlockZero(self):
    self.CBD.addBlock(ConstantBlock(block_name="c1", value=0.0))
    self.CBD.addBlock(NegatorBlock(block_name="n"))
    self.CBD.addConnection("c1", "n")

    self._run(NUM_DISCR_TIME_STEPS)
    self.assertEquals(self._getSignal("n"), [0.0] * NUM_DISCR_TIME_STEPS)  
    
  def testInverterBlock(self):
    self.CBD.addBlock(ConstantBlock(block_name="c1", value=5.0))
    self.CBD.addBlock(InverterBlock(block_name="i1"))
    self.CBD.addBlock(InverterBlock(block_name="i2"))

    self.CBD.addConnection("c1", "i1")
    self.CBD.addConnection("i1", "i2")
    self._run(NUM_DISCR_TIME_STEPS)
    self.assertEquals(self._getSignal("i1"), [0.2] * NUM_DISCR_TIME_STEPS)
    self.assertEquals(self._getSignal("i2"), [5.0] * NUM_DISCR_TIME_STEPS)

  def testAdderBlock(self):
    self.CBD.addBlock(ConstantBlock(block_name="c1", value=2.0))
    self.CBD.addBlock(ConstantBlock(block_name="c2", value=6.0))
    self.CBD.addBlock(AdderBlock(block_name="a"))
    
    self.CBD.addConnection("c1", "a")
    self.CBD.addConnection("c2", "a")
    self._run(NUM_DISCR_TIME_STEPS)
    self.assertEquals(self._getSignal("a"), [8.0] * NUM_DISCR_TIME_STEPS)
    
  def testAdderBlock2(self):
    self.CBD.addBlock(ConstantBlock(block_name="c1", value=2.0))
    self.CBD.addBlock(ConstantBlock(block_name="c2", value=-6.0))
    self.CBD.addBlock(AdderBlock(block_name="a"))
    
    self.CBD.addConnection("c1", "a")
    self.CBD.addConnection("c2", "a")
    self._run(NUM_DISCR_TIME_STEPS)
    self.assertEquals(self._getSignal("a"), [-4.0] * NUM_DISCR_TIME_STEPS)    
    
  def testProductBlock(self):
    self.CBD.addBlock(ConstantBlock(block_name="c1", value=2.0))
    self.CBD.addBlock(ConstantBlock(block_name="c2", value=5.0))
    self.CBD.addBlock(ProductBlock(block_name="p"))
    
    self.CBD.addConnection("c1", "p")
    self.CBD.addConnection("c2", "p")
    self._run(NUM_DISCR_TIME_STEPS)
    self.assertEquals(self._getSignal("p"), [10.0] * 5)

  def testProductBlock2(self):
    self.CBD.addBlock(ConstantBlock(block_name="c1", value=1.0/2.0))
    self.CBD.addBlock(ConstantBlock(block_name="c2", value=4.0))
    self.CBD.addBlock(ProductBlock(block_name="p"))
    
    self.CBD.addConnection("c1", "p")
    self.CBD.addConnection("c2", "p")
    self._run(NUM_DISCR_TIME_STEPS)
    self.assertEquals(self._getSignal("p"), [2.0] * 5)
    
  def testGenericBlock(self):
    self.CBD.addBlock(ConstantBlock(block_name="c1", value=2.2))
    self.CBD.addBlock(GenericBlock(block_name="g", block_operator="ceil"))
    
    self.CBD.addConnection("c1", "g")
    self._run(NUM_DISCR_TIME_STEPS)
    self.assertEquals(self._getSignal("g"), [3.0] * 5)  
    
  def testRootBlock(self):
    self.CBD.addBlock(ConstantBlock(block_name="c1", value=8.0))
    self.CBD.addBlock(ConstantBlock(block_name="c2", value=3.0))
    self.CBD.addBlock(RootBlock(block_name="g"))

    self.CBD.addConnection("c1", "g")
    self.CBD.addConnection("c2", "g")
    self._run(1)
    self.assertEquals(self._getSignal("g"), [2.0])
        
  def testRootBlock2(self):
    self.CBD.addBlock(ConstantBlock(block_name="c1", value=9.0))
    self.CBD.addBlock(ConstantBlock(block_name="c2", value=2.0))
    self.CBD.addBlock(RootBlock(block_name="g"))

    self.CBD.addConnection("c1", "g")
    self.CBD.addConnection("c2", "g")
    self._run(1)
    self.assertEquals(self._getSignal("g"), [3.0])
        
  def testModuloBlock(self):
    self.CBD.addBlock(ConstantBlock(block_name="c1", value=8.0))
    self.CBD.addBlock(ConstantBlock(block_name="c2", value=3.0))
    self.CBD.addBlock(ModuloBlock(block_name="g"))

    self.CBD.addConnection("c1", "g")
    self.CBD.addConnection("c2", "g")
    self._run(1)
    self.assertEquals(self._getSignal("g"), [2.0])

  def testModuloBlock2(self):
    self.CBD.addBlock(ConstantBlock(block_name="c1", value=8.0))
    self.CBD.addBlock(ConstantBlock(block_name="c2", value=8.0))
    self.CBD.addBlock(ModuloBlock(block_name="g"))

    self.CBD.addConnection("c1", "g")
    self.CBD.addConnection("c2", "g")
    self._run(1)
    self.assertEquals(self._getSignal("g"), [0.0])

  def testPreviousValueDelayBlock(self):
    self.CBD.addBlock(ConstantBlock(block_name="ZeroConstant", value=0.0))
    self.CBD.addBlock(SequenceBlock(block_name="seq", sequence=[0, 2, 4, 6, 8, 10, 12]))
    self.CBD.addBlock(DelayBlock(block_name="d"))
    
    self.CBD.addConnection("ZeroConstant", "d", input_port_name="IC")
    self.CBD.addConnection("seq", "d")
    
    self._run(7, 0.5)
    self.assertEquals(self._getSignal("d"), [0, 0, 2, 4, 6, 8, 10])    
    
  def testPreviousValueDelayBlock2(self):
    self.CBD.addBlock(SequenceBlock(block_name="FirstSeq", sequence=[2, 12, 22, 23, 32, 11, 91]))
    self.CBD.addBlock(SequenceBlock(block_name="SecSeq", sequence=[5, 5, 5, 5, 3, 3, 3]))
    self.CBD.addBlock(DelayBlock(block_name="prev"))
    self.CBD.addConnection(self.CBD.getBlockByName("FirstSeq"), "prev")
    self.CBD.addConnection(self.CBD.getBlockByName("SecSeq"), "prev", input_port_name="IC")
    self._run(7)  
    self.assertEquals(self._getSignal("prev"), [5, 2, 12, 22, 23, 32, 11])    
          
  def testTimeBlock(self):
    self.CBD.addBlock(TimeBlock(block_name="t"))
    self._run(4)
    self.assertEquals(self._getSignal("t"), [0.0, 1.0, 2.0, 3.0])
      
  def testSequenceBlock(self):
    self.CBD.addBlock(SequenceBlock(block_name="FirstSeq", sequence=[2, 2, 2, 3, 2, 1, 1]))
    self._run(7)  
    self.assertEquals(self._getSignal("FirstSeq"), [2, 2, 2, 3, 2, 1, 1])

  def testLoggingBlock(self):
    self.CBD.addBlock(ConstantBlock(block_name="One", value=1))
    self.CBD.addBlock(LoggingBlock("Test", "Logging block test with level is error", level.ERROR))
    self.CBD.addConnection("One", "Test")
    self._run(1)
    

  def testLinearStrongComponent(self):
    self.CBD.addBlock(ConstantBlock(block_name="c2", value=5.5))
    self.CBD.addBlock(ConstantBlock(block_name="c1", value=-5))
    self.CBD.addBlock(AdderBlock(block_name="a1"))
    self.CBD.addBlock(AdderBlock(block_name="a3"))
    self.CBD.addBlock(AdderBlock(block_name="a2"))

    self.CBD.addConnection("a3", "a1")
    self.CBD.addConnection("c1", "a1")
    self.CBD.addConnection("a1", "a3")
    self.CBD.addConnection("a2", "a3")
    self.CBD.addConnection("c2", "a2")
    self.CBD.addConnection("a3", "a2")
    self._run(NUM_DISCR_TIME_STEPS)
    self.assertEquals(self._getSignal("a1"), [-5.5]*5)
    self.assertEquals(self._getSignal("a2"), [5.0]*5)
    self.assertEquals(self._getSignal("a3"), [-0.5]*5)
  
  def testLinearStrongComponentWithDelay(self):
    self.CBD.addBlock(ConstantBlock(block_name="c1", value=3.0))
    self.CBD.addBlock(AdderBlock(block_name="sum"))
    self.CBD.addBlock(DelayBlock(block_name="delay"))
    self.CBD.addBlock(NegatorBlock(block_name="neg"))

    self.CBD.addConnection("c1", "sum")
    self.CBD.addConnection("neg", "sum")
    self.CBD.addConnection("sum", "delay", input_port_name="IC")
    self.CBD.addConnection("delay", "neg")
    self.CBD.addConnection("neg", "delay")
    
    self._run(1)
    self.assertEquals(self._getSignal("delay"), [1.5])
  
  def testLinearStrongComponentWithMult(self):
    self.CBD.addBlock(ConstantBlock(block_name="c1", value=3))
    self.CBD.addBlock(ConstantBlock(block_name="c2", value=5))
    self.CBD.addBlock(AdderBlock(block_name="a"))
    self.CBD.addBlock(ProductBlock(block_name="p"))

    self.CBD.addConnection("c1", "a")
    self.CBD.addConnection("p", "a")
    self.CBD.addConnection("a", "p")
    self.CBD.addConnection("c2", "p")
    self._run(NUM_DISCR_TIME_STEPS)
    self.assertEquals(self._getSignal("a"), [-0.75]*5)
    self.assertEquals(self._getSignal("p"), [-3.75]*5)
    
  def testLinearStrongComponentWithNeg(self):
    self.CBD.addBlock(ConstantBlock(block_name="c1", value=5))
    self.CBD.addBlock(ConstantBlock(block_name="c2", value=8))
    self.CBD.addBlock(AdderBlock(block_name="a1"))
    self.CBD.addBlock(AdderBlock(block_name="a2"))
    self.CBD.addBlock(NegatorBlock(block_name="n"))

    self.CBD.addConnection("c1", "a1")
    self.CBD.addConnection("a2", "a1")
    self.CBD.addConnection("c2", "a2")
    self.CBD.addConnection("n", "a2")
    self.CBD.addConnection("a1", "n")  
    self._run(NUM_DISCR_TIME_STEPS)
    self.assertEquals(self._getSignal("a1"), [6.5]*5)
    self.assertEquals(self._getSignal("a2"), [1.5]*5)  
    self.assertEquals(self._getSignal("n"), [-6.5]*5)  
    
  def testTwoLinearStrongComponent(self):
    self.CBD.addBlock(ConstantBlock(block_name="c1", value=3))
    self.CBD.addBlock(ConstantBlock(block_name="c2", value=2))
    self.CBD.addBlock(ConstantBlock(block_name="c3", value=1.5))
    self.CBD.addBlock(ConstantBlock(block_name="c4", value=1))
    self.CBD.addBlock(AdderBlock(block_name="a1"))
    self.CBD.addBlock(AdderBlock(block_name="a2"))
    self.CBD.addBlock(AdderBlock(block_name="a3"))
    self.CBD.addBlock(AdderBlock(block_name="a4"))
    self.CBD.addBlock(AdderBlock(block_name="a5"))
    self.CBD.addBlock(ProductBlock(block_name="p"))
    self.CBD.addBlock(NegatorBlock(block_name="n1"))
    self.CBD.addBlock(NegatorBlock(block_name="n2"))

    self.CBD.addConnection("a3", "a1")
    self.CBD.addConnection("c1", "a1")
    self.CBD.addConnection("c2", "a2")
    self.CBD.addConnection("a3", "a2")
    self.CBD.addConnection("a1", "a3")
    self.CBD.addConnection("a2", "a3")
    self.CBD.addConnection("a3", "p")
    self.CBD.addConnection("c3", "p")
    self.CBD.addConnection("p", "n1")
    self.CBD.addConnection("n1", "a4")
    self.CBD.addConnection("a5", "a4")
    self.CBD.addConnection("c4", "a5")
    self.CBD.addConnection("n2", "a5")
    self.CBD.addConnection("a4", "n2")
    self._run(NUM_DISCR_TIME_STEPS)
    self.assertEquals(self._getSignal("a1"), [-2.0]*5)
    self.assertEquals(self._getSignal("a2"), [-3.0]*5)
    self.assertEquals(self._getSignal("a3"), [-5.0]*5)
    self.assertEquals(self._getSignal("a4"), [4.25]*5)
    self.assertEquals(self._getSignal("a5"), [-3.25]*5)
    self.assertEquals(self._getSignal("p"), [-7.5]*5)
    self.assertEquals(self._getSignal("n1"), [7.5]*5)
    self.assertEquals(self._getSignal("n2"), [-4.25]*5)
        
  def testNonLinearStrongComponent(self):
    self.CBD.addBlock(ConstantBlock(block_name="c1", value=15))
    self.CBD.addBlock(ConstantBlock(block_name="c2", value=10))
    self.CBD.addBlock(AdderBlock(block_name="a1"))
    self.CBD.addBlock(AdderBlock(block_name="a2"))
    self.CBD.addBlock(ProductBlock(block_name="p"))

    self.CBD.addConnection("c2", "a1")
    self.CBD.addConnection("p", "a1")
    self.CBD.addConnection("a1", "p")
    self.CBD.addConnection("a2", "p")
    self.CBD.addConnection("p", "a2")
    self.CBD.addConnection("c1", "a2")
    self.assertRaises(SystemExit, self._run, 5)    
    
  def initializeFuncDerBas(self):
    #f(t) = 5*t  
    CBDFunc = CBD("function", output_ports = ["OUT1"])
    CBDFunc.addBlock(TimeBlock(block_name="t"))
    CBDFunc.addBlock(ProductBlock(block_name="p"))
    CBDFunc.addBlock(ConstantBlock(block_name="c", value=5.0))
    CBDFunc.addConnection("t", "p") 
    CBDFunc.addConnection("c", "p")
    CBDFunc.addConnection("p", "OUT1")
    return CBDFunc      
      
  def initializeFunc(self):
    #f(t) = (t-2)^3  
    CBDFunc = CBD("function", output_ports = ["OUT1"])
    CBDFunc.addBlock(TimeBlock(block_name="t"))
    CBDFunc.addBlock(ProductBlock(block_name="p"))
    CBDFunc.addBlock(ProductBlock(block_name="p2"))
    CBDFunc.addBlock(AdderBlock(block_name="a"))
    CBDFunc.addBlock(ConstantBlock(block_name="c", value=-2.0))
    CBDFunc.addConnection("t", "a") 
    CBDFunc.addConnection("c", "a")
    CBDFunc.addConnection("a", "p")
    CBDFunc.addConnection("a", "p")
    CBDFunc.addConnection("p", "p2")
    CBDFunc.addConnection("a", "p2")
    CBDFunc.addConnection("p2", "OUT1")
    return CBDFunc  
      
  def initializeFunc2(self):
    #f(t) = (t-2)^4
    CBDFunc = CBD("function", output_ports = ["OUT1"])
    CBDFunc.addBlock(TimeBlock(block_name="t"))
    CBDFunc.addBlock(ProductBlock(block_name="p"))
    CBDFunc.addBlock(ProductBlock(block_name="p2"))
    CBDFunc.addBlock(ProductBlock(block_name="p3"))
    CBDFunc.addBlock(AdderBlock(block_name="a"))
    CBDFunc.addBlock(ConstantBlock(block_name="c", value=-2.0))
    CBDFunc.addConnection("t", "a") 
    CBDFunc.addConnection("c", "a")
    CBDFunc.addConnection("a", "p")
    CBDFunc.addConnection("a", "p")
    CBDFunc.addConnection("p", "p2")
    CBDFunc.addConnection("a", "p2")
    CBDFunc.addConnection("p2", "p3")
    CBDFunc.addConnection("a", "p3")
    CBDFunc.addConnection("p3", "OUT1")
    return CBDFunc      
  
  def initializeFuncInt(self):
    #f(t) = 2*t  
    CBDFunc = CBD("function", output_ports = ["OUT1"])
    CBDFunc.addBlock(TimeBlock(block_name="t"))
    CBDFunc.addBlock(ProductBlock(block_name="p"))
    CBDFunc.addBlock(ConstantBlock(block_name="c", value=2.0))
    CBDFunc.addConnection("t", "p") 
    CBDFunc.addConnection("c", "p")
    CBDFunc.addConnection("p", "OUT1")
    return CBDFunc  
     
  def testDerivatorBlock(self):
    self.CBD.addBlock(ConstantBlock(block_name="c3", value=1.0))
    self.CBD.addBlock(ConstantBlock(block_name="zero", value=0.0))
    CBDFunc = self.initializeFuncDerBas()
    self.CBD.addBlock(CBDFunc) 
    self.CBD.addBlock(DerivatorBlock(block_name="der"))
    
    self.CBD.addConnection("c3", "der", input_port_name="delta_t")
    self.CBD.addConnection("zero", "der", input_port_name="IC")
    self.CBD.addConnection("function", "der")
    self._run(5)
    self.assertEquals(self._getSignal("der"), [0.0]+[5.0]*4)    

            
  def testIntegratorBlock(self):
    self.CBD.addBlock(ConstantBlock(block_name="c1", value=6.0))
    self.CBD.addBlock(ConstantBlock(block_name="c2", value=0.0))
    self.CBD.addBlock(ConstantBlock(block_name="c3", value=0.001))
    self.CBD.addBlock(AdderBlock(block_name="a"))
    self.CBD.addBlock(DelayBlock(block_name="d"))
    
    self.CBD.addBlock(IntegratorBlock(block_name="int"))
    self.CBD.addConnection("c3", "int", input_port_name="delta_t")
    self.CBD.addConnection("a", "int")
    self.CBD.addConnection("c2", "int", input_port_name="IC")
    
    self.CBD.addConnection("c1", "a")
    self.CBD.addConnection("d", "a")
    self.CBD.addConnection("a", "d")
    self.CBD.addConnection("c2", "d", input_port_name="IC")
    self._run(NUM_DISCR_TIME_STEPS)
    self.assertEquals(self._getSignal("int"), [0.0, 0.006, 0.018000000000000002, 0.036000000000000004, 0.060000000000000005])
  
  def testDelayBlock(self):
    self.CBD.addBlock(ConstantBlock(block_name="c1", value=5.0))
    self.CBD.addBlock(ConstantBlock(block_name="c2", value=3.0))
    self.CBD.addBlock(DelayBlock(block_name="d"))
    
    self.CBD.addConnection("c2", "d")
    self.CBD.addConnection("c1", "d", input_port_name="IC")
    self._run(4)
    self.assertEquals(self._getSignal("d"), [5.0, 3.0, 3.0, 3.0])

  def testDelayBlock2(self):
    self.CBD.addBlock(ConstantBlock(block_name="c1", value=1.0))
    self.CBD.addBlock(ConstantBlock(block_name="c2", value=5.0))
    self.CBD.addBlock(DelayBlock(block_name="d"))
    self.CBD.addBlock(AdderBlock(block_name="a"))

    self.CBD.addConnection("c2", "a")
    self.CBD.addConnection("d", "a")
    self.CBD.addConnection("c1", "d", input_port_name="IC")
    self.CBD.addConnection("a", "d")
    self._run(5)
    self.assertEquals(self._getSignal("d"), [1.0, 6.0, 11.0, 16.0, 21.0])
      

def suite():
    """Returns a test suite containing all the test cases in this module."""
    suite = unittest.makeSuite(BasicCBDTestCase)
    
    return unittest.TestSuite((suite))

if __name__ == '__main__':
    # When this module is executed from the command-line, run all its tests
    unittest.main(verbosity=2)

  
  
  
  
  
  
  
  
