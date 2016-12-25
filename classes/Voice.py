import discord
import asyncio

class Voice:
	def __init__(self, bot):
		self.bot = bot
		self.voice_state = None
		self.voice_channel = None
		self.default_text_channel = None
		self.default_voice_channel = None
		
	async def join_channel(self, server, schannel, content):
		if self.bot.is_voice_connected(server):
			await self.bot.send_message(schannel, '```Already connected to a voice channel```')
			return
		
		channel_name = content[5:].strip()
		check = lambda c: c.name == channel_name and c.type == discord.ChannelType.voice
		
		channel = discord.utils.find(check, server.channels)
		
		if channel is None:
			await self.bot.send_message(schannel, '```Cannot find a voice channel by that name.```')
			return
		
		self.voice_state = await self.bot.join_voice_channel(channel)
		self.voice_channel = channel.name

		
	async def leave_channel(self, channel):
		await self.bot.send_message(channel, "```Disconnecting...```")
		await self.voice_state.disconnect()
		self.voice_state = None
		