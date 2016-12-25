class Random_Object:
   def __init__(self, list, length):
      self.list = list
      self.length = length

class Cat_Object(Random_Object):
   def __init__(self, list, length):
      super().__init__(list, length)
	  
class Joke_Object(Random_Object):
   def __init__(self, list, length):
      super().__init__(list,length)