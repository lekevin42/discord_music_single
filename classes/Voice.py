import discord
import asyncio

class Voice:
	"""Class that handles the Discord voice connection
	
	Parameters:
		1) bot - allows the usage of the Discord API
	"""
	
	def __init__(self, bot):
		self.bot = bot
		self.voice_state = None
		self.voice_channel = None
		self.default_text_channel = None
		self.default_voice_channel = None
		
		
	async def join_channel(self, server, schannel, content):
		"""Function used to create the voice client given key arguments
		
		Parameters:
			1) server - the server the channel is located on
			2) schannel - channel to send error msg to
			3) content - voice channel to join
		
		"""
		
		#Check to see if voice client is already initialized
		if self.bot.is_voice_connected(server):
			await self.bot.send_message(schannel, '```Already connected to a voice channel```')
			return
		
		channel_name = content[5:].strip()
		check = lambda c: c.name == channel_name and c.type == discord.ChannelType.voice
		
		#Check to see if voice channel exists
		channel = discord.utils.find(check, server.channels)
		
		if channel is None:
			await self.bot.send_message(schannel, '```Cannot find a voice channel by that name.```')
			return
		
		#Create the voice client
		self.voice_state = await self.bot.join_voice_channel(channel)
		self.voice_channel = channel.name

		
	async def leave_channel(self, channel):
		"""Function that leaves the voice channel
		
		Parameters:
			1) channel - channel to send message to
		"""
			
		await self.bot.send_message(channel, "```Disconnecting...```")
		await self.voice_state.disconnect()
		self.voice_state = None
		