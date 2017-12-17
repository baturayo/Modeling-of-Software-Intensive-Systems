from pypdevs.DEVS import *
from pypdevs.infinity import INFINITY
from train import *
import random
from formulas import *

class light(AtomicDEVS):
  def __init__(self, name = "light"):
    AtomicDEVS.__init__(self, name)

    #Initial state of generator
    self.state="Green"

    #Input and output ports
    self.QUERYRECV = self.addInPort(name="QUERYRECV")
    self.CHANGECOL = self.addInPort(name="CHANGECOL")
    self.QUERYACK = self.addOutPort(name="QUERYACK")

  def intTransition(self):  
    #Internal transitions
    return {"Green": "Green",
            "Red": "Red",
            "GQuery": "Green",
            "RQuery": "Red"}[self.state]


  def extTransition(self, inputs):
    #External transitions
    if inputs.get(self.QUERYRECV) == "query":
      if self.state == "Green":
        return "GQuery"
      elif self.state == "Red":
        return "RQuery"
    elif inputs.get(self.CHANGECOL) == "setred" and self.state == "Green":
      return "Red"
    elif inputs.get(self.CHANGECOL) == "setgreen" and self.state == "Red":
      return "Green"

    return self.state


  def timeAdvance(self):
    #Time advance function:
    return {"Green": float("inf"),
            "Red": float("inf"),
            "GQuery": 0,
            "RQuery": 0}[self.state]
    

  def outputFnc(self):
    #Output function
    if self.state == "RQuery":
      return {self.QUERYACK: "red"}
    elif self.state == "GQuery":
      return {self.QUERYACK: "green"}
    else:
      return {}

class railway(AtomicDEVS):
  def __init__(self, name = "railway", l = 5000):
    AtomicDEVS.__init__(self, name)

    #Initial state of generator
    self.state="Idle"

    self.length = l
    #Train
    self.train = None

    #Input and output ports
    self.QUERYRECV = self.addInPort(name="QUERYRECV")
    self.TRAININ = self.addInPort(name="TRAININ")
    self.TRAINOUT = self.addOutPort(name="TRAINOUT")
    self.QUERY = self.addOutPort(name="QUERY")
    self.CHANGECOL = self.addOutPort(name="CHANGECOL")

  def intTransition(self):  
    #Internal transitions
    #Idle: No train on the track
    #TrainIn: Intermediate state to switch light
    #TrainAccel: A train has entered and is accelerating 
    #NextLight: The train spots the next light
    #Query: The train has queried the next track
    #Accel: The train has received a green light and is accelerating towards the next track
    return {"Idle": "Idle",
            "TrainIn": "TrainAccel",
            "TrainAccel": "NextLight",
            "NextLight": "Query",
            "Query": "Query",
            "Accel": "Idle"}[self.state]


  def extTransition(self, inputs):
    #External transitions
    if isinstance(inputs.get(self.TRAININ), train) and self.state == "Idle":
      self.train = inputs.get(self.TRAININ)
      return "TrainIn"
    elif inputs.get(self.QUERYRECV) == "red" and self.state == "Query":
      #Calculate next brakepoint for train and return to Nextlight for next query
      result = brake_formula(self.train.v, 1, self.train.x_remaining)
      self.train.v = result[0]
      self.train.x_remaining -= result[1]
      return "NextLight"
    elif inputs.get(self.QUERYRECV) == "green" and self.state == "Query":
      return "Accel"

    return self.state


  def timeAdvance(self):
    #Time advance function:
    if self.state == "Idle" or self.state == "Query":
      return float("inf")
    elif self.state == "NextLight":
      return 1
    elif self.state == "TrainAccel":
      #Calculate time using accel formula
      settings = acceleration_formula(self.train.v, 120, self.length - 1000, self.train.a_max)
      self.train.v = settings[0]
      self.train.remaining_x = self.length - 1000
      return settings[1]
    elif self.state == "Accel":
      settings = acceleration_formula(self.train.v, 120, self.train.remaining_x, self.train.a_max)
      self.train.v = settings[0]
      self.train.remaining_x = self.length - 1000
      return settings[1]    
    elif self.state == "TrainIn":
      return 0  
    

  def outputFnc(self):
    #Output function
    if self.state == "TrainIn":
      return {self.CHANGECOL: "setred"}
    elif self.state == "Accel":
      return {self.CHANGECOL: "setgreen",
              self.TRAINOUT: self.train}
      
    elif self.state == "NextLight":
      return {self.QUERY: "query"}
    else:
      return {}


class railwaysegment(CoupledDEVS):
  #Class representing a railway section
  def __init__(self, name, l = 5000):
    #l = length of track
    CoupledDEVS.__init__(self, "system")
    self.light = self.addSubModel(light())
    self.railway = self.addSubModel(railway())

    self.QUERYRECV = self.addInPort(name="QUERYRECV")       #Query towards light
    self.QUERYACKRECV = self.addInPort(name="QUERYACKRECV") #Query Aknowledgement from next light
    self.TRAIN = self.addInPort(name="TRAIN")               #Train to railroad
    self.TRAINOUT = self.addOutPort(name="TRAINOUT")        #Train to next railroad
    self.QUERYACK = self.addOutPort(name="QUERYACK")        #Query Aknowledgement from light
    self.QUERYSEND = self.addOutPort(name="QUERYSEND")      #Query towards next railroad

    self.connectPorts(self.railway.CHANGECOL, self.light.CHANGECOL)
    self.connectPorts(self.QUERYRECV, self.light.QUERYRECV)
    self.connectPorts(self.light.QUERYACK, self.QUERYACK)
    self.connectPorts(self.QUERYACKRECV, self.railway.QUERYRECV)
    self.connectPorts(self.railway.QUERY, self.QUERYSEND)
    self.connectPorts(self.TRAIN, self.railway.TRAININ)
    self.connectPorts(self.railway.TRAINOUT, self.TRAINOUT)

