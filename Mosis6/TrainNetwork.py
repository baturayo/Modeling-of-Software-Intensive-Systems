from pypdevs.DEVS import *
from pypdevs.infinity import INFINITY
from generator import *
from Collector import *
from railway import *

class TrainNetwork(CoupledDEVS):
  def __init__(self, name="trainnetwork", numTracks = 10, trackLength = 2500, numTrains = 10, a = (10, 30), iat = (20, 50), vmax = 150):
    CoupledDEVS.__init__(self, "system")
    self.lights = numTracks

    self.generator = self.addSubModel(generator(num_trains = numTrains, IAT = iat, a_max = a))
    self.railways = []
    for x in range(numTracks):
      self.railways.append(self.addSubModel(railwaysegment("Rail" + str(x), trackLength, vmax)))

    self.collector = self.addSubModel(collector())


    self.connectPorts(self.generator.QUERY, self.railways[0].QUERYRECV)
    self.connectPorts(self.generator.TRAIN, self.railways[0].TRAIN)    
    self.connectPorts(self.railways[0].QUERYACK, self.generator.QUERYRECV)

    for x in range(1, self.lights):
      self.connectPorts(self.railways[x-1].TRAINOUT, self.railways[x].TRAIN)
      self.connectPorts(self.railways[x-1].QUERYSEND, self.railways[x].QUERYRECV)
      self.connectPorts(self.railways[x].QUERYACK, self.railways[x-1].QUERYACKRECV)

    self.connectPorts(self.railways[-1].TRAINOUT, self.collector.TRAIN)
    self.connectPorts(self.railways[-1].QUERYSEND, self.collector.QUERYRECV)
    self.connectPorts(self.collector.QUERYACK, self.railways[-1].QUERYACKRECV)

  def select(self, immlist):
    #Generator should not pick first, because next track needs a chance to change it's light first
    if self.generator in immlist:
      if immlist[0] != self.generator:
        return immlist[0]
      else:
        return immlist[1]
    else:
      return immlist[0]

  def getStatistics(self):
    #Returns the statistics needed for optimalisation
    #return (10*self.lights) + self.collector.averageTime
    print(self.collector.timeSum)
    print(self.collector.numTrains)
    return (10*self.lights) + (self.collector.timeSum / self.collector.numTrains)
