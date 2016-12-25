import os
from misc.help import *
from random import *

def load_file(file_name):
    stuff = []
	
    with open(file_name) as list:
        for line in list:
            stuff.append(line)
					
    return stuff
	
def find_length(obj):
   return len(obj) -  1
   
def load_owners():
   owner_list = []
   with open('owners.txt') as list:
      for owner in list:
         owner_list.append(owner)
   return owner_list
   
def card_deck_with_suits():
	complete_cards = []
	cards = []
	suits = ['H', 'D', 'S', 'C']

	for num in range(1,11):
		cards.append(num)
	
	cards.append('Jack')
	cards.append('Queen')
	cards.append('King')
	cards.append('Ace')

	for card in cards:
		for suit in suits:
			complete_cards.append([card, suit])

	return complete_cards
	
def card_deck_without_suits():
	complete_cards = []
	
	for count in range(1,5):
		complete_cards.append('J')
		complete_cards.append('Q')
		complete_cards.append('K')
		complete_cards.append('A')
		for num in range(1,11):
			complete_cards.append(num)
	

	
	return complete_cards
	
def card_worth(card):
	if card == 'J' or card == 'Q' or card == 'K':
		return 10
		
	elif card == 'A':
		return 11
		
	return card
	

def load_credentials():
	with open("credentials.txt", 'r') as cred:
		s = cred.read()
	newline = s.find("\n", s.find("\n") + 1)
	user = s[newline:s.find(' ', newline)].strip()
	pas = s[s.find(' ', newline) + 1:].strip()
	
	return user, pas

def analyze_folder():
	miss = 0
	print("Searching for missing files and folders...")
	
	if os.path.exists("credentials.txt") is False:
		print("Found missing credentials.txt, creating it!")
		os.system("touch credentials.txt")
		with open("credentials.txt", "w") as cred:
			cred.write(credentials_help())
		miss += 1
	
	if os.path.exists("rec_songs.txt") is False:
		print("Creating a rec_songs.txt")
		os.system("touch rec_songs.txt")
		miss += 1
	
	if os.path.isdir('playlists/') is False:
		print("Found missing folder, creating playlists!")
		os.system("mkdir playlists")
		miss += 1
		
	if os.path.exists("readme.txt") is False:
		print("Creating readme file!")
		os.system("touch readme.txt")
		with open("readme.txt", "w") as readme:
			readme.write(readme_help())
		miss += 1
		
	if os.path.exists("responses.txt") is False:
		print("Creating responses.txt file!")
		os.system("touch responses.txt")
		miss += 1
		
	if os.path.exists("default_channels.txt") is False:
		print("Creating default_channels.txt!")
		os.system("touch default_channels.txt")
		miss += 1
		
	if os.path.exists("save_songs.txt") is False:
		print("Creating save_songs.txt file!")
		os.system("touch save_songs.txt")
		miss += 1
		
	if os.path.exists("comments.txt") is False:
		print("Creating a comments file!")
		os.system("touch comments.txt")
		miss += 1
		
	if os.path.exists("memes.txt") is False:
		print("Creating a meme file!")
		os.system("touch memes.txt")
		miss += 1
		
	if os.path.exists("options.txt") is False:
		print("Creating an options file!")
		os.system("touch options.txt")
		miss += 1
		
	print("Finished analyzing folder, there were {} missing files!\n".format(miss))
	
def load_responses():
	command_list = []
	responses_list = []
	with open("responses.txt", "rb") as responses:
		for response in responses:
			sep = response.find('|'.encode('utf-8'))
			
			command_list.append(response[0:sep - 1].decode('utf-8'))
			responses_list.append(response[sep + 2:].decode('utf-8'))
			
	return command_list, responses_list
		
		
def magic_ball():
	rand = randint(0,1)
	
	if rand is 0:
		msg = "```The magic 8 ball says YES!```"
	else:
		msg = "```The magic 8 ball says NO!```"
		
	return msg
	
	