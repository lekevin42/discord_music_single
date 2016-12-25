import urllib.request

class Web_Parser:
	def __init__(self, word, base_url, end_url, base_content):
		self.word = word
		self.dict_base_url = base_url
		self.end_url = end_url
		self.base_content = base_content
		self.counter = 0
	  
	def convert_word(self):
		self.word = self.word[0].upper() + self.word[1:]
	  
	def complete_url(self):
		complete_url = self.dict_base_url + self.word + self.end_url
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
		end_def = parse_string.find('.', index) + 1
		definition = parse_string[index:end_def]
		sentence = self.word + ' = ' + definition
		return sentence

	def find_index(self, parse_string, full_content):
		index = None
		parse_word = ' '
		for letter in parse_string:
			parse_word = parse_word + letter
			if parse_word == full_content:
				index = self.counter

			if letter == " ":
				parse_word = ''
			self.counter = self.counter + 1
		
		if index is not None:
			index = index + 13
		
		return index
		 