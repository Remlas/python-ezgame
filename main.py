"""
from main import *

a = Orcs....
"""

import random
import os

"""
on each game start ask user about size of the map
"""
map_size_x = input("Podaj szerokosc mapy: ")
map_size_y = input("Podaj wysokosc mapy: ")


class Map(object):
	"""
	Map generator on start and object
	Show map by Map.Mapen
	"""
	mapen = []
	for _ in range(map_size_y):
		tmp = []
		for i in range(map_size_x):
			tmp.append(None)
		mapen.append(tmp)

class Creature(object):
	"""
	Base creaqture class.
	"""
	def __init__(self, hp=0, mp=0, pos_x=0, pos_y=0, base_attack=2):
		self.hp = hp
		self.mp = mp
		self._base_attack = base_attack
		self.pos_x = pos_x
		self.pos_y = pos_y
		self.alive = True
		
	def move(self, x,y):	
		if (self.pos_x+x > map_size_x or self.pos_x+x <= 0) or (self.pos_y+y > map_size_y or self.pos_y+y <= 0):
			print("Nie mozesz wyjsc poza mape! Tracisz kolejke")
		else:
			self.pos_x += x
			self.pos_y += y
			Map.mapen[self.pos_x][self.pos_y] = self
			Map.mapen[self.pos_x - x][self.pos_y - y] = None
		
	def random_move(self):
		"""
		Randomly select 1 of 4 world direction, then call move() method to move
		"""
		direction = random.randint(1,4)
		if direction == 1:
			self.move(0,1)
		elif direction == 2:
			self.move(1,0)
		elif direction == 3:
			self.move(0,-1)
		elif direction == 4:
			self.move(-1,0)
		

	@property
	def attack(self):
		"""
		Effective attack power of creature
		"""
		return self._base_attack
		
	def hit(self, target):
		"""
		Hit the target with all you got!
		"""
		target.hp -= self.attack
		self.try_to_kill(target)
	
	def try_to_kill(self, target):
		"""
		Mr. Target, plz die now...
		"""
		if target.hp <= 0:
			target.die()
	
	def die(self):
		print("AAAAAAAaaarghhh!!!")
		self.alive = False

class Orcs(Creature):
	def __init__(self, pos_x, pos_y, hp=20):
		Creature.__init__(self)
		self.pos_x = pos_x
		self.pos_y = pos_y
		self.hp = hp
		Map.mapen[self.pos_x][self.pos_y] = self

	@property
	def attack(self):
		return self._base_attack * 4
		
	def die(self):
		self.alive = False
		Map.mapen[self.pos_x][self.pos_y] = None #When target die - it's removed from the map
		print("For Sauron")


class Player(Creature):
	pass

class WaterOrcs(Orcs):
	water_protection = True
	def __init__(self, pos_x, pos_y, hp=20):
		Orcs.__init__(self)
		self.pos_x = pos_x
		self.pos_y = pos_y
		self.hp = hp
		
	def die(self):
		print("BulBul")
		if not self.water_protection:
			self.alive = False


class ForestOrcs(Orcs):
	forest_protection = True
	pass

	
a=Orcs(2,2)
b=Orcs(2,1)