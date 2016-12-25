from parsers.parser import *
from urllib.request import urlopen
from bs4 import BeautifulSoup
from random import *
from classes.Web_Parser import *

#parse for dictionary
def parse_dict(word):	
	try:
		if word.find(" ") is not -1:
			word_search = word.replace(" ", "-")
			url = 'http://dictionary.reference.com/browse/' + word_search
		else:
			url = 'http://dictionary.reference.com/browse/' + word + "?s=t"

		response = urlopen(url)
		html = response.read()
		soup = BeautifulSoup(html, "html.parser")
		definition = soup.find("div", attrs={"class": "def-content"})
		return (definition.contents[0].strip())
				
	except urllib.error.HTTPError as error:
		return("Error")

#parser for urban dictionary, beware of 18+ content
def parse_urban(word):
	try:
		if word.find(" ") is not -1:
			word_search = word.replace(" ", "%20")
			url = "http://www.urbandictionary.com/define.php?term=" + word_search
		else:
			url = "http://www.urbandictionary.com/define.php?term=" + word

		response = urlopen(url)
		html = response.read()

		soup = BeautifulSoup(html, "html.parser")
		
		s = soup.find("div", attrs={"class": "meaning"})
		
		return(s.contents[0].strip())
		
	except urllib.error.HTTPError as error:
		return("Cannot find word!")
		
		
#parse for youtube		
def parse_yt(word):
	try:
		query = word.replace(' ', '+')
		url = "https://www.youtube.com/results?search_query=" + query
		response = urlopen(url)
		html = response.read()
		soup = BeautifulSoup(html, "html.parser")
		for vid in soup.findAll(attrs={'class':'yt-uix-tile-link'}):
			song = 'https://youtube.com' + vid['href']
			#print(vid)
			return song

	except urllib.error.HTTPError as error:
		return("Error")
	
def crawl_rec(link, max):
	counter = 0

	try:
		list = []
		response = urlopen(link)
		html = response.read()
		soup = BeautifulSoup(html, "html.parser")
		#print(link, counter)
		#for vid in soup.findAll("a", attrs={'class': 'yt-uix-sessionlink content-link spf-link spf-link '}):
		for vid in soup.findAll("a", attrs={'class': ' content-link spf-link yt-uix-sessionlink spf-link '}):
			if counter < max:
				song = "https://youtube.com" + vid['href']
				counter += 1
				#print(song, counter)
			else:
				max += 1
				print(song, link, max)
				return song, max 

	except urllib.error.HTTPError as error:
		print("HTTPERROR")
		return("Error")