import urllib.request

class Urban_Dictionary:
   def __init__(self, word):
      self.word = word
      self.dict_base_url = 'http://www.urbandictionary.com/define.php?term='
      self.base_content = "property='og:description'>"
      self.counter = 0
	  
  # def convert_word(self):
     # self.word = self.word[0].upper() + self.word[1:]
	  
   def complete_url(self):
      complete_url = self.dict_base_url + self.word
      return complete_url
	  
   def read_full_content(self):
      return self.base_content + self.word
	  
   def read_string(self, complete_url, amt):
      request = urllib.request.urlopen(complete_url)
      string = request.read(int(amt))   
      return string
	  
   def convert_string(self, string):
      parse_string = ' '
      for letter in string:
         parse_string = parse_string + chr(letter)
      
      return parse_string		
   
   def print_def(self, parse_string, index):
      end_def = parse_string.find('.', index) - 1
      findex = parse_string.find("<meta content='1.", index) + 18
      definition = parse_string[findex:end_def]
      sentence = self.word + ' = ' + definition
      return sentence
   
   def parse_string(self):	   
      try:
         #self.convert_word()
         complete_url = self.complete_url()
         string = self.read_string(complete_url, 30000)
         parse_string = self.convert_string(string)
         print(parse_string)
        # print('\n\n\n\n??????????????????????????????????????????????????')
         parse_word = ' '
      
        # full_content = self.read_full_content()
		 
         for letter in parse_string:
            
            parse_word = parse_word + letter
            if parse_word == self.base_content:
               index = self.counter

            if letter == '\n' or letter == ' ':
               parse_word = ''
            self.counter = self.counter + 1
   
         index = index - 300
         sentence = self.print_def(parse_string, index)
         return sentence
   
      except urllib.error.HTTPError as error:
         sentence = "Word is misspelled"
         return "Word is misspelled or doesn't exist!"
		   
#obj = Urban_Dictionary('tilt')
#print(obj.parse_string())