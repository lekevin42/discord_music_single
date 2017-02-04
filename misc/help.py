def general_help():
	msg = "```*Song Commands*\n \
!join channel - join a voice channel \n \
!leave - leave a voice channel \n \
!play <url/playlist/query> - play songs\n \
!skip - skip a song\n \
!clear - clear every song in queue\n \
!pause - pause the song \n \
!rep <amt> - repeat the song this many times \n \
!resume - resume the song \n \
!response - response stuff``` \
\n \
```*Managing your playlist* \n \
!playlist - playlist management ``` \
\n \
```*Fun Commands* \n \
!avatar <username> - pic of someone's avatar \n \
!8ball <msg> - ask the magic ball \n \
!restart - restart the bot \n \
!dict - query dictionary.com\n \
!rec - automatic youtube queue\n \
!udict - query urbandictionary.com\n \
!meme - unleash the memes\n \
!roll - use like magic ball \n \
\n```  \
"

	return msg
	
def terminal_help():
	msg = '`change directory - cd <directoryname> \n \
go all the way back - cd \n \
go back one folder - cd .. \n \
list all files - ls \n \
run python program - python <file_name> \n \
create a file - touch <file_name> (python files end with .py) \n \
remove a file - rm <file_name> \n \
`'

	return msg
	
def python_help():
	msg = "'https://www.python.org/downloads/windows/' \n \
DL python3.5.1 Windows x86 executable installer or Windows x86-64 executable installer \n \
You need Windows SP1 to download python3.5.1 \n \
'https://sourceforge.net/projects/mingw/files/' \n \
(mingw) dl with mingw and msys base plox \n \
'https://notepad-plus-plus.org/download/v6.9.html'"

	return msg
	
	
def credentials_help():
	msg = "#Please place your credentials in this folder.\n\
#Ex. username password\n"

	return msg
	
def readme_help():
	msg = "Hello there, this discord bot was programmed by Kevin Le and this was done as a fun project for me and some friends.\n\
In order for the bot to function properly,\n\
1) Please run the .exe file first and let it generate missing files and folders that you will need.\n\
2) Edit the credentials.txt file.\n\
3) Start the program again.\n\n\
Thanks for trying out my bot and have fun!"
	
	return msg
"""
await self.send_message(message.channel, 'https://www.python.org/downloads/windows/')
			await self.send_message(message.channel, 'DL python3.5.1 Windows x86 executable installer or Windows x86-64 executable installer')
			await self.send_message(message.channel, 'You need Windows SP1 to download python3.5.1')
			await self.send_message(message.channel, 'https://sourceforge.net/projects/mingw/files/')
			await self.send_message(message.channel, '(mingw) dl with mingw and msys base plox')
			await self.send_message(message.channel, 'https://notepad-plus-plus.org/download/v6.9.html')
"""