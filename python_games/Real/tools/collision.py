from . import *
import constants as c
import pygame, os


class HandleCollision(object):
	def __init__(self, player, enemies, blockers):
		self.player = player
		self.enemies = enemies
		self.blockers = blockers
		print "Finished initiating HandleCollision module..."
		
	def player_and(self):
		collideables = pygame.sprite.spritecollide(self.player, self.blockers, False)
		for blocker in collideables:
			last = self.player.last
			new = self.player.rect
			blocker = blocker.rect
			collide_side = self.collision(last, new, blocker)
			if self.player.target != None:
				self.new_way(self.player, collide_side)
				
	def enemies_and(self):
		collideables = pygame.sprite.groupcollide(self.enemies, self.blockers, False, False)	
		for enemy, colliders in collideables.iteritems():
			for collider in colliders:
				collider = collider.rect
				new = enemy.rect
				last = enemy.last
				collide_side = self.collision(last, new, collider)
				if enemy.target != None:
					self.new_way(enemy, collide_side)
		
	def collision(self, last, new, blocker):
		if last.right <= blocker.left and new.right > blocker.left:
			new.right = blocker.left
			return c.horizontal
		if last.left >= blocker.right and new.left < blocker.right:
			new.left = blocker.right
			return c.horizontal
		if last.bottom <= blocker.top and new.bottom > blocker.top:
			new.bottom  = blocker.top
			return c.vertical
		if last.top >= blocker.bottom and new.top < blocker.bottom:
			new.top = blocker.bottom
			return c.vertical
		
	def new_way(self, sprite, collide_side):
		if collide_side == c.horizontal:
			if sprite.target.rect.centery > sprite.rect.centery:
				sprite.rect.y += sprite.speed
			elif sprite.target.rect.centery < sprite.rect.centery:
				sprite.rect.y -= sprite.speed
		if collide_side == c.vertical:
			if sprite.target.rect.centerx > sprite.rect.centerx:
				sprite.rect.x += sprite.speed
			elif sprite.target.rect.centerx < sprite.rect.centerx:
				sprite.rect.x -= sprite.speed
	
	def update(self):
		self.player_and()
		self.enemies_and()