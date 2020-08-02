import constants as c
import pygame, os
from tools import loadgraphic as g


class GameUI(object):
	def __init__(self, player, enemies):
		self.player = player
		self.enemies = enemies
		self.player_exists = False
		self.target_exists = False
		self.font = pygame.font.Font(None, 20)
		self.hotkeys = 4
		self.skill_bar = self.make_skill_bar()
		print "Finished initiating User interface..."
		
	def make_unit_frames(self):
		gap = c.unit_gap
		self.player_frame = UnitFrame(c.unit_x, c.unit_y, self.player)
		self.player_exists = True
		if self.player.target != None:
			self.target_frame = UnitFrame(c.unit_x + gap, c.unit_y, self.player.target)
			self.target_exists = True	
		
	def unit_frames_update(self):
		if not self.player_exists or not self.target_exists:
			self.make_unit_frames()
		self.player_frame.update()
		if self.player.target != None:
			self.target_frame.sprite = self.player.target
			self.target_frame.update()
	
	def make_skill_bar(self):
		skill_bar = pygame.sprite.Group()
		screen = c.SCREEN.get_rect()
		x = screen.width / 2 - 80
		y = screen.height - 40
		gap = 40
		for hotkey in range(self.hotkeys):
			skill = SkillBar(x, y, hotkey + 1)
			skill_bar.add(skill)
			x += gap
		return skill_bar
				
	def update(self, input, surface):
		self.unit_frames_update()
		self.skill_bar.update(input, surface)
		
	def draw_unit_frame(self, surface):
		if self.player_exists:
			self.player_frame.draw(surface)	
		if self.target_exists and self.player.target != None:
			self.target_frame.draw(surface)
			
	def draw_skill_bar(self, surface):
		self.skill_bar.draw(surface)
		for skill in self.skill_bar:
			skill.draw_skill_image(surface)
		
	def draw(self, surface):
		self.draw_unit_frame(surface)
		self.draw_skill_bar(surface)

class UnitFrame(object):
	def __init__(self, x, y, sprite):
		self.empty, self.full = g.load_unit_frame_graphic()
		self.full_width, self.full_height = self.full.get_size()
		self.empty_rect = self.empty.get_rect(x = x, y = y)
		self.full_rect = self.full.get_rect(x = x, y = y)
		self.unit_hp_x, self.unit_hp_y = self.full_rect.center
		self.sprite = sprite
		self.font = pygame.font.Font(None, 20)
	
	def update(self):
		self.percent = float(self.sprite.hp) / float(self.sprite.full_hp)
		damaged_width = int(self.full_width * self.percent)
		self.full_rect.width = damaged_width
		self.make_damaged_frame(damaged_width)
		self.unit_hp = self.font.render('%d / %d ' % (self.sprite.hp, self.sprite.full_hp), 1, c.black)
		
	def make_damaged_frame(self, damaged_width):
		if damaged_width < 0:
			damaged_width = 0
		damaged_frame = pygame.Surface((damaged_width, self.full_height))
		damaged_frame.blit(self.full, (0, 0))
		self.damaged_frame = damaged_frame
		
	def draw(self, surface):
		if self.sprite.hp > 0:
			surface.blit(self.empty, self.empty_rect)
			surface.blit(self.damaged_frame, self.full_rect)
			surface.blit(self.unit_hp, (self.unit_hp_x - 30, self.unit_hp_y - 6))

class SkillBar(pygame.sprite.Sprite):
	def __init__(self, x, y, hotkey):
		super(SkillBar, self).__init__()
		self.pressed_key = None
		self.hotkey = hotkey
		self.buttons, self.skills = g.load_skill_bar_graphic()
		self.image = self.buttons['button_up']
		self.rect = self.image.get_rect(x = x, y = y)
		self.skill_image = self.set_skill_image()
		self.skill_image_rect = self.skill_image.get_rect()
		self.skill_image_rect.centerx = self.rect.centerx
		self.skill_image_rect.centery = self.rect.centery
		
	def set_pressed_key(self, input):
		if input.keydown:
			if input.key_event == pygame.K_1:
				self.pressed_key = 1
			elif input.key_event == pygame.K_2:
				self.pressed_key = 2
			elif input.key_event == pygame.K_3:
				self.pressed_key = 3
			elif input.key_event == pygame.K_4:
				self.pressed_key = 4
		else:
			self.pressed_key = None
			
	def set_pressed_state(self):
		if self.pressed_key == self.hotkey:
			self.image = self.buttons['button_down']
		else:
			self.image = self.buttons['button_up']
			
	def set_skill_image(self):
		if self.hotkey == 1:
			return self.skills['dagger']
		elif self.hotkey == 2:
			return self.skills['staff']
		elif self.hotkey == 3:
			return self.skills['bow']
		elif self.hotkey == 4:
			return self.skills['spear']
	
	def draw_skill_image(self, surface):
		surface.blit(self.skill_image, self.skill_image_rect)
	
	def update(self, input, surface):
		self.set_pressed_key(input)
		self.set_pressed_state()
		
		