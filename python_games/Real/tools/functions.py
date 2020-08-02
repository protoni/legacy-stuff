import pygame
import math, os
from . import *
import constants as c

'''--------------------------global functions--------------------------------'''

def world_to_pixel_coordinates(target, viewport):
	# return new rectangle with world coordinates transformed to pixel coordinates
	new_x = target.rect.x - viewport.x
	new_y = target.rect.y - viewport.y
	width, height = size = target.image.get_size()
	target_rect = pygame.Rect(new_x, new_y, width, height)
	return target_rect
	
def game_object_coordinates_transform(target, viewport):
	# change game objects coordinates when the viewport is moving
	world_x = viewport.x + target.x
	world_y = viewport.y + target.y
	move_x = target.x + viewport.x
	move_y = target.y + viewport.y
	target_x = world_x - move_x
	target_y = move_y - move_y
	new_x = target_x + target.x
	new_y = target_y + target.y
	return new_x, new_y

def	mouse_click():
	# create and return (1, 1) pixel wide rectangle of the mouse position
	mouse_pos = pygame.mouse.get_pos()
	mouse_click = pygame.Rect(mouse_pos, (1, 1))
	return mouse_click
		
def get_image(direction, size, file_name):
	# returns the right image from a sprite sheet
	x, y          = direction
	width, lenght = size
	sprite_sheet  = file_name
	image         = pygame.Surface([width, lenght]).convert()
	image.blit(sprite_sheet, (0, 0), (x, y, width, lenght))
	image.set_colorkey((0, 0, 0))
	return image
	
def get_movement_vector_non_strafe(x, y, self_x, self_y, speed):
	# return x, y direction can strafe
	distance = [x - self_x, y - self_y]
	norm = math.sqrt(distance[0] ** 2 + distance[1] ** 2)
	direction = [distance[0] / norm, distance[1 ] / norm]
	movement_vector = [direction[0] * speed, direction[1] * speed]
	return movement_vector
			
def get_movement_vector(x, y, self_x, self_y, speed):
	#return x, y direction, cannot strafe
	distance = [x - self_x, y - self_y]
	if distance == 0:
		distance = 0.1
	norm = math.sqrt(distance[0] ** 2 + distance[1] ** 2)
	if norm == 0:
		norm = 0.1
	direction = [distance[0] / norm, distance[1 ] / norm]
	movement_vector = [direction[0] * speed, direction[1] * speed]
	if self_x > x:
		return -speed, 0
	elif self_x < x:
		return speed, 0
	elif self_y > y:
		return 0, -speed
	elif self_y < y:
		return 0, speed
	else:
		return movement_vector
		
def focus(self_x, self_y, enemy_x, enemy_y):
	# change image direction towards target
	angle = math.atan2(self_x - enemy_x, self_y - enemy_y)
	if angle > 0.75 and angle < 2.5:
		return c.left
	if angle > 2.5 or angle < -2.5:
		return c.down
	if angle > -2.5 and angle < -0.75:
		return c.right
	if angle < 0.75 and angle > -0.75:
		return c.up
		
def change_direction(last, new, sprite):
	# change image direction when moved
	if last.x > new.x:
		sprite.direction = c.left
	if last.x < new.x:
		sprite.direction = c.right
	if last.y < new.y:
		sprite.direction = c.down
	if last.y > new.y:
		sprite.direction = c.up
	
	
'''----------------------------------------------------------------------------'''