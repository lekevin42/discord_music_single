import os
import youtube_dl

class Playlist:
	"""
	Class that manages user's playlists
	
	Parameters:
		1) bot - Allows the usage of the Discord API
	"""
	
	def __init__(self, bot):
		self.bot = bot
		self.author = None
		self.msg = self.set_message()
		self.file_path = "playlists/"
	
	
	def set_message(self):
		"""Set message that will be shown to users"""
		
		msg = "```!playlist is used to create playlists, add songs, remove songs, delete playlists, list playlists.\n\n\
1.  Create a playlist. \n\
2.  Add a song.\n\
3.  Delete a song.\n\
4.  Delete a playlist.\n\
5.  List all playlists.\n\
6.  Exit```"

		return msg
		
		
	def get_message(self):
		return self.msg
		
		
	def set_author(self, author):
		"""Set author to allow commands to be usable only for that person
		
		Parameters:
			1) author - authors id that the bot will respond to
		"""
		
		self.author = author
		
		
	def get_info(self, song):
		"""
		Call upon the youtube-dl library to obtain info about the song.
		
		Parameters:
			1) song - url containing the song
		"""
		
		ydl_opts = {
			'format': 'bestvideo+bestaudio/best',
			'quiet' : True,
		}
		
		try:
			with youtube_dl.YoutubeDL(ydl_opts) as ydl:
				result = ydl.extract_info(song, download=False)
		except:
			return "Copyright Error"
						
		return result
		
		
	async def create_playlist(self, channel):
		"""
		Function that will create a playlist for the user.
		
		Parameters:
			1) channel - send messages to this channel
		"""
		
		await self.bot.send_message(channel, "```What do you want to name your playlist?```")
		file_name = await self.bot.wait_for_message(author=self.author)
		file_name = file_name.content.strip()
		file_name += ".txt"
		
		#check to see if playlist name is already taken
		if os.path.isfile(self.file_path + file_name):
			await self.bot.send_message(channel, "```File {} already exists!```".format(file_name))
		else:
			os.system("cd {0} && touch {1}".format(self.file_path, file_name))
			await self.bot.send_message(channel, "```{} has been created.```".format(file_name))
	
	
	async def add_song(self, channel):
		"""Function that will add a song to a playlist for the user.
		
		Parameters:
			1) channel - send messages to this channel
		"""
		
		await self.bot.send_message(channel, "```What song do you want to add? (Please provide an url!)```")
		url = await self.bot.wait_for_message(author=self.author)
		url = url.content.strip()
		
		await self.bot.send_message(channel, "```What playlist do you want to add this song to?```")
		playlist = await self.bot.wait_for_message(author=self.author)
		playlist = playlist.content.strip()
		playlist += ".txt"
		
		msg = await self.list_append(playlist, url)		
		await self.bot.send_message(channel, msg)
		
		
	async def delete_song(self, channel):
		"""Function that will delete a song from a playlist.
		
		Parameters:
			1) channel - send messages to this channel
		"""
		await self.bot.send_message(channel, "```What song do you want to delete? (Please provide an url!)```")
		url = await self.bot.wait_for_message(author=self.author)
		url = url.content.strip()
		
		await self.bot.send_message(channel, "```What playlist do you want to remove this song from?```")
		playlist = await self.bot.wait_for_message(author=self.author)
		playlist = playlist.content.strip()
		playlist += ".txt"
		
		msg = await self.delete(playlist, url)
		await self.bot.send_message(channel, "```{}```".format(msg))
		
		
	async def delete_playlist(self, channel):
		"""Function that will delete an entire playlist for a user.
		
		Parameters:
			1) channel - send messages to this channel
		"""
		
		await self.bot.send_message(channel, "```What playlist do you want to remove?```")
		file_name = await self.bot.wait_for_message(author=self.author)
		file_name = file_name.content.strip()
		file_name += ".txt"
		
		os.system("cd playlists/ && rm {}".format(file_name))
		await self.bot.send_message(channel, "```{} has been removed```".format(file_name))
		
	async def list_all(self, channel):
		"""Function that will list all the playlists.
		
		Parameters:
			1) channel - send messages to this channel
		"""
		
		list = os.listdir(self.file_path)
		for file in list:
			await self.bot.send_message(channel, "```{}```".format(file))
			
	async def list_append(self, file, song_link):
		"""function to append a song to a user created list"""
		first_time = False
		try:
			#Decide if user's playlist is empty
			if os.path.getsize(self.file_path + file) is 0:
				first_time = True
	
			if song_link.find("list=") is not -1:
				#if the user wants to add a list, extract the individual songs and add to playlist
				playlist = Extract(song_link)
				list = playlist.check()
				
				with open(self.file_path + file, 'a') as playlist:
					for song in list:
						if first_time:
							playlist.write(song)
							first_time = False
						else:
							playlist.write("\n")
							playlist.write(song)
									
				return "```You have successfully appended your playlist to {}!```".format(file)
												
			else:
				#otherwise add the single song to the playlist	
				with open(self.file_path + file, 'a') as list:
					if first_time:
						list.write(song_link)
						first_time = False
					else:
						list.write('\n')
						list.write(song_link)
				return "```You have successfully appended song {0} to {1}!```".format(song_link, file)
	
		except FileNotFoundError:
			return "File {} not found.".format(file)
			
	async def delete(self, file, song_link):
		"""Generic function used to delete a line from a text file.
		
		
		Parameters:
			1) file - txt file to edit
			2) song_link - link to be deleted from said file
		"""
		
		url_list = []
		counter = 0
		
		try:
			#Gather all other urls into a list
			with open(self.file_path + file, "r") as list:
				for url in list:
					url = url.strip()
					if url.find(song_link) is -1:
						url_list.append(url)
			
			#Save back into the user's playlist
			with open(self.file_path + file, "w") as list:
				for url in url_list:
					list.write(url)
					counter += 1
					
					if counter != len(url_list):
						list.write("\n")
								
			return "Successfully deleted {0} from {1}!".format(song_link, file)
		
		except FileNotFoundError:
			return "File {} not found.".format(file)
	
	async def playlist_info(self, playlist, channel):
		"""Get the titles of songs of a playlist.
		
		Parameters:
			1) playlist - the txt file to look at
			2) channel - send message to this text channel
		"""
		
		info_list = []
		msg = ""
		counter = 0
		how_many = 0
		
		if playlist is not "":
			playlist += ".txt"
			with open(self.file_path + playlist, 'r') as list:
				for song in list:
					info = self.get_info(song)
					info_list.append(info['title'])
					
			for song in info_list:
				length = math.floor(len(info_list) / 10)
				msg += "{}\n".format(song)
				counter += 1
			
				if counter == 10 and how_many < length:
					await self.bot.send_message(channel, "`{}`".format(msg))
					counter = 0
					msg = ""
					how_many += 1
				
				elif how_many == length:
					msg = song
					await self.bot.send_message(channel, "`{}`".format(msg))
					msg = ""

		else:	
			await self.bot.send_message(channel, "```This command is used to see what songs are in a playlist.```")
			await self.bot.send_message(channel, "```!info <playlist>```")