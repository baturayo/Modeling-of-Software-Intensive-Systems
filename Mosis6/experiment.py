# Import code for model simulation:
from pypdevs.simulator import Simulator

# Import the model to be simulated
from TrainNetwork import *

trainnetwork = TrainNetwork('trainnetwork')
sim = Simulator(trainnetwork)

# 3. Perform all necessary configurations, the most commonly used are:

# A. Termination time (or termination condition)
#    Using a termination condition will execute a provided function at
#    every simulation step, making it possible to check for certain states
#    being reached.
#    It should return True to stop simulation, or Falso to continue.
def terminate_whenStateIsReached(clock, model):
    return len(model.generator.queue) == 0
sim.setTerminationCondition(terminate_whenStateIsReached)

#    A termination time is prefered over a termination condition,
#    as it is much simpler to use.
#    e.g. to simulate until simulation time 400.0 is reached
#sim.setTerminationTime(400.0)

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
