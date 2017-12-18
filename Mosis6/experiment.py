# Import code for model simulation:
from pypdevs.simulator import Simulator

# Import the model to be simulated
from TrainNetwork import *


#Initialize train here:
#TrainNetwork(name, numTracks, trackLength, numTrains, a, iat, vmax)
#Name = name
#numTracks = #lights (equivalent to #tracks)
#trackLength = length of a single track
#numTrains = The amount of trains to generate
#a = (a_min, a_max) -> tuple with range for amax for trains
#iat = (iat_min, iat_max) -> tuple with range for iat 
#vmax = maximum velocity, used in the formula's
#!!!!!!!Don't forget to set the correct terminate condition in the next segment!!!!!!!!!
trainnetwork = TrainNetwork('trainnetwork', 10, 2500, 100, iat = (10,20))
sim = Simulator(trainnetwork)

# 3. Perform all necessary configurations, the most commonly used are:

# A. Termination time (or termination condition)
#    Using a termination condition will execute a provided function at
#    every simulation step, making it possible to check for certain states
#    being reached.
#    It should return True to stop simulation, or Falso to continue.
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!Don't forget to set this!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def terminate_whenStateIsReached(clock, model):
    if model.collector.numTrains == 100:
      return True
    else:
      return False
sim.setTerminationCondition(terminate_whenStateIsReached)

#    A termination time is prefered over a termination condition,
#    as it is much simpler to use.
#    e.g. to simulate until simulation time 400.0 is reached
#sim.setTerminationTime(500.0)

# B. Set the use of a tracer to show what happened during the simulation run
#    Both writing to stdout or file is possible:
#    pass None for stdout, or a filename for writing to that file
sim.setVerbose(None)

# C. Use Classic DEVS instead of Parallel DEVS
#    If your model uses Classic DEVS, this configuration MUST be set as
#    otherwise errors are guaranteed to happen.
#    Without this option, events will be remapped and the select function
#    will never be called.
sim.setClassicDEVS()

#    ======================================================================

sim.simulate()
print(trainnetwork.getStatistics())
