from pypdevs.DEVS import *
from pypdevs.infinity import INFINITY
from train import *

class collector(AtomicDEVS):
  #Collector class
  def __init__(self, name = "Collector"):
    AtomicDEVS.__init__(self, name)

    #Elapsed time, used to schedule train departments
    self.goneby = 0

    #Initial state of generator
    self.state="Wait"

    #Statistics
    #Average time in 'transit' = timeSum/numTrains
    self.timeSum = 0.0    #Total sum of time spent by trains
    self.numTrains = 0.0  #Number of trains arrived

    #Input and output ports
    self.QUERYRECV = self.addInPort(name="QUERYRECV")
    self.TRAIN = self.addInPort(name="TRAIN")
    self.QUERYACK = self.addOutPort(name="QUERYACK")

  def intTransition(self):  
    #Internal transitions
    return {"Ack": "Wait",
            "Proc": "Wait",
            "Wait": "Wait"}[self.state]


  def extTransition(self, inputs):
    #External transitions
    self.goneby += self.elapsed
    if inputs.get(self.QUERYRECV) == "query":
      #Train wants to enter, is always allowed (Holds for all states)
      return "Ack"
    elif isinstance(inputs.get(self.TRAIN), train):
      #A train arrived
      #Statistical processing
      self.numTrains += 1
      self.timeSum += self.goneby - inputs.get(self.TRAIN).deptime
      
      return "Proc"
    else:
      return self.state


  def timeAdvance(self):
    #Time advance function:
    return {"Wait": float("inf"),
            "Ack": 0,
            "Proc": 0}[self.state]
    

  def outputFnc(self):
    #Output function
    if self.state == "Ack":
      return {self.QUERYACK: "green"}
    elif self.state == "Wait" or self.state == "Proc":
      return {}
    else:
      raise DEVSException(\
      "unknown state <%s> in TrafficLight external transition function"\
      % self.state)


