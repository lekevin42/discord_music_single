from random import *
import math
import time

class Battle_Royale:
	def __init__(self):
		self.story = None
		self.survivor_count = 0
		self.players = []
		self.no_action = []
		self.action_taken = []
		self.alive = []
		self.grave = []
		self.passive = []
		self.passive_events = []
		self.kill_events = []
		self.death_events = []
		self.winner = None
		self.day = 1
		self.night = 1
		self.is_day = True
		self.path = "classes/Battle_Royale/"

	def get_players(self):
		for player in self.players:
			print(player)
			
	def get_days(self):
		return str(self.day)
	
	def load_game(self):
		self.story = open(self.path + 'story.txt', 'w')
		self.story.write("")
		self.day = 1
		self.night = 1
		
		with open(self.path + "player.txt", 'r') as p_list:
			for player in p_list:
				p = player.strip()
				self.players.append(p)
				self.alive.append(p)
				self.survivor_count += 1
				
		with open(self.path + "events/passive_event.txt", 'r') as pa_list:
			for passive_event in pa_list:
				p_event = passive_event.strip()
				self.passive_events.append(p_event)
			
		with open(self.path + "events/kill_event.txt", 'r') as k_list:
			for k_event in k_list:
				k = k_event.strip()
				self.kill_events.append(k)
				
		with open(self.path + "events/death_event.txt", 'r') as d_list:
			for d_event in d_list:
				d = d_event.strip()
				self.death_events.append(d)
				
	def load_no_action(self):
		for player in self.alive:
			self.no_action.append(player)
	
	def decide_winner(self):
		winner = randint(0, self.survivor_count - 1)
		self.winner = self.players[winner]
		
	def event(self, k_event, p_event, d_event):
		counter = 0
		s_rand = None

		while counter < k_event and k_event is not 0:
			f_rand = randint(0, len(self.no_action) - 1)
			first_person = self.no_action[f_rand]
			
			self.action_taken.append(self.no_action[f_rand])
			self.no_action.pop(self.no_action.index(self.no_action[f_rand]))
			
			s_rand = randint(0, len(self.no_action) - 1)
			
			while (s_rand is f_rand and len(self.no_action) - 1 is not 0) :
				s_rand = randint(0, len(self.no_action) - 1)
					
			second_person = self.no_action[s_rand]
			
			self.action_taken.append(self.no_action[s_rand])
			
			self.no_action.pop(self.no_action.index(self.no_action[s_rand]))
			
			self.kill_event(first_person, second_person)

			counter += 1
		
		counter = 0

		while counter < p_event and p_event is not 0:
			f_rand = randint(0, len(self.no_action) - 1)
			self.passive_event(self.no_action[f_rand])
			self.action_taken.append(self.no_action[f_rand])
			self.no_action.pop(self.no_action.index(self.no_action[f_rand]))
			counter += 1
			
		counter = 0
		
		while counter < d_event and d_event is not 0:
			f_rand = randint(0, len(self.no_action) - 1)
			self.death_event(self.no_action[f_rand])
			self.action_taken.append(self.no_action[f_rand])
			self.no_action.pop(self.no_action.index(self.no_action[f_rand]))
			counter += 1
		
	def kill_event(self, f_person, s_person):
		k_event = randint(0, len(self.kill_events) - 1)
		msg = "{}\n".format(self.kill_events[k_event])

		self.story.write(msg.format(f_person, s_person))
		self.grave.append(s_person)
		self.survivor_count -= 1
		self.alive.pop(self.alive.index(s_person))
	
	def passive_event(self, person):
		p_event = randint(0, len(self.passive_events) - 1)
		msg = "{}\n".format(self.passive_events[p_event])
		self.story.write(msg.format(person))
		
	def death_event(self, person):
		d_event = randint(0, len(self.death_events) - 1)
		msg = "{}\n".format(self.death_events[d_event])
		self.story.write(msg.format(person))
		self.grave.append(person)
		self.survivor_count -= 1
		self.alive.pop(self.alive.index(person))
		
	def total_people(self):
		return len(self.grave) + len(self.alive)
		
	def new_day(self):
		#self.story.write('`End of Day {}`\n\n'.format(self.day - 1))
		if self.is_day:
			msg = "`End of Day {}`\n"
			self.story.write(msg.format(self.day - 1))
			self.is_day = False
		
		else:
			msg = "`End of Night {}`\n"
			self.story.write(msg.format(self.night - 1))
			self.is_day = True
		
		while len(self.action_taken) is not 0:
			self.action_taken.pop()
			
	def m_game(self):
		self.load_game()
		is_day = True
		counter = 0
		self.story.write('`Battle Royale has started` \n')
		
		while len(self.action_taken) is not self.total_people() and self.survivor_count is not 1:
			self.load_no_action()
			
			if is_day:
				msg = "\n`Day {}`\n"
				self.story.write(msg.format(self.day))
				self.day += 1
				is_day = False
			else:
				msg = "\n`Night {}`\n"
				self.story.write(msg.format(self.night))
				self.night += 1
				is_day = True

			amt = math.floor(len(self.alive) / 2)
			d_event = 0
			k_event = randint(0, amt)
			p_event = math.floor(len(self.no_action) - (k_event * 2))
			if p_event is not 0:
				d_event = math.floor(p_event / 3)
				p_event = p_event - d_event
				
			self.event(k_event, p_event, d_event)
		
			self.new_day()
		
		self.story.write("{} is the most savage!\n".format(self.alive[0]))
		self.story.write('`End of game!`\n')	
		
	#	self.story.close()
		
	def read_story(self):
		s = ""
		with open("story.txt", 'r') as story:
			story.seek(0)
			s = story.read()
				
				
		return s
		
def main():		
	BR = Battle_Royale()
	BR.m_game()

if __name__ == "__main__":
	main()