from CBDMultipleOutput.Source.CBD import *
from CBD_assignment_startingpoint.DiverlessTrain import DriverlessTrain



trainsim = DriverlessTrain("Train")

trainsim.run(3500)
print(trainsim.getSignal("cost")[-1])