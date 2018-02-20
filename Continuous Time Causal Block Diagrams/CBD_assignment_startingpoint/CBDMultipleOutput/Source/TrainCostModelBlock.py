#!/usr/bin/env python
from CBDMultipleOutput.Source.CBD import *

class CostFunctionBlock(BaseBlock):        
    def __init__(self, block_name):
        BaseBlock.__init__(self, block_name, ["InVi","InVTrain","InDelta","InXPerson"], ["OutCost"])
        self.viChanged = False
        self.timeInWhichViChanged = 0.0
        self.cummulativeCost = 0.0
        
    def compute(self, curIteration):
        displacement_person = self.getInputSignal(curIteration, "InXPerson").value
        velocity_train = self.getInputSignal(curIteration, "InVTrain").value
        
        if abs(displacement_person) > 0.4 or velocity_train<0.0:
            raise StopSimulationException()
        
        currentVi = self.getInputSignal(curIteration, "InVi").value
        currentTime = self.getClock().getTime()
        lastVi = self.getInputSignal(curIteration-1, "InVi").value
        if lastVi != currentVi:
            self.viChanged = True
            self.timeInWhichViChanged = currentTime
            self.attainedVelocity = False
        else:
            self.viChanged = False
        
        lastVTrain = self.getInputSignal(curIteration-1, "InVTrain").value
        currentVTrain = self.getInputSignal(curIteration, "InVTrain").value
        if ((lastVTrain-currentVi)*(currentVTrain-currentVi) <= 0):
            self.attainedVelocity = True;
        
        if (not self.attainedVelocity):
            instantCostTime = currentTime - self.timeInWhichViChanged
            assert instantCostTime >= 0
            delta_t = self.getInputSignal(curIteration, "InDelta").value
            self.cummulativeCost = self.cummulativeCost + instantCostTime*delta_t
        
        self.appendToSignal(self.cummulativeCost, name_output="OutCost")



class AboveThresholdBlock(BaseBlock):
    def __init__(self, block_name, threshold):
        BaseBlock.__init__(self, block_name, ["IN1"], ["OUT1"])
        self.threshold = threshold

    def compute(self, curIteration):
        self.appendToSignal(1.0 if self.getInputSignal(curIteration).value > self.threshold else -1.0)



class StopSimulationBlock(BaseBlock):
    def __init__(self, block_name):
        BaseBlock.__init__(self, block_name, ["IN1"], [])

    def compute(self, curIteration):
        inSignalValue = self.getInputSignal(curIteration).value
        if inSignalValue > 0.0:
            raise StopSimulationException()
        

class StopSimulationException(Exception):
    pass
        








