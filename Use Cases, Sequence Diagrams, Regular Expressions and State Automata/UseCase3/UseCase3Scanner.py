from scanner import Scanner
import charstream

class Case3Scanner(Scanner):

  def __init__(self, stream):
  
    # superclass constructor
    Scanner.__init__(self, stream)

    # define accepting states
    self.accepting_states=["Init", "S2", "S3", "S4", "S5", "S6", "S7", "S8"]
   
   
  def transition(self, state, input):
   """
   Encodes transitions and actions
   """

   if state == None:
      # new state
      return "Init"
	  
   elif state == "Init":
    if input  == 'E':
      # new state
      return "S2"
    else:
      return "Init"

   elif state == "S2":
    if input == " ":
      # new state
      return "S3"
    else:
      return "Init"
	  
   elif state == "S3":
    if input == '3':
      # new state
      return "S4"
    else:
      return "Init"
	  
   elif state == "S4":
    if input == '\n':
       return "S5"
    else:
      return "Init"
	  
   elif state == "S5":
    if input == 'G':
      return "ERROR"
    elif input  == 'X':
      return "S6"
    else:
	  return "S5"

   elif state == "S6":
    if input == " ":
      # new state
      return "S7"
    else:
      return "S5"
	
   elif state == "S7":
    if input == '3':
      # new state
      return "S8"
    else:
      return "S5"
	  
   elif state == "S8":
    if input == '\n':
      # new state
      return "Init"
    else:
      return "S5"
	  
   elif state == "ERROR":
    return "ERROR"
	  
   else:
	return None
	  
	  
  def entry(self, state, input):
    pass
	
def main():
  f = open("trace.txt", 'r')
  #f = open("FaultiveTrace.txt", 'r')
  inputstring = f.read()
  stream = charstream.CharacterStream(inputstring)
  scanner = Case3Scanner(stream)
  result = scanner.scan()
  if result:
    print ">> Correct "
    stream.commit()
  else:
    print ">> Violation"

  
if __name__ == "__main__":
  main()
