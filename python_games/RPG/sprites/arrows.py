import pygame, math
from . import *
import constants as c
from tools import functions as f
from tools import loadgraphic as g

class Arrow(pygame.sprite.Sprite):
	max_distance = 250 # max arrow flight distance
	def __init__(self, x, y, rect, direction):
		super(Arrow, self).__init__()
		self.x = x
		self.y = y
		self.rect = rect
		self.direction = direction
		
	def make_arrow_dict(self):
		x, y = 0, 0
		directions = [c.left, c.up, c.right, c.down]
		arrow_dict = {}
		for direction in directions:
			arrow_dict[direction] = f.get_image((x, y), (self.width, self.height), self.sheet)
			x += self.width
		return arrow_dict
		
	def change_arrow_coordinates(self, target, viewport):
		# change spell coordinates when camera moves
		world_x = viewport.x + target.x
		world_y = viewport.y + target.y
		move_x = target.x + viewport.x
		move_y = target.y + viewport.y
		target_x = world_x - move_x
		target_y = move_y - move_y
		new_x = target_x + target.x
		new_y = target_y + target.y
		return new_x, new_y
		
	def update(self, viewport):
		self.rect.x, self.rect.y = f.game_object_coordinates_transform(self.rect, viewport)
		distance = math.hypot(self.x - self.rect.x, self.y - self.rect.y)
		if distance > self.max_distance:
			pygame.sprite.Sprite.kill(self)
	
		if self.direction == c.up:
			self.rect.y -= self.speed
		elif self.direction == c.left:
			self.rect.x -= self.speed
		elif self.direction == c.down:
			self.rect.y += self.speed
		elif self.direction == c.right:
			self.rect.x += self.speed
		
class BasicArrow(Arrow):
	sheet = g.load_arrow_graphic()['arrow']
	sheet_size = sheet.get_size()
	width = sheet_size[0] / 4 # 4 cols
	height = sheet_size[1] # 1 rows
	speed = 12
	damage = 5
	
	def __init__(self, x, y, direction):
		self.x = x # original position
		self.y = y # original position
		self.arrow_dict = self.make_arrow_dict()
		self.direction = direction
		self.image = self.arrow_dict[direction]
		self.center_x = x - self.width / 2
		self.center_y = y - self.height / 2
		self.rect = self.image.get_rect(x = self.center_x, y = self.center_y)
		super(BasicArrow, self).__init__(self.x, self.y, self.rect, self.direction)
		
class DoubleArrow(Arrow):
	sheet = g.load_arrow_graphic()['arrow_double']
	sheet_size = sheet.get_size()
	width = sheet_size[0] / 4 # 4 cols
	height = sheet_size[1] # 1 rows
	speed = 12
	damage = 10
	
	def __init__(self, x, y, direction):
		self.x = x # original position
		self.y = y # original position
		self.arrow_dict = self.make_arrow_dict()
		self.direction = direction
		self.image = self.arrow_dict[direction]
		self.center_x = x - self.width / 2
		self.center_y = y - self.height / 2
		self.rect = self.image.get_rect(x = self.center_x, y = self.center_y)
		super(DoubleArrow, self).__init__(self.x, self.y, self.rect, self.direction)
		
		
class FireArrow(Arrow):
	sheet = g.load_arrow_graphic()['arrow_fire']
	sheet_size = sheet.get_size()
	width = sheet_size[0] / 4 # 4 cols
	height = sheet_size[1] # 1 rows
	speed = 12
	damage = 15
	
	def __init__(self, x, y, direction):
		self.x = x # original position
		self.y = y # original position
		self.arrow_dict = self.make_arrow_dict()
		self.direction = direction
		self.image = self.arrow_dict[direction]
		self.center_x = x - self.width / 2
		self.center_y = y - self.height / 2
		self.rect = self.image.get_rect(x = self.center_x, y = self.center_y)
		super(FireArrow, self).__init__(self.x, self.y, self.rect, self.direction)
	