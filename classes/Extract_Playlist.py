# Name: Extract_Playlist.py
# Version: 1.5
# Author: pantuts
# Email: pantuts@gmail.com
# Description: Parse URLs in Youtube User's Playlist (Video Playlist not Favorites)
# Use python3 and later
# Agreement: You can use, modify, or redistribute this tool under
# the terms of GNU General Public License (GPLv3).
# This tool is for educational purposes only. Any damage you make will not affect the author.
# Usage: python3 Extract_Playlist.py youtubeURLhere

#This program was not created by me but it is used to extract information from youtube
 
import re
import urllib.request
import urllib.error
import sys
import time

class Extract:
	def __init__(self, url):
		self.url = url

	def check(self):
		if 'http' not in self.url:
			self.url = 'http://' + self.url
				
		url_list = self.crawl()
		return url_list
				
	def crawl(self):
		sTUBE = ''
		cPL = ''
		amp = 0
		final_url = []
    
		if 'list=' in self.url:
			eq = self.url.rfind('=') + 1
			cPL = self.url[eq:]
            
		else:
			print('Incorrect Playlist.')
	
    
		try:
			yTUBE = urllib.request.urlopen(self.url).read()
			sTUBE = str(yTUBE)
		except urllib.error.URLError as e:
			print(e.reason)
    
		tmp_mat = re.compile(r'watch\?v=\S+?list=' + cPL)
		mat = re.findall(tmp_mat, sTUBE)
 
		if mat:
			for PL in mat:
				yPL = str(PL)
				if '&' in yPL:
					yPL_amp = yPL.index('&')
				final_url.append('http://www.youtube.com/' + yPL[:yPL_amp])
 
			all_url = list(set(final_url))
 
			return all_url
