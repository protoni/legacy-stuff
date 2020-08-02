from . import *
import constants as c
import pygame, os


class Input(object):
	def __init__(self):
		self.keyup = True
		self.keydown = False
		self.keys = None
		self.mouse = None
		self.key_events = []
		self.key_event = None
		self.mouse_events = []
		self.mouse_event = None
		self.mousedown = False
		print "Finished initiating Input module..."
	
	def set_input(self, event):
		self.mouse = pygame.mouse.get_pressed()
		self.keys = pygame.key.get_pressed()
		if event.type == pygame.KEYUP:
			self.key_event = event.key
			self.keydown = False
			self.keyup = True
		elif event.type == pygame.KEYDOWN:
			self.key_event = event.key
			self.keyup = False
			self.keydown = True	
		elif event.type == pygame.MOUSEBUTTONDOWN:
			self.mousedown = True
			self.mouse_event = event.button
		
	def reset(self):
		self.keydown = False
		self.mousedown = False
		self.mouse_event = None
		self.mouse = None
		self.key_events = []
		self.mouse_events = []
		self.mouse_event = None
		
	def update(self, event):
		self.reset()
		self.set_input(event)
		