import os

class Response:
	def __init__(self, bot):
		self.bot = bot
		self.path = "files/load/responses.txt"
		self.commands, self.responses = self.load_responses()
		self.message = self.set_message()
		self.author = None
		
	def get_commands(self):
		return self.commands
		
	def get_responses(self):
		return self.responses
		
	def set_message(self):
		message = "!response is used to create, delete and list responses.\n\n\
Options Available:\n \
1.  Create a new response\n \
2.  Delete responses \n \
3.  List responses \n \
4.  Exit"
		return message

	def get_message(self):
		return self.message
		
	def set_author(self, author):
		self.author = author
		
	def load_responses(self):
		command_list = []
		responses_list = []
		with open(self.path, "rb") as responses:
			for response in responses:
				sep = response.find('|'.encode('utf-8'))
				
				command_list.append(response[0:sep - 1].decode('utf-8'))
				responses_list.append(response[sep + 2:].decode('utf-8'))
				
		return command_list, responses_list
		
	async def create_response(self, channel):
		first_time = False
				
		if os.path.getsize(self.path) is 0:
			first_time = True
		
		await self.bot.send_message(channel, "```What do you want to name your command?```")
		
		cmd = await self.bot.wait_for_message(author=self.author)
		
		cmd = cmd.content
		
		await self.bot.send_message(channel, "```What do you want your response to be?```")
		
		response = await self.bot.wait_for_message(author=self.author)
		
		response = response.content
		
		if cmd is not None and response is not None:
			with open(self.path, "ab") as responses:
				if first_time:
					r = "{} | {}".format(cmd, response)
					r = r.encode('utf-8')
					responses.write(r)
					first_time = False
				else:
					r = "{} | {}".format(cmd, response)
					responses.write(("\n" + r).encode('utf-8'))
				
			while len(self.commands) != 0:
				self.commands.pop()
				self.responses.pop()
				
			self.commands, self.responses = self.load_responses()
			
			await self.bot.send_message(channel, "```Command {} has been created!```".format(cmd))
			
		else:
			await self.bot.send_message(channel, "```Command or response has been left blank.```")
			
			
	async def delete_response(self, channel):
		await self.bot.send_message(channel, "```What command do you want to delete?```")
				
		cmd = await self.bot.wait_for_message(author=self.author)
		
		cmd = cmd.content
		
		list = []
		counter = 0
		found = False
		
		if found == False:
			with open(self.path, "rb") as responses:
				for response in responses:
					sep = response.find("|".encode('utf-8'))
					
					if response[0: sep - 1].decode('utf-8') != cmd:
						list.append(response.strip())
						
					if response[0: sep - 1].decode('utf-8') == cmd:
						found = True
						
		
		if found == True:			
			with open(self.path, "wb") as responses:
				for response in list:
					responses.write(response)
					counter += 1
					
					if counter != len(list):
						responses.write("\n".encode('utf-8'))
			
			await self.bot.send_message(channel, "```{}```".format(msg))
			
		else:
			await self.bot.send_message(channel, "```{} has not been found!```".format(cmd))
			
			
	async def print_responses(self, channel):
		how_many = 0
		counter = 0
		msg = ""
		response_list = []
		
		with open(self.path, "rb") as responses:
			for response in responses:
				sep = response.find("|".encode('utf-8'))
				response_list.append(response[0:sep - 1].decode('utf-8'))
				
		length = len(response_list)
		
		await self.bot.send_message(channel, "```These commands are available:\n```")
		while length is not 0:
			response = response_list.pop(0)
			msg += "{}\n".format(response)
				
			counter += 1
				
			msg, counter, how_many = await self.bot.print_songs(msg, channel, length, counter, how_many)
			length -= 1