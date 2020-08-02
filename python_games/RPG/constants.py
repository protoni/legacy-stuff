import pygame

SCREEN = pygame.display.set_mode((1028, 578))


#states
menu = 'menu'
game = 'game'
gameover = 'gameover'

	
#levels
level1 = 'level1'
level2 = 'level2'


#framework
unit_gap = 250
unit_x = 50
unit_y = 50
unit_width = 70
unit_height = 20
thickness = 1
fill = 0
white = (255, 255, 255)
red   = (255, 0,     0)
green = (0,   255,   0)
blue  = (0,   0,   255)
black = (0,   0,     0)


#directions
left  = 'left'
right = 'right'
up    = 'up'
down  = 'down'
horizontal = 'horizontal'
vertical   = 'vertical'


#actions
spell = 'spell'
thrust = 'thrust'
shoot = 'shoot'
walk = 'walk'
slash = 'slash'
hurt = 'hurt'