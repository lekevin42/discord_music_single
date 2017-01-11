# -*- coding: utf-8 -*-

import asyncio
import discord
from queue import *
import os
import sys
import math
import signal
from random import *

from misc.utils import *
from misc.help import *

from classes.Battle_Royale.Battle_Royale import *
from classes.Math import *
from classes.Music import *
from classes.Voice import *
from classes.Loader import *
from classes.Response import *

from parsers.parser import *

if not discord.opus.is_loaded():
	discord.opus.load_opus('libopus-0.dll')

class Bot(discord.Client):
	def __init__(self):
		super().__init__()
		self.music = Music(self)
		self.voice = Voice(self)
		self.loader = Loader()
		self.BR = Battle_Royale()
		self.response = Response(self)
		self.default_text_channel = None
		self.default_voice_channel = None
		self.pid = os.getpid()
        		
			
	def grab_spawn(self):
		"""Get info about the server and channels and save it to a text file, so the bot will spawn back into that server and channel."""
		with open("default_channels.txt", "r") as channels:
			server = channels.readline().strip()
			text_channel = channels.readline().strip()
			voice_channel = channels.readline().strip()
		
		"""Use the utils function given by Discord to turn the string types from the text file back into Discord channel types to use."""
		text_channel = discord.utils.get(self.get_all_channels(), server__name = server, name = text_channel)
		voice_channel = discord.utils.get(self.get_all_channels(), server__name = server, name = voice_channel)
		
		return text_channel, voice_channel
		
	async def print_songs(self, msg, channel, length, counter, how_many):
		"""Generic function to display a set amount of messages to avoid maximum text limit.
			Default is 10 max."""
		if counter == 10 and how_many < length:
			await self.send_message(channel, "```{}``` ".format(msg))
			counter = 0
			msg = ""
			how_many += 1
			return msg, counter, how_many
						
		elif how_many == length:
			await self.send_message(channel, "```{}```".format(msg))
			msg = ""
			return msg, counter, how_many
			
		return msg, counter, how_many
		
	async def save_songs(self):
		"""When the bot crashes or usage of !restart occurs, save the songs that are in the queue to a text file and save rec mode."""
		first_line = True
		with open("save_songs.txt", "w") as songs:
			while not self.music.play_list.empty():
				song = await self.music.play_list.get()
				if not first_line:
					songs.write("\n")
				songs.write(song)
				first_line = False
				
		with open("options.txt", "w") as options:
			if self.music.rec_songs:
				s = "on"
			else:
				s = "off"
			options.write(s)
			
		first = True
		with open("rec_songs.txt", "w") as rec_songs:
			for url in self.music.rec_list:
				if first:
					rec_songs.write("{}".format(url))
					first = False
				else:
					rec_songs.write("\n{}".format(url))
				
	
	async def check_music(self):
		"""Check to see if there are songs inside the file and put back into the queue.  Also check for the default rec mode."""
		with open("save_songs.txt", "r") as songs:
			for song in songs:
				song = song.strip()
				await self.music.play_list.put(song)
		
		with open("save_songs.txt", "w") as songs:
			songs.write("")
			
		with open("options.txt", "r") as options:
			s = options.readline()
			s = s.strip()
			
			if s == "on":
				self.music.rec_songs = True
				
			else:
				self.music.rec_songs = False
			
			
		with open("options.txt", "w") as options:
			options.write("")
			
		with open("rec_songs.txt", "r") as rec_songs:
			for url in rec_songs:
				url = url.strip()
				self.music.rec_list.append(url)
				
		with open("rec_songs.txt", "w") as rec_songs:
			rec_songs.write("")
		
		if not self.music.play_list.empty():
			return "```Continuing to play songs from where I left off!```"
		
		return None
				
	def get_duration(self, duration):
		minutes = math.floor(duration / 60)
		seconds = duration % 60
		format = "{}:{}".format(minutes, seconds)
		return format
	
					
	async def repeat_short_yt(self, amt, song):
		counter = 0
		
		if amt is not "":
			amt = int(amt)
				
			if not self.is_playing():
				while counter < amt:
					await self.play_list.put(song)
					counter += 1
				
			else:
				return "```Currently playing music.```"
		
		else:
			return "`Usage: !cmd <amt>`"
		
	def start_battle(self):
		s=""
		day_one = True
		BR = Battle_Royale()
		BR.m_game()
		day = BR.get_days()
		
		return day
		
	async def read_battle(self, channel, day):
		s = ""

		with open("classes/Battle_Royale/story.txt", 'r') as story:
			for char in story:
				if char.find("End") is not -1 and not day_one:
					await self.send_message(channel, s)
					s = ""
					
				day_one = False	
				s += char
			
				if char.find(day) is not -1:
					await self.send_message(channel, s)
		
	async def on_message(self, message):
		if message.author == self.user:
			return

		elif message.content.startswith("!quit"):
			print("KILLING PROCESS {}".format(self.pid))
			self.send_message(message.channel, "Good Bye!")
			os.kill(self.pid, signal.SIGTERM)
		
		elif message.content.startswith("!pic"):
			pic_url = message.content[5:]
			self.edit_profile("nightblade44", avatar=pic_url)
			await self.send_message(message.channel, "```Changing picture!```")
		
		elif message.content.startswith("!spawn"):
			"""Spawn function saves the server and channels used, so the bot can respawn at that point if it crashes or is restarted."""
			with open("default_channels.txt", "w") as channels:
				channels.write(str(message.server))
				channels.write("\n" + str(message.channel.name))
				if self.voice.voice_channel is not None:
					channels.write("\n" + str(self.voice.voice_channel))
					await self.send_message(message.channel, "```Spawn point is set at {} and {}!```".format(message.channel.name, self.voice.voice_channel))
				else:
					await self.send_message(message.channel, "```Spawn point is set at {}!```".format(message.channel.name))
				
		elif message.content.startswith('!dict'):
			"""Use the dictionary parser to obtain a definition from https://www.dictionary.com"""
			word = message.content[6:]
			defined_word = parse_dict(word)
			await self.send_message(message.channel, "```{}```".format(defined_word))
			
		elif message.content.startswith('!udict'):
			"""Use the urban dictionary parser to obtain a definition from https://www.urbandictionary.com"""
			word = message.content[7:]
			defined_word = parse_urban(word)
			await self.send_message(message.channel, "```{}```".format(defined_word))
			
		elif message.content.startswith('!python'):
			msg = python_help()
			await self.send_message(message.channel, msg)

		elif message.content.startswith('!terminal'):
			msg = terminal_help()
			await self.send_message(message.channel, msg)
	
		elif message.content.startswith("!roll"): 
			member_list = []
			word_list = ["TBH", "100%", "Obviously", "Apparently"]
			for member in message.server.members:
				if str(member.status) == "online":
					member_list.append(member.name)
			
			if len(member_list) != 0:
				member_rand = randint(0, len(member_list) - 1)
				word_rand = randint(0, len(word_list) - 1)
				
				await self.send_message(message.channel, "```{}```".format(word_list[word_rand]))
				await self.send_message(message.channel, "```{}```".format(member_list[member_rand]))
			
		
		elif message.content.startswith("!meme"):
			"""Get a random meme from a list and send it to chat."""
			
			rand = randint(0, len(self.loader.get_memes()))
			await self.send_message(message.channel, self.loader.get_memes()[rand])
		
		elif message.content.startswith("!8ball"):
			"""Ask the magic 8 ball, responds with yes or no."""
			msg = magic_ball()
			await self.send_message(message.channel, msg)
			
		elif message.content.startswith("!avatar"):
			"""Given a username, use discord utilities functions to get a person's profile picture"""
			person = message.content[8:]
			person = discord.utils.get(message.server.members, name = person)
			if person is not None:
				await self.send_message(message.channel, person.avatar_url)
			else:
				await self.send_message(message.channel, "```Invalid Person!```")
		
		elif message.content.startswith("!battle"):
			day = self.start_battle()
			await self.read_battle(message.channel, day)

		elif message.content.startswith('!restart'):
			"""Restart the bot."""
			await self.send_message(message.channel, "```Restarting...```")
			await self.save_songs()
			os.execv(sys.executable, [sys.executable] + sys.argv)
		
		elif message.content.startswith("!rec"):
			"""Given the option "on" or "off", turn on or off automatic queuing of youtube songs."""
			option = message.content[5:]
			await self.music.rec_option(message.channel, option)
				
		elif message.content.startswith('!queue'):
			await self.music.queue(message.channel)
					
		elif message.content.startswith("!playlist"):
			d_author = message.author
			self.music.playlist.set_author(d_author)
			
			await self.send_message(message.channel, self.music.playlist.get_message())
			
			option = await self.wait_for_message(author=d_author)
			
			option = option.content.strip()
			
			if option == "1":
				await self.music.playlist.create_playlist(message.channel)
				
			elif option == "2":
				await self.music.playlist.add_song(message.channel)

			elif option == "3":
				await self.music.playlist.delete_song(message.channel)
									
			elif option == "4":
				await self.music.playlist.delete_playlist(message.channel)
					
			elif option == "5":
				await self.music.playlist.list_all(message.channel)
				
			elif option == "6":
				await self.send_message(message.channel, "```Exited Successfully!```")
			
		elif message.content.startswith('!shuffle'):
			await self.music.shuffle(message.channel)
			
		elif message.content.startswith('!info'):
			playlist = message.content[6:].strip()
			await self.music.playlist.playlist_info(playlist, message.channel)
											
		elif message.content.startswith('!join'):
			await self.voice.join_channel(message.server, message.channel, message.content)

		elif message.content.startswith('!clear'):
			await self.music.clear(message.channel)
			
		elif message.content.startswith('!help'):
			"""Print a help message."""
			msg = general_help()
			await self.send_message(message.channel, msg)
			
		elif message.content.startswith('!leave'):
			"""Leave the voice channel."""
			while not self.music.play_list.empty():
				await self.music.play_list.get()
				
			self.music.cancel_player()
			
			await self.voice.leave_channel(message.channel)
			
		elif message.content.startswith('!pause'):
			self.music.pause()
				
		elif message.content.startswith('!resume'):
			self.music.resume()
				
		elif message.content.startswith('!skip'):
			await self.music.skip(message.channel)
	
		elif message.content.startswith('!play'):
			"""Given a url/song/play_list/query, play that song."""
			if not self.is_voice_connected(message.server):
				await self.send_message(message.channel, '```Not connected to a voice channel```')
				return				
			#print("NOTLIKETHIS")
			link = message.content[6:].strip()
			
			await self.music.play(message.channel, link)
		
		elif message.content.startswith('!rep'):
			"""Given a number, repeat the song that is currently playing."""
			amt = message.content[5:].strip()
			await self.music.repeat_song(message.channel, amt)
			
		elif message.content.startswith("!response"):
			"""Used to do things with response."""
			r_author = message.author
			
			self.response.set_author(r_author)
		
			await self.send_message(message.channel, "```{}```".format(self.response.get_message()))
			
			option = await self.wait_for_message(author=r_author)
			
			option = option.content.strip()
			
			if option == "1":
				await self.response.create_response(message.channel)
					
			elif option == "2":
				await self.response.delete_response(message.channel)
				
			elif option == "3":
				await self.response.print_responses(message.channel)
			
			elif option == "4":
				await self.send_message(message.channel, "```Exited Successfully!```")
						
		elif message.content.startswith("!flirt"):
			index = randint(0, self.joke_list_length)
			
			await self.send_message(message.channel, "```{}```".format(self.joke_list[index]))
		
		counter = 0
			
		for command in self.response.get_commands():
			if message.content.strip() == command:
				await self.send_message(message.channel, self.response.get_responses()[counter])
			
			counter += 1

		eq = message.content.strip()

		math = Math(eq)
		value = math.parse_equation()
		if value is not None:
			await self.send_message(message.channel, "```{}```".format(value))
				
	async def on_ready(self):
		print('Logged in as')
		print(self.user.name)
		print(self.user.id)
		print('------')
		
		self.music.set_ydl_opts()
		self.default_text_channel, self.default_voice_channel = self.grab_spawn()
	
		if self.default_voice_channel is not None:
			self.voice.voice_state = await self.join_voice_channel(self.default_voice_channel)
			self.voice.voice_channel = self.default_voice_channel
		
		if self.default_text_channel is not None:
			await self.send_message(self.default_text_channel, "```I am now ready!```")
			await self.send_file(self.default_text_channel, "files/maid/maid-start.png")
	
		msg = await self.check_music()
	
		if msg is not None:
			await self.send_message(self.default_text_channel, msg)
				
def main():
	analyze_folder()
	
	try:
		bot = Bot()
		
		bot.run('token')
		
	except Exception as error:
		print(error)
		os.execv(sys.executable, [sys.executable] + sys.argv)

if __name__ == "__main__":
	main()
