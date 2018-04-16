"""
from main import *

a = Orcs....
"""

import random
import os
import sys

import pygame
from pygame.locals import *


pygame.init()


"""
on each game start ask user about size of the map
"""
map_size_x = int(input("Podaj szerokosc mapy: "))
map_size_y = int(input("Podaj wysokosc mapy: "))

class WorldObjects(object):
	#Name-ID
	TileTypes = {
		'GROUND' : 0, 
		'WATER' : 1, 
		'FOREST' : 2, 
		'FIRE' : 3,
		'VOID' : 4}

class Map(object):
	"""
	Map generator on start and object
	Show map by Map.grid
	"""
	
	#Random terrain - YEA
	def rand_tile():
		rtile = random.choice(list(WorldObjects.TileTypes.values())) 
		return rtile

	#Grid for creatures
	grid = []
	for _ in range(map_size_y):
		tmp = []
		for i in range(map_size_x):
			tmp.append(None)
		grid.append(tmp)
		
	#tiles for world
	tiles = []
	for _ in range(map_size_y):
		tmp = []
		for i in range(map_size_x):
			tmp.append(rand_tile())
		tiles.append(tmp)

	
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
		"""
		Because of the list as map, first index is for height (y - number of list - row number) and second is for width (x - number on list - column number) position on map.
		"""
		if (self.pos_x+x > map_size_x-1 or self.pos_x+x < 0) or (self.pos_y+y > map_size_y-1 or self.pos_y+y < 0):
			print("Nie mozesz wyjsc poza mape! Tracisz kolejke")
		elif Map.grid[self.pos_y + y][self.pos_x + x] != None: #check if new position is empty
			print("Ktos juz tam jest, tracisz kolejke")
		else:
			self.pos_x += x
			self.pos_y += y
			Map.grid[self.pos_y][self.pos_x] = self
			Map.grid[self.pos_y - y][self.pos_x - x] = None
		
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
		Map.grid[self.pos_x][self.pos_y] = None #When target die - it's removed from the map

class Orcs(Creature):
	def __init__(self, pos_x, pos_y, hp=20):
		Creature.__init__(self)
		self.pos_x = pos_x
		self.pos_y = pos_y
		self.hp = hp
		Map.grid[self.pos_x][self.pos_y] = self

	@property
	def attack(self):
		return self._base_attack * 4
		
	def die(self):
		self.alive = False
		Map.grid[self.pos_x][self.pos_y] = None #When target die - it's removed from the map
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
	
	
	
class Graphics(object):
	#color names to hex
	BLACK = (0, 0, 0)
	WHITE = (255, 255, 255)
	RED = (255, 0, 0)
	GREEN = (0, 255, 0)
	BLUE = (0, 0, 255)
	
	#and patching those colors to tile type
	
	colors = {
		WorldObjects.TileTypes['GROUND'] : BLACK,
		WorldObjects.TileTypes['WATER'] : BLUE,
		WorldObjects.TileTypes['FOREST'] : GREEN,
		WorldObjects.TileTypes['FIRE'] : RED,
		WorldObjects.TileTypes['VOID'] : WHITE
		}
	
	#how big is one Tile. Maximum monitor height or width minus 20% for windows bars
	max_per_h = pygame.display.Info().current_h * 0.8
	TileSize = int(round(max_per_h / map_size_y))
	
DISPLAYARENA = pygame.display.set_mode((map_size_x*Graphics.TileSize, map_size_y*Graphics.TileSize))

while True:

	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
			
	for row in range(map_size_y):
		#loop through each column in the row
		for column in range(map_size_x):
			#draw the resource at that position in the tilemap, using the correct colour
			pygame.draw.rect(DISPLAYARENA, Graphics.colors[Map.tiles[row][column]], (column*Graphics.TileSize,row*Graphics.TileSize,Graphics.TileSize,Graphics.TileSize))
	
	pygame.display.update()
