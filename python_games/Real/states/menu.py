from . import *
import constants as c
from tools import functions as f
from tools import loadgraphic as g
import pygame, os, time


class Menu(object):
	def __init__(self):
		self.background = g.load_menu_graphic()['menu_background_small']
		self.background_rect = self.background.get_rect()
		self.button_background = g.load_menu_graphic()['button_background']
		self.button_background_rect = self.button_background.get_rect()
		self.screen_rect = c.SCREEN.get_rect()
		
		self.next = None
		self.done = False
		self.level_next = None
		self.level_done = False
		self.menu_items = [c.level1, c.level2]
		self.surface = pygame.display.get_surface()
		print "Finished initiating the Main Menu..."
		
	def startup(self, level):
		self.buttons = self.make_buttons()
	
	def make_buttons(self):
		screen = c.SCREEN.get_rect()
		x = screen.centerx - 53
		y = screen.centery
		gap = 50
		menu_buttons = pygame.sprite.Group()
		for item in self.menu_items:
			button = MenuButton(x, y, item, self.surface)
			menu_buttons.add(button)
			y += gap
		return menu_buttons
	
	def update(self, surface, input):
		self.draw(surface)
		self.buttons.update()
	
	def button_background_draw(self):
		x = (self.screen_rect.width / 2) - (self.button_background_rect.width / 2)
		y = (self.screen_rect.height / 2) - 100
		self.surface.blit(self.button_background, (x, y))
	
	def draw(self, surface):
		surface.blit(self.background, self.background_rect)
		self.button_background_draw()
		self.buttons.draw(surface)
		for button in self.buttons:
			button.render_text()
	
	def button_pressed(self):
		for button in self.buttons:
			if f.mouse_click().colliderect(button.rect):
				button.pressed()
				if button.item == c.level1:
					self.level_next = c.level1
					self.level_done = True
					self.next = c.game
					self.done = True
				elif button.item == c.level2:
					self.level_next = c.level2
					self.level_done = True
					self.next = c.game
					self.done = True
		
	def handle_input(self, event):		
		if event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 1:
				self.button_pressed()
		
		
class MenuButton(pygame.sprite.Sprite):
	def __init__(self, x, y, item, surface):
		super(MenuButton, self).__init__()
		self.surface = surface
		self.item = item
		self.menu_buttons = g.load_menu_graphic()
		self.image = self.menu_buttons['button_solid']
		self.rect = self.image.get_rect(x = x, y = y)
		self.font = pygame.font.SysFont('comicsansms', 15)
		self.button_text = self.font.render(item, 1, c.white)
		self.button_text_x = self.rect.centerx
		self.button_text_y = self.rect.centery
		
	def update(self):
		if f.mouse_click().colliderect(self.rect):
			self.image = self.menu_buttons['button_hover']
		else:
			self.image = self.menu_buttons['button_solid']
	
	def render_text(self):
		self.surface.blit(self.button_text, (self.button_text_x - 17, self.button_text_y - 10))
	
	def pressed(self):
		self.image = self.menu_buttons['button_pressed']
		self.surface.blit(self.image, self.rect)
		pygame.display.update()
		
		
		
		
		
		