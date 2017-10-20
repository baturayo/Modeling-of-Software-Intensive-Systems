
class CharacterStream:

 def __init__(self, str):
  self.str = str
  self.last_ptr    = -1
  self.current_ptr = self.last_ptr

 def isEndOfStream(self):
  return self.current_ptr >= len(self.str)-1
  # works for empty string

 def showNextChar(self):
  if self.isEndOfStream():
   return None
  else:
   return self.str[self.current_ptr+1]

 def getNextChar(self):
  if self.isEndOfStream():
   return None
  else:
   self.current_ptr+=1
   return self.str[self.current_ptr]

 def commit(self):
  self.last_ptr=self.current_ptr

 def rollback(self):
  self.current_ptr=self.last_ptr
  
 def __str__(self):
  return  "stream : "+self.str+"\n"+\
          "last   :"+" "*(self.last_ptr+1)+"^\n"+\
          "current:"+" "*(self.current_ptr+1)+"^"

