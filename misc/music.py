def add(link):
	playList = []
			
	if link != "":
		if link.find("list=") != -1:
			playlist = Extract(link)
			list = playlist.check()
				
			for song in list:
				await self.play_list.put(song)
			await self.send_message(message.channel, "`I have queued your playlist!`")
				
		elif link.find("http") == -1:
			file = link
			file += ".txt"
				with open(self.file_path + file) as list:
				for song in list:
					song = song.strip()
					playList.append(song)
						
				shuffle(playList)
					
				for song in playList:
					await self.play_list.put(song)
				await self.send_message(message.channel, "`I have queued {}!`".format(file))
					
		else:		
			url = link.strip()
			await self.play_list.put(url)
			await self.send_message(message.channel, "`I have queued your song request!`")
					
	else:
		await self.send_message(message.channel, "`!add is used to add songs, playlists, or youtube playlists!`")
		await self.send_message(message.channel, "`Usage: !add <url/song>`")