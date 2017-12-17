from pypdevs.DEVS import *
from pypdevs.infinity import INFINITY
from generator import *
from Collector import *
from railway import *

class TrainNetwork(CoupledDEVS):
  def __init__(self, name="trainnetwork", numTracks = 10):
    CoupledDEVS.__init__(self, "system")
    self.lights = numTracks

    self.generator = self.addSubModel(generator())
    self.collector = self.addSubModel(collector())
    self.railway = self.addSubModel(railwaysegment(2500))
    self.connectPorts(self.generator.QUERY, self.railway.QUERYRECV)
    self.connectPorts(self.generator.TRAIN, self.railway.TRAIN)    
    self.connectPorts(self.railway.QUERYACK, self.generator.QUERYRECV)

    self.connectPorts(self.railway.TRAINOUT, self.collector.TRAIN)
    self.connectPorts(self.railway.QUERYSEND, self.collector.QUERYRECV)
    self.connectPorts(self.collector.QUERYACK, self.railway.QUERYACKRECV)

  def select(self, immlist):
    #Generator should not pick first, because next track needs a chance to change it's light first
    if self.generator in immlist:
      if immlist[0] != self.generator:
        return immlist[0]
      else:
        return immlist[1]

  def getStatistics(self):
    #Returns the statistics needed for optimalisation
    #return (10*self.lights) + self.collector.averageTime
    print(self.collector.timeSum)
    print(self.collector.numTrains)
    return (10*self.lights) + (self.collector.timeSum / self.collector.numTrains)
