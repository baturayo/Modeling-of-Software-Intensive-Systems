class train:
  #Container class for train
  def __init__(self, id, amax, deptime):
    self.id = id            #Id will indicate that this is the nth train. This makes it unique
    self.a_max=amax         #Max acceleration allowed
    self.deptime = deptime  #Time at which this train departs

    self.v = 0              #Current speed
    self.remaining_x = 0    #Remaining distance on railwaytrack
