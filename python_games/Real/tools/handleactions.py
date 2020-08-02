from . import *
import constants as c
import sprites
from sprites import spells, arrows
import math
import pygame, os
from tools import functions as f


class HandlePlayerActions(object):
	def __init__(self, player, enemies, blockers, viewport):
		self.player = player
		self.enemies = enemies
		self.blockers = blockers
		self.viewport = viewport
		self.arrows = pygame.sprite.Group()
		self.spells = pygame.sprite.Group()
		self.add_arrow = False
		self.spell_target = None
		print "Finished initiating HandleActions module..."
		
	def set_targets(self, mouse_event):
		# check if mouse is colliding with enemy
		# set enemy as target
		for enemy in self.enemies:
			target = f.world_to_pixel_coordinates(enemy, self.viewport)
			if not f.mouse_click().colliderect(target):
				self.player.target = None
		for enemy in self.enemies:
			target = f.world_to_pixel_coordinates(enemy, self.viewport)
			if f.mouse_click().colliderect(target):
				if mouse_event == 1:
					self.player.target = enemy
	
	def move(self, input):
		self.player.last = self.player.rect.copy()
		if not self.player.attacking:
			if input.keys[pygame.K_w]:
				self.player.rect.y -= self.player.y_vel
				self.player.direction = c.up
				self.player.action = c.walk
				self.player.moving = True
			elif input.keys[pygame.K_s]:
				self.player.rect.y += self.player.y_vel
				self.player.direction = c.down
				self.player.action = c.walk
				self.player.moving = True
			elif input.keys[pygame.K_a]:
				self.player.rect.x -= self.player.x_vel
				self.player.direction = c.left
				self.player.action = c.walk
				self.player.moving = True
			elif input.keys[pygame.K_d]:
				self.player.rect.x += self.player.x_vel
				self.player.direction = c.right
				self.player.action = c.walk
				self.player.moving = True
			else:
				self.player.moving = False
	
	def attack(self, input):
		if input.keydown:
			if input.key_event == pygame.K_1:
				self.player.attacking = True
				self.player.action = c.slash
			elif input.key_event == pygame.K_2:
				self.player.attacking = True
				self.player.action = c.spell
				self.cast()
			elif input.key_event == pygame.K_3:
				self.player.attacking = True
				self.player.action = c.shoot
				self.add_arrow = True # create arrow only when sprite animation is right
			elif input.key_event == pygame.K_4:
				self.player.attacking = True
				self.player.action = c.thrust
	
	def charge(self):
		# run to attacked enemy
		enemy_x, enemy_y = self.player.target.rect.center
		self_x, self_y = self.player.rect.center
		speed = 3.
		movement_vector = f.get_movement_vector(enemy_x, enemy_y, self_x, self_y, speed)
		distance = math.hypot(enemy_x - self_x, enemy_y - self_y)
		if distance > self.player.attack_range_min and distance < self.player.attack_range_max:
			self.player.rect.x += movement_vector[0]
			self.player.rect.y += movement_vector[1]
			self.player.charging = True
		else:
			self.player.charging = False
		self.player.direction = f.focus(self_x, self_y, enemy_x, enemy_y)
	
	def cast(self):
		x, y = pygame.mouse.get_pos()
		self.player.direction = f.focus(self.player.rect.x, self.player.rect.y, x, y)
		x += self.viewport.x
		y += self.viewport.y
		fireball = spells.FireBall(x, y)
		self.spells.add(fireball)
	
	def handle_keyboard(self, input):
		self.move(input)
		if not self.player.moving and not self.player.attacking and not self.player.charging: # attack
			self.attack(input)
		if self.player.target != None and self.player.attacking: # charge
			self.charge()
		else:
			self.player.charging = False
				
	def handle_mouse(self, input):
		if input.mousedown:
			self.set_targets(input.mouse_event)
	
	def handle_arrows(self):
		if self.add_arrow and self.player.animation_index >= 8:
			x, y = self.player.rect.center
			basicarrow = arrows.FireArrow(x, y, self.player.direction)
			self.arrows.add(basicarrow)
			self.add_arrow = False
			
		collideables = pygame.sprite.groupcollide(self.arrows, self.enemies, False, False)	
		for arrow, enemies in collideables.iteritems():
			for enemy in enemies:
				pygame.sprite.Sprite.kill(arrow)
				enemy.damage_taken += arrow.damage
				
	
	def update(self, input):
		self.handle_mouse(input)
		self.handle_keyboard(input)
		self.spells.update(self.viewport)
		self.handle_arrows()
		self.arrows.update(self.viewport)