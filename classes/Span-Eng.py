import urllib.request

class Spanish_To_English:
   def __init__(self, word):
      self.word = word
      self.dict_base_url = 'http://translate.google.com/#es/en/'
      self.base_content = "<meta content='1."
      self.counter = 0
	    
   def complete_url(self):
      complete_url = self.dict_base_url + self.word
      return complete_url
	  
   def read_full_content(self):
      return self.base_content + self.word
	  
   def read_string(self, complete_url, amt):
      request = urllib.request.urlopen(complete_url, headers={'User-Agent':'Mozilla/5.0'})
      f = request.read()
      print("?")
      string = request.read(int(amt))   
      print("STRING:" + string)
      return string
	  
   def convert_string(self, string):
      parse_string = ' '
      for letter in string:
         parse_string = parse_string + chr(letter)
         print(letter)
      
      return parse_string		
   
   def print_def(self, parse_string, index):
      end_def = parse_string.find('.', index) + 1
      definition = parse_string[index:end_def]
      sentence = self.word + ' = ' + definition
      return sentence
   
   def parse_string(self):	   
#      try:
         #self.convert_word()
         complete_url = self.complete_url()
         print(complete_url)
         print(self.word)
         string = self.read_string(complete_url, 30000)
         print(string)
         parse_string = self.convert_string(string)
         print(parse_string)
         parse_word = ' '
      
         full_content = self.read_full_content()
		 
         for letter in parse_string:
            
            parse_word = parse_word + letter
            if parse_word == full_content:
               index = self.counter

            if letter == " ":
               parse_word = ''
            self.counter = self.counter + 1
   
         index = index + 13
         sentence = self.print_def(parse_string, index)
         return sentence
   
#      except urllib.error.HTTPError as error:
#         return "Word is misspelled or doesn't exist!"
	  

test = Spanish_To_English('amigo')
w = test.parse_string()
print(w)