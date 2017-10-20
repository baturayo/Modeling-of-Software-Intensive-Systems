#
# scanner.py
#
# COMP 304B Assignment 3
#
import string

False = 0
True  = 1

# trace FSA dynamics (True | False)
__trace__ = False 
#__trace__ = True 

class Scanner:
 """
  A simple Finite State Automaton simulator.
  Used for scanning an input stream.
 """
 def __init__(self, stream):
  self.set_stream(stream)
  self.current_state=None
  self.accepting_states=[]

 def set_stream(self, stream):
  self.stream = stream

 def scan(self):

  self.current_state=self.transition(self.current_state, None)

  if __trace__:
    print "\ndefault transition --> "+self.current_state

  while 1:
    # look ahead at the next character in the input stream
    next_char = self.stream.showNextChar()

    # stop if this is the end of the input stream
    if next_char == None: break

    if __trace__:
      print str(self.stream)
      if self.current_state != None:
        print "transition "+self.current_state+" -| "+next_char,
   
    # perform transition and its action to the appropriate new state 
    next_state = self.transition(self.current_state, next_char)

    if __trace__:
      if next_state == None: 
        print
      else:
        print "|-> "+next_state
    

    # stop if a transition was not possible
    if next_state == None: 
      break
    else:
      self.current_state = next_state
      # perform the new state's entry action (if any)
      self.entry(self.current_state, next_char)

    # now, actually consume the next character in the input stream 
    next_char = self.stream.getNextChar()

  if __trace__:
    print str(self.stream)+"\n"

  # now check whether to accept consumed characters
  success = self.current_state in self.accepting_states
  if success:
   self.stream.commit()
  else:
   self.stream.rollback()
  return success

## An example scanner, see http://moncs.cs.mcgill.ca/people/hv/teaching/SoftwareDesign/COMP304B2003/assignments/assignment3/solution/
class NumberScanner(Scanner):

 def __init__(self, stream):
  
   # superclass constructor
   Scanner.__init__(self, stream)

   # define accepting states
   self.accepting_states=["S2","S4","S7"]

 def __str__(self):
  
   return str(self.value)+"E"+str(self.exp)


 def transition(self, state, input):
   """
   Encodes transitions and actions
   """

   if state == None:
      # action
      # initialize variables 
      self.value = 0 
      self.exp = 0
      # new state
      return "S1"

   elif state == "S1":
    if input  == '.':
      # action
      self.scale = 0.1
      # new state
      return "S3"
    elif '0' <= input <= '9':
      # action
      self.value = ord(string.lower(input))-ord('0')
      # new state
      return "S2"
    else:
      return None

   elif state == "S2":
    if input  == '.':
      # action
      self.scale = 0.1
      # new state
      return "S4"
    elif '0' <= input <= '9':
      # action
      self.value = self.value*10+ord(string.lower(input))-ord('0')
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
      # action
      self.value += self.scale*(ord(string.lower(input))-ord('0'))
      self.scale /= 10
      # new state
      return "S4"
    else:
      return None

   elif state == "S4":
    if '0' <= input <= '9':
      # action
      self.value += self.scale*(ord(string.lower(input))-ord('0'))
      self.scale /= 10
      # new state
      return "S4"
    elif string.lower(input)  == 'e':
      # action
      self.exp = 1
      # new state
      return "S5"
    else:
      return None

   elif state == "S5":
    if   input  == '+':
      # new state
      return "S6"
    elif input  == '-':
      # action
      self.exp = -1
      # new state
      return "S6"
    elif '0' <= input <= '9':
      # action
      self.exp *= ord(string.lower(input))-ord('0')
      # new state
      return "S7"
    else:
      return None

   elif state == "S6":
    if '0' <= input <= '9':
      # action
      self.exp *= ord(string.lower(input))-ord('0')
      # new state
      return "S7"
    else:
      return None

   elif state == "S7":
    if '0' <= input <= '9':
      # action
      self.exp = self.exp*10+ord(string.lower(input))-ord('0')
      # new state
      return "S7"
    else:
      return None

   else:
    return None

 def entry(self, state, input):

   pass
