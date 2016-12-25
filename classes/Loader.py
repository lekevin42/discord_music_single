class Loader:
	def __init__(self):
		self.memes = self.load_memes("files/load/memes.txt")
		self.joke_list = self.load_file("files/load/pick_up_lines.txt")
		self.cat_list = self.load_file("files/load/cats.txt")
		
	def get_memes(self):
		return self.memes
	
	def load_memes(self, file):
		"""Load a binary file."""
		list = []
		with open(file, "rb") as memes:
			for m in memes:
				list.append(m.decode('utf-8', "replace"))
				
		return list
		
	def load_file(self, file_name):
		stuff = []
	
		with open(file_name) as list:
			for line in list:
				stuff.append(line)
					
		return stuff