from pypdevs.DEVS import *
from pypdevs.infinity import INFINITY
from train import *
import random
    
class generator(AtomicDEVS):

  def __init__(self, name="generator" , num_trains = 10, IAT = (0, 50), a_max = (20, 30)):
    AtomicDEVS.__init__(self, name)
    
    #Generate num_trains trains and add to queue
    self.queue = []

    for x in range(num_trains):
      amax = random.randint(a_max[0], a_max[1])
      iat = random.randint(IAT[0], IAT[1])
      deptime = self.queue[0].deptime + iat if len(self.queue) != 0 else 0
      self.queue.insert(0, train(x, amax, deptime))

    #Elapsed time, used to schedule train departments
    self.goneby = 0

    #Initial state of generator
    self.state="Wait"

    #Input and output ports
    self.QUERYRECV = self.addInPort(name="QUERYRECV")
    self.QUERY = self.addOutPort(name="QUERY")
    self.TRAIN = self.addOutPort(name="TRAIN")


  def intTransition(self):
    #Internal transitions
    self.goneby += self.timeAdvance()    #Update elapsed time on transition
    return {"Wait": "Send",
            "Send": "Poll",
            "Poll": "Send",
            "Allowed": "Wait"}[self.state]


  def extTransition(self, inputs):
    #External transitions
    input = inputs.get(self.QUERYRECV)
    if input == "green":
      #Green light, return to wait (Holds for all states)
      return "Allowed"
    else:
      return self.state


  def timeAdvance(self):
    #Time advance function:
    waittime = max(0, self.queue[-1].deptime - self.goneby) if len(self.queue) != 0 else float('inf')
    return {"Wait": waittime,
            "Send": 0,
            "Poll": 1,
            "Allowed": 0}[self.state]
    

  def outputFnc(self):
    #Output function
    if self.state == "Send":
      return {self.QUERY: "query"}
    elif self.state == "Allowed":
      return {self.TRAIN: self.queue.pop()}
    elif self.state == "Poll" or self.state == "Wait":
      return {}
    else:
      raise DEVSException(\
      "unknown state <%s> in TrafficLight external transition function"\
      % self.state)
generator()
