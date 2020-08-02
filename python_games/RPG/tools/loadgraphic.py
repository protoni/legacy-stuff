import pygame
import os

'''-----------------------------------------game objects------------------------------------------------'''

def load_arrow_graphic():
	arrows = {'arrow' : pygame.image.load(os.path.join('graphics', 'WEAPON_arrow.png')),
			  'arrow_double' : pygame.image.load(os.path.join('graphics', 'WEAPON_arrow_double.png')),
			  'arrow_fire' : pygame.image.load(os.path.join('graphics', 'WEAPON_arrow_fire2.png'))}
	return arrows

def load_spell_graphic():
	spells = {'fireball' : pygame.image.load(os.path.join('graphics', 'flame_fire.png')),
			  'lightning' : pygame.image.load(os.path.join('graphics', 'light_glow_effect.png')),
			  'fire' : pygame.image.load(os.path.join('graphics', 'ring_fire.png'))}
	return spells

'''----------------------------------------------characters------------------------------------------------'''
	
def load_enemy_spritesheet_graphic():
	spritesheets = {'slash' : pygame.image.load(os.path.join('graphics', 'index2.png')),
					'shoot' : pygame.image.load(os.path.join('graphics', 'index2.png')),
					'thrust' : pygame.image.load(os.path.join('graphics', 'index2.png')),
					'walk' : pygame.image.load(os.path.join('graphics', 'index2.png')),
					'spell' : pygame.image.load(os.path.join('graphics', 'index2.png'))}
	return spritesheets

def load_player_spritesheet_graphic():
	spritesheets = {'slash' : pygame.image.load(os.path.join('graphics', 'player_dagger.png')),
					'shoot' : pygame.image.load(os.path.join('graphics', 'player_bow.png')),
					'thrust' : pygame.image.load(os.path.join('graphics', 'player_spear.png')),
					'walk' : pygame.image.load(os.path.join('graphics', 'player_bow.png')),
					'spell' : pygame.image.load(os.path.join('graphics', 'player_bow.png'))}
	return spritesheets

'''------------------------------------------------UI-------------------------------------------------------'''
	
def load_unit_frame_graphic():
	empty = pygame.image.load(os.path.join('graphics', 'bar1.png'))
	full = pygame.image.load(os.path.join('graphics', 'bar2.png'))
	return empty, full

def load_skill_bar_graphic():
	buttons = {'button_up' : pygame.image.load(os.path.join('graphics', 'skill_button_up.png')),
			   'button_down' : pygame.image.load(os.path.join('graphics', 'skill_button_down.png'))}
				
	skills = {'dagger' : pygame.image.load(os.path.join('graphics', 'dagger.png')),
			  'staff' : pygame.image.load(os.path.join('graphics', 'staff.png')),
			  'bow' : pygame.image.load(os.path.join('graphics', 'bow.png')),
			  'spear' : pygame.image.load(os.path.join('graphics', 'spear.png'))}
	return buttons, skills
	
'''-----------------------------------------------menu-------------------------------------------------------'''	

def load_menu_graphic():
	menu_graphics = {'button_solid' : pygame.image.load(os.path.join('graphics', 'button_solid.png')),
					 'button_hover' : pygame.image.load(os.path.join('graphics', 'button_hover.png')),
					 'button_pressed' : pygame.image.load(os.path.join('graphics', 'button_pressed.png')),
					 'button_background' : pygame.image.load(os.path.join('graphics', 'button_background.png')),
					 'menu_background_big' : pygame.image.load(os.path.join('graphics', 'menu1.png')),
					 'menu_background_small' : pygame.image.load(os.path.join('graphics', 'menu2.png'))}
	return menu_graphics