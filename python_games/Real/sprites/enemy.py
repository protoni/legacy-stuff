from . import *
import constants as c
from tools import spritesheet
from tools import functions as f
from tools import loadgraphic as g
import pygame, os
import math


class Enemy(pygame.sprite.Sprite):
	def __init__(self, x, y, player):
		super(Enemy, self).__init__()
		self.spritesheets = g.load_enemy_spritesheet_graphic()
		self.player = player
		self.direction = c.right
		self.action = c.walk
		self.moving = False
		self.attacking = False
		self.charging = False
		self.sprite = spritesheet.Spritesheet(self.spritesheets, self)
		self.animation_index = 0 # animation index
		self.image = self.sprite.animate()
		self.size = self.image.get_size()
		self.rect = self.image.get_rect(x = x, y = y)
		self.speed = 1.
		self.x_vel = self.y_vel = 0
		self.target = None
		self.full_hp = 100
		self.hp = self.full_hp
		self.damage_taken = 0
		self.aggro_max = 300
		self.aggro_min = 40
		self.in_range = False
		
	def aggro(self):
		x, y = self.player.rect.center
		self_x, self_y = self.rect.center
		distance = math.hypot(x - self_x, y - self_y)
		if distance < self.aggro_max:
			self.target = self.player
			self.x_vel, self.y_vel = f.get_movement_vector(x, y, self_x, self_y, self.speed)		
		else:
			self.target = None
			self.x_vel, self.y_vel = 0, 0
		if distance > self.aggro_min:
			self.in_range = False
		else:
			self.in_range = True

	def move(self):
		self.last = self.rect.copy()
		if not self.in_range:
			self.x_vel, self.y_vel = self.x_vel, self.y_vel
		elif self.in_range:	
			self.x_vel, self.y_vel = 0, 0
			
		if self.x_vel == 0 and self.y_vel == 0:
			self.moving = False
		else:
			self.moving = True
		
		self.rect.x += self.x_vel
		self.rect.y += self.y_vel
		new = self.rect
		
		if self.target != None:
			target_x, target_y = self.target.rect.x, self.target.rect.y
			x, y = self.rect.x, self.rect.y
			if self.in_range:
				self.direction = f.focus(x, y, target_x, target_y)
			else:	
				f.change_direction(self.last, new, self)
	
	def damage(self):
		if self.hp <= 0:
			pygame.sprite.Sprite.kill(self)
			if self.player.target == self:
				self.player.target = None
		if self.damage_taken != 0:
			self.hp -= self.damage_taken
			self.damage_taken = 0
	
	def update(self):
		self.aggro()
		self.move()
		self.damage()
		self.image = self.sprite.animate()

class Boss(Enemy):
	def __init__(self):
		pass