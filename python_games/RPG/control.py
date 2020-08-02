import constants as c
import pygame, os
from tools import *
from states import menu
from states import game
from states import gameover
from sprites import level
from gameui import GameUI
from tools import input

pygame.init()


class Control(object):
	def __init__(self, caption):
		self.surface = pygame.display.get_surface()
		self.surface_rect = self.surface.get_rect()
		self.state_dict = {}
		self.state_name = None
		self.level_dict = {}
		self.level_name = None
		self.caption = caption
		self.show_fps = False
		self.done = False
		self.input = input.Input()
		self.fps = 60
		self.clock = pygame.time.Clock()
		self.fps_font = pygame.font.SysFont('comicsansms', 20)
		self.fps_pos = (880, 50)
		
	def set_level(self, level_dict, level_name):
		self.level_dict = level_dict
		self.level_name = level_name
		self.level = level_dict[level_name]
		
	def next_level(self):
		self.state.level_done = False
		self.level_name = self.state.level_next
		self.level = self.level_dict[self.level_name]
		
	def set_state(self, state_dict, state_name):
		self.state_dict = state_dict
		self.state_name = state_name
		self.state = state_dict[state_name]
		self.state.startup(self.level)
		
	def flip_state(self):
		self.state.done = False
		self.state_name = self.state.next
		self.state = self.state_dict[self.state_name]
		self.state.startup(self.level)
		
	def update(self):
		if self.state.level_done:
			self.next_level()
		if self.state.done:
			self.flip_state()
		self.state.update(self.surface, self.input)
		
	def event_loop(self):
		for event in pygame.event.get():
			self.input.update(event)
			self.toggle_show_fps(event)
			if event.type == pygame.QUIT:
				self.done = True
			elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
				self.state.handle_input(event)
			elif event.type == pygame.KEYUP or event.type == pygame.MOUSEBUTTONUP:
				self.state.handle_input(event)
			
	def toggle_show_fps(self, event):
		if event.type == pygame.KEYDOWN and event.key == pygame.K_F5:
			self.show_fps = not self.show_fps
			
	def main(self):
		while not self.done:
			self.event_loop()
			self.update()
			if self.show_fps:
				fps = self.clock.get_fps()
				fps_text = self.fps_font.render('{} {:.2f}'.format('FPS: ', fps), 1, c.white)
				self.surface.blit(fps_text, self.fps_pos)
			pygame.display.update()
			self.clock.tick(self.fps)


caption = 'trololo'	
TMX1 = os.path.join(os.getcwd(),'maps', 'level1.tmx')
TMX2 = os.path.join(os.getcwd(),'maps', 'level2.tmx')
level_dict = {c.level1 : level.Level(TMX1), c.level2 : level.Level(TMX2)}
state_dict = {c.menu : menu.Menu(), c.game : game.Game(), c.gameover : gameover.GameOver()}

run = Control(caption)
run.set_level(level_dict, c.level1)
run.set_state(state_dict, c.menu)
run.main()