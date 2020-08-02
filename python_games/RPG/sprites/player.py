from . import *
import constants as c
from tools import spritesheet
from tools import functions as f
from tools import loadgraphic as g
import pygame, os, math


class Player(object):
	def __init__(self, x, y):
		self.spritesheets = g.load_player_spritesheet_graphic()
		self.direction = c.right
		self.action = c.walk
		self.moving = False
		self.attacking = False
		self.charging = False
		self.attack_range_max = 350
		self.attack_range_min = 40
		self.sprite = spritesheet.Spritesheet(self.spritesheets, self)
		self.animation_index = 0 # current animation index
		self.animation_attack_indexes = {}
		self.image = self.sprite.animate()
		self.rect = self.image.get_rect(x = x, y = y)
		self.speed = 3
		self.x_vel = self.y_vel = self.speed
		self.target = None
		self.full_hp = 100
		self.hp = self.full_hp
		print "Finished initiating Player module..."
	
	def handle_attack_ranges(self):
		if self.action == c.spell or self.action == c.shoot:
			self.attack_range_min = 250
		if self.action == c.slash:
			self.attack_range_min = 40
		if self.action == c.thrust:
			self.attack_range_min = 60
	
	def update(self, input):
		self.handle_attack_ranges()
		self.image = self.sprite.animate()
		
		