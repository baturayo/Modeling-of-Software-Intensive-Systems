from scanner import Scanner
import charstream

class Case3Scanner(Scanner):

  def __init__(self, stream):
  
    # superclass constructor
    Scanner.__init__(self, stream)

    # define accepting states
    self.accepting_states=["S3"]
   
   
  def transition(self, state, input):
   """
   Encodes transitions and actions
   """

   if state == None:
      # new state
      return "S1"
   elif state == "S1":
    if input  == '.':
      # new state
      return "S3"
    elif '0' <= input <= '9':
      # new state
      return "S1"
    else:
      return None

   elif state == "S2":
    if '0' <= input <= '9':
      # new state
      return "S2"
    elif string.lower(input)  == 'e':
      # action
      self.exp = 1
      # new state
      return "S5"
    else:
      return None

   elif state == "S3":
    if '0' <= input <= '9':
      # new state
      return "S3"
    else:
      return None

   else:
    return None
	
  def entry(self, state, input):
    pass
	
def main():
  stream = charstream.CharacterStream("123.456")
  scanner = Case3Scanner(stream)
  result = scanner.scan()
  if result:
    print ">> recognized " + stream.__str__()
    print ">> committing"
    stream.commit()
  else:
    print ">> rejected"

  
if __name__ == "__main__":
  main()