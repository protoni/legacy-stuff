from tools import collision
from tools import handleactions
from tools import spritesheet
from . import *
import constants as c
import pygame, os
import gameui

class Game(object):
	def __init__(self):
		self.next = None
		self.done = False
		self.level_next = None
		self.level_done = False
		self.surface = pygame.display.get_surface()
		
	def startup(self, level):
		self.level = level
		self.level.startup()
		self.level_surface = self.level.level_surface
		self.blockers = self.level.blockers
		self.player = self.level.player
		self.enemies = self.level.enemies
		self.viewport = self.level.viewport
		self.handleplayeractions = handleactions.HandlePlayerActions(self.player, self.enemies, self.blockers, self.viewport)
		self.collision = collision.HandleCollision(self.player, self.enemies, self.blockers)
		self.gameui = gameui.GameUI(self.player, self.enemies)
		self.spells = self.handleplayeractions.spells
		self.arrows = self.handleplayeractions.arrows
		print "Finished initiating the Game Engine..."
		
	def update(self, surface, input):
		self.player.update(input)
		self.enemies.update()
		self.collision.update()
		self.handleplayeractions.update(input)
		self.gameui.update(input, surface)
		self.level.update()
		self.draw(surface)
		
	def draw(self, surface):
		self.level.draw(surface, self.spells, self.arrows)
		self.gameui.draw(surface)
		
	def handle_input(self, event):
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				self.next = c.menu
				self.done = True
		