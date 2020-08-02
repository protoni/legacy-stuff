from . import *
import constants as c
from tools import functions as f

class Spritesheet(object):
	# all_spritesheets_dict = 'walk' : {direction_dict}
	# direction_dict        = 'right' : {right_dict}
	# right_dict            = 'walk' : [animation_list]
	# loop [animation_list] to animate 'walk' to 'right'
	
	def __init__(self, spritesheets, sprite):
		self.spritesheets = spritesheets
		self.sheet = spritesheets[sprite.action]
		self.sprite = sprite
		self.timer = 0.0
		self.index = 0
		self.end_of_row = False
		self.animation_done = True
		self.actions_list = ['spell', 'thrust', 'walk', 'slash', 'shoot']
						
		self.col_dict = {'spell' : 7, 'thrust' : 8,
						 'walk' : 9, 'slash' : 6,
						  'shoot' : 13}
						  
		self.all_spritesheets_dict = self.make_all_spritesheets_dict()
		
	def make_all_spritesheets_dict(self):
		all_spritesheets_dict = {}
		for action in self.actions_list:
			all_spritesheets_dict[action] = self.make_sheet_dict(self.spritesheets[action])
		return all_spritesheets_dict
		
	def make_sheet_dict(self, sheet):
		sheet_size = sheet.get_size()
		cols = 13
		rows = 21
		width = sheet_size[0] / cols
		height = sheet_size[1] / rows
		x, y = 0, 0
		up_dict = {}
		left_dict = {}
		down_dict = {}
		right_dict = {}
		action_index = 0
		row_calc = 0
		for row in range(rows):	
			action = self.actions_list[action_index]
			row_calc += 1
			animation_list = self.make_sheet_list(self.col_dict[action], x, y, width, height, sheet)
			if row_calc == 1:
				up_dict[action] = animation_list
			if row_calc == 2:
				left_dict[action] = animation_list
			if row_calc == 3:
				down_dict[action] = animation_list
			if row_calc == 4:
				right_dict[action] = animation_list	
			y += height		
			if row_calc == 4:
				row_calc = 0
				action_index += 1
				if action_index > 4:
					break
		direction_dict = {'up' : up_dict, 'left' : left_dict,
						  'down' : down_dict, 'right' : right_dict}
		
		return direction_dict
		
	def make_sheet_list(self, cols, x, y, width, height, sheet):
		sprite_list = []
		for col in range(cols):
			sprite_list.append(f.get_image((x, y), (width, height), sheet))
			x += width
		return sprite_list
			
	def animate(self):
		directions_dict = self.all_spritesheets_dict[self.sprite.action]
		actions_dict    = directions_dict[self.sprite.direction]
		animation       = actions_dict[self.sprite.action]
		self.sprite.animation_index = self.index # give sprite classes index number of spritelists so they can time spell creation
		cols = self.col_dict[self.sprite.action] - 1
		if self.sprite.charging:
			animation = actions_dict[c.walk]
			cols = self.col_dict[c.walk] - 1
		if self.index >= cols:
			self.end_of_row = True		
		if self.sprite.moving or self.sprite.attacking:
			self.timer += 1
			if self.end_of_row: # animate the last image for 5frames
				if self.timer >= 5:
					self.index = 0
					self.timer = 0.0
					self.end_of_row = False
					self.sprite.attacking = False
			if self.timer >= 5:
				self.index += 1
				self.timer = 0.0
			return animation[self.index]
		self.index = 0
		return animation[self.index]
		