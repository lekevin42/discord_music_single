import asyncio
import youtube_dl
import discord
from classes.Extract_Playlist import *
from parsers.parser import *
from queue import *
from classes.Playlist import *

class Entry:
	"""
	Container for song when it is queued.
	
	Parameters:
		1) song - url for the given song
		2) channel - text channel to send message to
		3) title - title of the song
	"""
	
	def __init__(self, song, channel, title):
		self.song = song
		self.channel = channel
		self.title = title
		

class Music:
	"""
	Class that handles all of the bot's musical commands.
	
	Parameters:
		1) bot - the actual bot itself, allows for the usage of unique Discord API commands
	"""
	
	def __init__(self, bot):
		self.bot = bot
		self.play_list = asyncio.Queue()
		self.play_next_song = asyncio.Event()
		self.playlist = Playlist(bot)
		self.ydl_opts = None
		self.rec_songs = False
		self.rec_list = []
		self.entry = None
		self.player = None
		self.audio_player = None
		self.found = False
		self.max = 1
		
	def cancel_player(self):
		"""Cancel the music player when it is no longer required."""
		
		self.player = None
		
		
	async def init_audio(self):
		"""Function that creates a music player task to handle song requests."""
		
		self.audio_player = self.bot.loop.create_task(self.audio_player_task())
	
	async def audio_player_task(self):
		"""Construct a task that will create a ytdl player when given a song and play it for the voice channel."""
		
		try:
			#Attempt to play music for as long as program is running and queue is not empty.
			while True:
				#Empty the next song
				self.play_next_song.clear()
				
				#Grab the entry
				self.entry = await self.play_list.get()
				
				#Use the voice client connection in order to create a ytdl player that will play audio
				self.player = await self.bot.voice.voice_state.create_ytdl_player(self.entry.song, after=self.toggle_next_song)
				self.player.volume = 0.1
				
				#Display a playing message for the current song and start the player.
				await self.bot.send_message(self.entry.channel, "```Now playing: {}```".format(str(self.entry.title)))
				self.player.start()
				
				#If rec mode is on, query youtube for a recommended song and place it into the queue.
				while self.rec_songs and not self.found:
					next_url, self.max = crawl_rec(self.entry.song, self.max)
					if self.rec_list.count(next_url) is 0:
						self.found = True
						await self.add(self.entry.channel, next_url)
						self.rec_list.append(next_url)

				self.found = False
				self.max = 1	
				await self.play_next_song.wait()
					
		
		except discord.ConnectionClosed as cError:
			print("Connection closed: {}".format(cError))

		except discord.GatewayNotFound as gError:
			print("Connection closed: {}".format(cError))
		
		
	def toggle_next_song(self):
		"""Grab the next song for the bot to play if there is one."""
		
		self.bot.loop.call_soon_threadsafe(self.play_next_song.set)

		
	def is_playing(self):
		"""Check to see if a song is currently playing."""
		
		if self.player is None:
			return False
		
		return True
	
	
	def set_ydl_opts(self):
		"""Set youtube dl options when extracting audio for the player."""
		
		self.ydl_opts = {
			'format': 'bestvideo+bestaudio/best',
			'quiet' : True,
		}
	
	
	def get_info(self, song):
		"""Call upon the youtube-dl library to obtain info about the song."""
		
		try:
			with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
				result = ydl.extract_info(song, download=False)
			
		except youtube_dl.utils.DownloadError as dlError:
			result = None
						
		return result
	
	
	def pause(self):
		"""Function that will pause the music player."""
		
		if self.is_playing():
			self.player.pause()
	
	
	def resume(self):
		"""Function that will resume the music player."""
		
		if self.is_playing():
			self.player.resume()
	
	
	async def skip(self, channel):
		"""Function that will stop the music player in order to skip the current song."""
		
		if self.is_playing():
			self.player.stop()
			self.player = None

			
	async def clear(self, channel):
		"""
		Function that clears the entire music queue.
		
		Parameters:
			1) channel - the text channel to send a clear message to
		"""
		
		if self.is_playing():
			self.player.stop()
		
		while not self.play_list.empty():
			await self.play_list.get()
				
		self.player = None
		await self.bot.send_message(channel, "```Queue has been cleared!```")
	
	
	async def shuffle(self, channel):
		"""
		Function that will shuffle the music queue for the user.
		
		Parameters:
			1) channel - the text channel to send a shuffle message to
		"""
		
		playlist = []
		while not self.play_list.empty():
			song = await self.play_list.get()
			playlist.append(song)
		
		shuffle(playlist)
		
		for song in playlist:
			await self.play_list.put(song)
		
		await self.bot.send_message(channel, "```Queue has been shuffled.```")
	
	
	async def queue(self, channel):
		"""Function that checks which songs are queued."""
		
		save_queue = Queue()
		info_list = Queue()
		how_many = 0
		counter = 0
		song_no = 1
		msg = ""
			
		#Empty the song queue and save it for future restoration
		if not self.play_list.empty():
			while not self.play_list.empty():
				current = await self.play_list.get()
				title = current.title
				info_list.put(title)
				save_queue.put(current)
				
			#Grab the length of the queue
			length = int(info_list.qsize() / 10)
				
			#Print the queue out and restore the songs
			while info_list.qsize() is not 0:
				song = info_list.get()
				await self.play_list.put(save_queue.get())
				msg += "{}. {}\n".format(song_no, song)
					
				counter += 1
				song_no += 1
				msg, counter, how_many = await self.bot.print_songs(msg, channel, length, counter, how_many)
		else:
			await self.bot.send_message(channel, "```Queue is currently empty.```")
	
	
	async def play(self, channel, link):
		"""Helper function that will call the add function to queue songs.
		
		Parameters:
			1) channel - Send a rec message just in case rec mode is on
			2) link - the song link to pass to the add function
		"""	
		
		#if rec mode is on do not queue the song
		if self.player and self.rec_songs:
			await self.bot.send_message(channel, "```!rec mode is currently on! Turn !rec mode off or use !clear to queue a new song!```")
		
		await self.add(channel, link)
	
	
	async def set_music(self, song, channel):
		"""Function that grabs the title of the song in order to create an Entry object to pass to audio task."""
		
		#Get title by parsing youtube
		info = self.get_info(song)
		if info is None:
			await self.bot.send_message(channel, "```{} is copyrighted, cannot queue!```".format(song))
			return
			
		#Create an entry object and place in queue
		entry = Entry(song, channel, info['title'])
		await self.play_list.put(entry)
			
		
	async def add(self, channel, link):
		"""This function is used to decide what to add to the queue for playing."""	
		
		#link is an youtube playlist, extract individual songs and add to queue
		if link != "":
			if link.find("list=") != -1:
				list = None
				playlist = Extract(link)
				list = playlist.check()
				
				if list is not None:
					shuffle(list)
					
					for song in list:
						await self.set_music(song, channel)
					await self.bot.send_message(channel, "```I have queued your youtube playlist!```")
					
				else:
					await self.bot.send_message(channel, "```Error parsing through list!```")
			
			#link is user created playlist, read from file and add to queue
			elif link.find(".txt") != -1:
				playList = []
				file = link
	
				try:
					with open(self.playlist.file_path + file) as list:
						for song in list:
							song = song.strip()
							playList.append(song)
							
					shuffle(playList)
					
					for song in playList:
						await self.set_music(song, channel)
					await self.bot.send_message(channel, "```I have queued {}!```".format(file))
				
				except FileNotFoundError:
					await self.bot.send_message(channel, "```File {} not found.```".format(file))
			
			#link is a single youtube song, just add to queue
			elif link.find("http") != -1:		
				info = self.get_info(link)
				if info is None:
					await self.bot.send_message(channel, "```This song is copyrighted, cannot queue!```")
					return

				await self.set_music(link, channel)
				await self.bot.send_message(channel, "```Queued song: {0} in position {1}!```".format(info['title'], self.play_list.qsize()))
			
			#if none of the above, link is a youtube query pass to beautifulsoup4 parser to get song and add to queue
			else:
				link += " lyrics"
				link = parse_yt(link)
				await self.add(channel, link)
					
		else:
			await self.bot.send_message(channel, "```!play is used to play songs, playlists, youtube playlists or queries!```")
			await self.bot.send_message(channel, "```Usage: !play <url/song/play_list/query>```")
			
			
	async def repeat_song(self, channel, amt):
		"""
		Function that allows a user to repeat the song an x amt of times
		
		Parameters:
			1) channel - message that informs user song is queued x times
			2) amt - the amount of times to queue the song
		"""
		
		if amt is not "":
			amt = int(amt)
			list = []
			counter = 0
			
			while not self.play_list.empty():
				song = await self.play_list.get()
				list.append(song)
					
			while counter < amt:
				await self.play_list.put(self.song)
				counter += 1
				
			while len(list) != 0:
				await self.play_list.put(list.pop())
				
			await self.bot.send_message(channel, "Song {0} is going to be repeated an additional {1} times!".format(self.song, amt))
				
		else:
			await self.bot.send_message(channel, "```!rep is used to repeat the current song x amt of times```")
			await self.bot.send_message(channel, "```Usage: !rep <amt>```")
	
	
	async def rec_option(self, channel, option):
		"""Function that controls rec mode.
		Rec mode queues songs automatically and disables querying of songs by users.
		
		Parameters:
			1) channel - send message to user to notify user.
			2) option - turn on or off
		"""
		
		if option is not "":
			option = option.strip()
			option = option.lower()
		
			if option == "on":
				self.rec_songs = True
				await self.bot.send_message(channel, "```Automatic queuing of youtube songs has been turned on!```")
				
			elif option == "off":
				self.rec_songs = False
				self.rec_list.clear()
				await self.bot.send_message(channel, "```Automatic queuing of youtube songs has been turned off!```")
					
		else:
			msg = "```The !rec command is used to turn on automatic queueing of youtube songs!  This option is currently {}!```".format(self.rec_songs)
			await self.bot.send_message(channel, msg)
	