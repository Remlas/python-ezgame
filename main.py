"""
from main import *

a = orki....
"""

import random

map_size_x = input("Podaj szerokosc mapy: ")
map_size_y = input("Podaj wysokosc mapy: ")

class Mapa(object):
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
		
		self.pos_x += x
		self.pos_y += y
		Mapa.mapen[self.pos_x][self.pos_y] = self
		Mapa.mapen[self.pos_x - x][self.pos_y - y] = None
		
	def random_move(self):
		direction = random.randint(1,4)
		if direction == 1:
			self.move(0,1)
		elif direction == 2:
			self.move(1,0)
		elif direction == 3:
			self.move(0,-1)
		elif direction == 4:
			self.move(-1,0)
		

	#property
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

class Orki(Creature):
	def __init__(self, pos_x, pos_y, hp=20):
		Creature.__init__(self)
		#super(Orki, self).__init__() < z grubsza rownowazne > Creature.__init__
		self.pos_x = pos_x
		self.pos_y = pos_y
		self.hp = hp

	#property
	def attack(self):
		return self._base_attack * 4
		
	def die(self):
		print("For Sauron")
		self.alive = False

class Player(Creature):
	pass

class MorskieOrki(Orki):
	water_protection = True
	def __init__(self, pos_x, pos_y, hp=20):
		Orki.__init__(self)
		self.pos_x = pos_x
		self.pos_y = pos_y
		self.hp = hp
		
	def die(self):
		print("BulBul")
		if not self.water_protection:
			self.alive = False


class LesneOrki(Orki):
	forest_protection = True
	pass
