import asyncio
import youtube_dl
from classes.Extract_Playlist import *
from parsers.parser import *
from queue import *
from classes.Playlist import *

class Entry:
	def __init__(self, player, channel, title, url):
		self.player = player
		self.channel = channel
		self.title = title
		self.url = url
		

class Music:
	def __init__(self, bot):
		self.bot = bot
		self.play_list = asyncio.Queue()
		self.play_next_song = asyncio.Event()
		self.playlist = Playlist(bot)
		self.ydl_opts = None
		self.rec_songs = False
		self.rec_list = []
		self.current = None
		self.audio_player = self.bot.loop.create_task(self.audio_player_task())
		self.found = False
		self.max = 1
	
	async def audio_player_task(self):
		while True:
			self.play_next_song.clear()
			self.current = await self.play_list.get()
			await self.bot.send_message(self.current.channel, "```Now playing: {}```".format(str(self.current.title)))
			self.current.player.start()
			
			while self.rec_songs and not self.found:
				next_url, self.max = crawl_rec(self.current.url, self.max)
				if self.rec_list.count(next_url) is 0:
					self.found = True
					await self.add(self.current.channel, next_url)
					self.rec_list.append(next_url)

			self.found = False
			self.max = 1	
			await self.play_next_song.wait()

		
	def toggle_next_song(self):
		self.bot.loop.call_soon_threadsafe(self.play_next_song.set)

		
	def is_playing(self):
		if self.current is None:
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
		if self.is_playing():
			self.current.player.pause()
	
	
	def resume(self):
		if self.is_playing():
			self.current.player.resume()
	
	
	async def skip(self, channel):
		if self.is_playing():
			self.current.player.stop()
			self.current = None

			
	async def clear(self, channel):
		if self.is_playing():
			self.current.player.stop()
		
		while not self.play_list.empty():
			await self.play_list.get()
				
		self.current = None
		await self.bot.send_message(channel, "```Queue has been cleared!```")
	
	
	async def shuffle(self, channel):
		playlist = []
		while not self.play_list.empty():
			song = await self.play_list.get()
			playlist.append(song)
		
		shuffle(playlist)
		
		for song in playlist:
			await self.play_list.put(song)
		
		await self.bot.send_message(channel, "```Queue has been shuffled.```")
	
	
	async def queue(self, channel):
		"""Look into which songs are queued currently."""
		save_queue = Queue()
		info_list = Queue()
		how_many = 0
		counter = 0
		msg = ""
			
		if not self.play_list.empty():
			while not self.play_list.empty():
				current = await self.play_list.get()
				title = current.title
				info_list.put(title)
				save_queue.put(current)
				
			length = int(info_list.qsize() / 10)
				
			while info_list.qsize() is not 0:
				song = info_list.get()
				await self.play_list.put(save_queue.get())
				msg += "{}\n".format(song)
					
				counter += 1
				
				msg, counter, how_many = await self.bot.print_songs(msg, channel, length, counter, how_many)
		else:
			await self.bot.send_message(channel, "```Queue is currently empty.```")
	
	
	async def play(self, channel, link):
		if self.current and self.rec_songs:
			await self.bot.send_message(channel, "```!rec mode is currently on! Turn !rec mode off or use !clear to queue a new song!```")
		
		await self.add(channel, link)
	
	
	async def set_music(self, song, channel):
		try:	
			player = await self.bot.voice.voice_state.create_ytdl_player(song, after=self.toggle_next_song)
			player.volume = 0.1
			info = self.get_info(song)
			
			entry = Entry(player, channel, info['title'], song)
			await self.play_list.put(entry)
			
		except Exception as error:
			print(error)
			
	async def add(self, channel, link):
		"""This function is used to decide what to add to the queue for playing."""	
		if link != "":
			"""link is an youtube playlist, extract individual songs and add to queue"""
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
			
			elif link.find(".txt") != -1:
				"""link is user created playlist, read from file and add to queue"""
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
			
			elif link.find("http") != -1:		
				"""link is a single youtube song, just add to queue"""
				
				info = self.get_info(link)
				if info == None:
					await self.bot.send_message(channel, "```Copyright Error! Try a different query!```")

				await self.set_music(link, channel)
				await self.bot.send_message(channel, "```Queued song: {0} in position {1}!```".format(info['title'], self.play_list.qsize()))
					
			else:
				"""if none of the above, link is a youtube query pass to beautifulsoup4 parser to get song and add to queue"""
				link += " lyrics"
				link = parse_yt(link)
				await self.add(channel, link)
					
		else:
			await self.bot.send_message(channel, "```!play is used to play songs, playlists, youtube playlists or queries!```")
			await self.bot.send_message(channel, "```Usage: !play <url/song/play_list/query>```")
			
			
	async def repeat_song(self, channel, amt):
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
	