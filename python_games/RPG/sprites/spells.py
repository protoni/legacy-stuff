import pygame
from . import *
import constants as c
from tools import functions as f
from tools import loadgraphic as g

class Spell(pygame.sprite.Sprite):
	def __init__(self, image, rect):
		super(Spell, self).__init__()
		self.image = image
		self.rect = rect
			
	def make_animation_list(self):
		animation_list = []
		x, y = 0, 0
		for row in range(self.rows):
			for col in range(self.cols):
				animation_list.append(f.get_image((x, y), (self.width, self.height), self.sheet))
				x += self.width
			x = 0
			y += self.height
		return animation_list
	
	def animate(self, animation_list):
		if self.index >= len(animation_list) - 1:
			self.end_of_list = True
		self.timer += 1
		if self.end_of_list: # animate the last image for 5frames
			if self.timer >= 5:
				self.index = 0
				self.timer = 0.0
				pygame.sprite.Sprite.kill(self)
		if self.timer >= 5:
			self.index += 1
			self.timer = 0.0
			return animation_list[self.index]
		
		return animation_list[self.index]
	
	def update(self, viewport):
		self.image = self.animate(self.animation_list)
		self.rect.x, self.rect.y = f.game_object_coordinates_transform(self.rect, viewport)
		
class FireBall(Spell):
	index = 0
	timer = 0.0
	end_of_list = False
	sheet = g.load_spell_graphic()['fireball']
	sheet_size = sheet.get_size()
	cols = 6
	rows = 5
	width = sheet_size[0] / cols
	height = sheet_size[1] / rows
	
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.animation_list = self.make_animation_list()
		self.image = self.animate(self.animation_list)
		self.center_x = x - self.width / 2
		self.center_y = y - self.height
		self.rect = self.image.get_rect(x = self.center_x, y = self.center_y)
		super(FireBall, self).__init__(self.image, self.rect)
	
	
class Lightning(Spell):
	index = 0
	timer = 0.0
	end_of_list = False
	sheet = g.load_spell_graphic()['lightning']
	sheet_size = sheet.get_size()
	cols = 1
	rows = 10
	width = sheet_size[0] / cols
	height = sheet_size[1] / rows
	
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.animation_list = self.make_animation_list()
		self.image = self.animate(self.animation_list)
		self.center_x = x - self.width / 2
		self.center_y = y - self.height / 2
		self.rect = self.image.get_rect(x = self.center_x, y = self.center_y)
		super(Lightning, self).__init__(self.image, self.rect)
	
		
class Fire(Spell):
	index = 0
	timer = 0.0
	end_of_list = False
	sheet = g.load_spell_graphic()['fire']
	sheet_size = sheet.get_size()
	cols = 8
	rows = 5
	width = sheet_size[0] / cols
	height = sheet_size[1] / rows
	
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.animation_list = self.make_animation_list()
		self.image = self.animate(self.animation_list)
		self.center_x = x - self.width / 2
		self.center_y = y - self.height / 2
		self.rect = self.image.get_rect(x = self.center_x, y = self.center_y)
		super(Fire, self).__init__(self.image, self.rect)
	
		