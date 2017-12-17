from pypdevs.DEVS import *
from pypdevs.infinity import INFINITY
from generator import *
from Collector import *

class TrainNetwork(CoupledDEVS):
  def __init__(self, name="trainnetwork"):
    CoupledDEVS.__init__(self, "system")
    self.generator = self.addSubModel(generator())
    self.collector = self.addSubModel(collector())
    self.connectPorts(self.generator.QUERY, self.collector.QUERYRECV)
    self.connectPorts(self.generator.TRAIN, self.collector.TRAIN)    
    self.connectPorts(self.collector.QUERYACK, self.generator.QUERYRECV)

  def getStatistics(self):
    #Returns the statistics needed for optimalisation
    #return (10*self.lights) + self.collector.averageTime
    print(self.collector.timeSum)
    print(self.collector.numTrains)
    return self.collector.timeSum / self.collector.numTrains
