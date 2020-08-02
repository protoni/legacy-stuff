from . import *
import constants as c
from tools import tilerender
import pygame, os
from sprites import player, enemy


class Level(object):
	def __init__(self, map):
		self.map = map
		
	def startup(self):
		self.done = False
		self.next = c.menu
		self.renderer = tilerender.Renderer(self.map)
		self.map_image = self.renderer.make_map()
		self.level_surface = self.make_level_surface(self.map_image)
		self.level_rect = self.level_surface.get_rect()
		self.player = self.make_player()
		self.enemies = self.make_enemies()
		self.blockers = self.make_blockers()
		self.viewport = self.make_viewport()
		print "Finished initiating Level module..."
		print "Finished initiating Enemy module..."
		
	def make_viewport(self):
		map_rect = self.map_image.get_rect()
		return c.SCREEN.get_rect(bottom = map_rect.bottom)
		
	def viewport_update(self):
		self.viewport.center = self.player.rect.midbottom
		self.viewport.clamp_ip(self.level_rect)
		
	def make_level_surface(self, map_image):
		map_rect = map_image.get_rect()
		map_width = map_rect.width
		map_height = map_rect.height
		size = map_width, map_height
		return pygame.Surface(size).convert()
		
	def make_player(self):
		for object in self.renderer.tmx_data.getObjects():
			properties = object.__dict__
			if properties['name'] == 'player':
				x = properties['x']
				y = properties['y']
		return player.Player(x, y)
	
	def make_enemies(self):
		enemies = pygame.sprite.Group()
		for object in self.renderer.tmx_data.getObjects():
			properties = object.__dict__
			if properties['name'] == 'enemy':
				x = properties['x']
				y = properties['y']
				sprite = enemy.Enemy(x, y , self.player)
				enemies.add(sprite)
		return enemies
		
	def make_blockers(self):
		blockers = pygame.sprite.Group()
		for object in self.renderer.tmx_data.getObjects():
			properties = object.__dict__
			if properties['name'] == 'blocker':
				x = properties['x']
				y = properties['y']
				width = properties['width']
				height = properties['height']
				blocker = pygame.sprite.Sprite()
				blocker.state = None
				blocker.rect = pygame.Rect(x, y, width, height)
				blockers.add(blocker)
		return blockers
		
	def update(self):
		self.viewport_update()
		
	def draw(self, surface, spells, arrows):
		self.level_surface.blit(self.map_image, self.viewport, self.viewport)
		self.level_surface.blit(self.player.image, self.player.rect)
		self.enemies.draw(self.level_surface)
		spells.draw(self.level_surface)
		arrows.draw(self.level_surface)
		surface.blit(self.level_surface, (0, 0), self.viewport)
		
	