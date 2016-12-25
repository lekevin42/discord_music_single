import time
import math

class Timer:
	def __init__(self):
		self.start_time = None
		self.current_time = None

	def start_timer(self):
		self.start_time = time.clock()
			
	def set_timer(self, t):
		self.start_time = t
			
	def get_start(self):
		return self.start_time
			
	def save_timer(self):
		self.current_time = time.clock()
			
	def get_timer(self):
		self.current_time = time.clock()
		t = self.convert()
		return t
		
	def convert(self):
		t = self.current_time - self.start_time
		
		if t > 3599.99:
			h = t / 3600
			hours = math.floor(h)
			m = t % 3600
			minutes = math.floor(m)
			
			seconds = t % 3600
			seconds = str(seconds)
			seconds = seconds[seconds.find('.') + 1:]
			
			if int(seconds) > 59:
				minutes += 1
				seconds = int(seconds) % 60
				
			if minutes < 10:
				minutes = "0" + str(minutes)
				
			if seconds < 10:
				seconds = "0" + str(seconds)
			
			t = "{0}:{1}:{2}".format(hours, minutes, seconds)
		
		elif t > 59.99:
			seconds = math.floor(t % 60)
			if seconds < 10:
				seconds = "0" + str(seconds)
				
			minutes = math.floor(t / 60)
			t = "{0}:{1}".format(minutes, seconds)
			
		else:
			seconds = math.floor(t % 60)
			t = str(seconds) + " seconds!"
			
		return t

		
"""	
timer = Timer()
timer.start_timer()

time.sleep(65)

print(timer.get_timer())
"""