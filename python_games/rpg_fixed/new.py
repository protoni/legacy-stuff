import pygame, sys, math
from random import randint
import datetime
import os

pygame.init()



class Bullet(pygame.sprite.Sprite):
	def __init__(self, pos, player, spell_file):
		pygame.sprite.Sprite.__init__(self)
		
		self.image = pygame.image.load(spell_file)
	
		self.rect = self.image.get_rect()
		
		self.pos = pos
		
		self.rect.x = player[0]
		self.rect.y = player[1]
		
		self.mouse_x, self.mouse_y = pos[0], pos[1]
		
		self.player = player
		
	def update(self, bullet_list):
		speed = 20.
		distance = [self.mouse_x - self.player[0], self.mouse_y - self.player[1]]
		norm = math.sqrt(distance[0] ** 2 + distance[1] ** 2)
		direction = [distance[0] / norm, distance[1 ] / norm]
		bullet_vector = [direction[0] * speed, direction[1] * speed]
		self.rect.x += bullet_vector[0]
		self.rect.y += bullet_vector[1]
		
		
		if self.rect.x < 0:
			pygame.sprite.Group.remove(bullet_list, self)
		if self.rect.x > 1028:
			pygame.sprite.Group.remove(bullet_list, self)
		if self.rect.y < 0:
			pygame.sprite.Group.remove(bullet_list, self)
		if self.rect.y > 480:
			pygame.sprite.Group.remove(bullet_list, self)

			
class Player():
	def __init__(self, screen):
		self.animation_calculator = 0
		self.sprite_animation_x = 0
		self.moving = False
		self.right = self.sprite_animation_x, 96
		self.left = self.sprite_animation_x, 48
		self.up = self.sprite_animation_x, 144
		self.down = self.sprite_animation_x, 0
		self.sprite_size = 32, 48
		
		
		self.sheet = r'C:\Users\ton\rpg\sprites\player.png'
		self.image = get_image(self.right, self.sprite_size, self.sheet)
		self.rect = self.image.get_rect()
		self.rect.x, self.rect.y = 400, 400
		
		self.screen = screen
		
		self.hp = 50
		self.hp_bar = pygame.Surface((self.hp, 7))
		self.hp_bar.fill((255, 0, 0))
		
		self.damage_taken = 0
		
		self.rect.x = 400
		self.rect.y = 400
		
		# damage done variable for stats
		self.damage_done = 0
		# enemies killed variable for stats
		self.enemies_killed = 0
	
		self.x = 5
		self.y = 5
		
		self.alive = True
		
		self.shooting = False
	
	def shooting_direction(self):
		# change image direction when shooting, changes with the angle
		import math
		mouseX, mouseY = pygame.mouse.get_pos()
		playerX, playerY = main.player.rect.x, main.player.rect.y
		angle = math.atan2(playerX-mouseX, playerY-mouseY)
		if angle > 0.75 and angle < 2.5:
			self.image = get_image(self.left, self.sprite_size, self.sheet)
		if angle > 2.5 or angle < -2.5:
			self.image = get_image(self.down, self.sprite_size, self.sheet)
		if angle > -2.5 and angle < -0.75:
			self.image = get_image(self.right, self.sprite_size, self.sheet)
		if angle < 0.75 and angle > -0.75:
			self.image = get_image(self.up, self.sprite_size, self.sheet)
	
	def update(self, bullet_list, enemy_list):
		# walking animations
		if self.moving:
			self.animation_calculator += 1
			if self.sprite_animation_x == self.sprite_size[0] * 3:
				# wait for the last animation image to animate for 5 frames time
				if self.animation_calculator > 5:
					self.sprite_animation_x = 0
					self.animation_calculator = 0
				
			if self.animation_calculator > 5:
				self.sprite_animation_x += self.sprite_size[0]
				self.animation_calculator = 0	
		else:
			self.sprite_animation_x = 0
			
		
		self.right = self.sprite_animation_x, 96
		self.left = self.sprite_animation_x, 48
		self.up = self.sprite_animation_x, 144
		self.down = self.sprite_animation_x, 0
		
		
		# Self.shooting == False prevents the movement keys from changing the
		# self.image direction while shooting. Resets after 10 frames
		
		pygame.font.init()
		last = self.rect.copy()
		self.moving = False
		key = pygame.key.get_pressed()
		if key[pygame.K_a]:
			self.moving = True
			self.rect.x -= self.x
			if self.shooting == False:
				self.image = get_image(self.left, self.sprite_size, self.sheet)
		if key[pygame.K_d]:
			self.moving = True
			self.rect.x += self.x
			if self.shooting == False:
				self.image = get_image(self.right, self.sprite_size, self.sheet)
		if key[pygame.K_w]:
			self.moving = True
			self.rect.y -= self.y
			if self.shooting == False:
				self.image = get_image(self.up, self.sprite_size, self.sheet)
		if key[pygame.K_s]:
			self.moving = True
			self.rect.y += self.y
			if self.shooting == False:
				self.image = get_image(self.down, self.sprite_size, self.sheet)
		
		
		# prevent the player from running through the enemy
		new = self.rect	
		enemy_hit_list = pygame.sprite.spritecollide(self, enemy_list, False)
		for cell in enemy_hit_list:
			cell = cell.rect
						
			if last.right <= cell.left and new.right > cell.left:
				new.right = cell.left
				
			if last.left >= cell.right and new.left < cell.right:
				new.left = cell.right
				
			if last.bottom <= cell.top and new.bottom > cell.top:
				new.bottom = cell.top
							
			if last.top >= cell.bottom and new.top < cell.bottom:
				new.top = cell.bottom
				
			
			
		if self.hp > self.damage_taken:
			if pygame.sprite.spritecollide(self, bullet_list, True):
				self.screen.fill((255, 255, 255))
				self.damage_taken += randint(1, 9)	
			
			if self.damage_taken > self.hp:
				self.damage_taken = self.hp	
			
			self.damage_bar = pygame.Surface((self.hp - self.damage_taken, 7))
			self.damage_bar.fill((0, 255, 0))
				
			self.screen.blit(self.hp_bar, (self.rect.x - 5, self.rect.y - 15))
			self.screen.blit(self.damage_bar, (self.rect.x - 5, self.rect.y - 15))
				
		else:
			self.alive = False
						
		
# print score to the board	
score = 0		
def print_score(screen):
	font = pygame.font.Font(None, 24)
	print_score = font.render('Score:  %d ' % (score), 1, (255, 255, 255))
	screen.blit(print_score, (60, 20))

	
# returns the right image from a sprite sheet	
def get_image(direction, size, file_name):
	x, y = direction
	width, lenght = size
	sprite_sheet = pygame.image.load(file_name)
	image = pygame.Surface([width, lenght]).convert()
	image.blit(sprite_sheet, (0, 0), (x, y, width, lenght))
	image.set_colorkey((0, 0, 0))
	return image
	
class Enemy(pygame.sprite.Sprite):
	def __init__(self, screen):
		pygame.sprite.Sprite.__init__(self)
		self.animation_calculator = 0
		self.sprite_animation_x = 0
		self.moving = False
		
		self.right = self.sprite_animation_x, 96
		self.left = self.sprite_animation_x, 48
		self.up = self.sprite_animation_x, 144
		self.down = self.sprite_animation_x, 0
		
		self.sprite_size = 50, 48
		
		# make enemy rectangle
		self.sheet = r'C:\Users\ton\rpg\sprites\death_scythe.png'
		self.image = get_image(self.right, self.sprite_size, self.sheet)
		self.rect = self.image.get_rect()
		self.rect.x, self.rect.y = self.random_spawn()
		
		self.screen = screen
		
		self.hp = 50
		self.hp_bar = pygame.Surface((self.hp, 7))
		self.hp_bar.fill((255, 0, 0))
		
		self.damage_taken = 0
		self.damage_overtime_counter = 0
		
		self.x = 5
		self.y = 5
		
		self.enemy_bullet_counter = 0
		self.bullet_counter = 40
		
	# get random coordinates for enemy spawn	
	def random_spawn(self):
		x = randint(0, 1028)
		y = randint(0, 480)
		player = main.player
		# add 100px spawn range
		if x < player.rect.x and x >= player.rect.x - 100:
			x -= 100
		if x > player.rect.x and x <= player.rect.x + 100:
			x += 100
		if y < player.rect.y and y >= player.rect.y - 100:
			y -= 100
		if y > player.rect.y and y <= player.rect.y + 100:
			y += 100
		
		return x, y
		
	
	def update(self, bullet_list, enemy_list):
		last = self.rect.copy()
		self.moving = False
		# calculate the x and y direction for bullet movement and move it
		speed = 2.
		distance = [main.player.rect.x - self.rect.x, main.player.rect.y - self.rect.y]
		norm = math.sqrt(distance[0] ** 2 + distance[1] ** 2)
		direction = [distance[0] / norm, distance[1 ] / norm]
		movement_vector = [direction[0] * speed, direction[1] * speed]
		self.rect.x += movement_vector[0]
		self.rect.y += movement_vector[1]
		
		new = self.rect
		cell = main.player.rect
		
		# check if player is moving
		if movement_vector[0] > 0.0 or movement_vector[1] > 0.0:
			self.moving = True
		
		# walking animations
		if self.moving:
			self.animation_calculator += 1
			if self.sprite_animation_x == self.sprite_size[0] * 3:
				# wait for the last animation image to animate for 5 frames time
				if self.animation_calculator > 5:
					self.sprite_animation_x = 0
					self.aimation_calculator = 0
				
			if self.animation_calculator > 5:
				self.sprite_animation_x += self.sprite_size[0]
				self.animation_calculator = 0
				
			self.right = self.sprite_animation_x, 96
			self.left = self.sprite_animation_x, 48
			self.up = self.sprite_animation_x, 144
			self.down = self.sprite_animation_x, 0
		else:
			self.sprite_animation_x = 0
		
		
		
		# limit the DOT damage with a counter
		if self.damage_overtime_counter > 10:
			
			# deal damage to player if touching
			if self.rect.colliderect(main.player.rect) and main.player.alive:
					main.player.damage_taken += 1
					self.damage_overtime_counter = 0
					
		self.damage_overtime_counter += 1
		
		# prevent the enemy from stomping on the player
		if last.right <= cell.left and new.right > cell.left:
			new.right = cell.left	
				
		if last.left >= cell.right and new.left < cell.right:
			new.left = cell.right
				
		if last.bottom <= cell.top and new.bottom > cell.top:
			new.bottom = cell.top
			
		if last.top >= cell.bottom and new.top < cell.bottom:
			new.top = cell.bottom
		
		
		# prevent the enemies from colliding with each other
		enemy_hit_list = pygame.sprite.spritecollide(self, enemy_list, False)
		for cell in enemy_hit_list:
			cell = cell.rect					
			if last.right <= cell.left and new.right > cell.left:
				new.right = cell.left
				
			if last.left >= cell.right and new.left < cell.right:
				new.left = cell.right
				
			if last.bottom <= cell.top and new.bottom > cell.top:
				new.bottom = cell.top			
				
			if last.top >= cell.bottom and new.top < cell.bottom:
				new.top = cell.bottom
			
		
		
		# get the right image for the direction enemy is moving
		if last.x > new.x:
			self.image = get_image(self.left, self.sprite_size, self.sheet)
		if last.x < new.x:
			self.image = get_image(self.right, self.sprite_size, self.sheet)
		if last.y < new.y:
			self.image = get_image(self.down, self.sprite_size, self.sheet)
		if last.y > new.y:
			self.image = get_image(self.up, self.sprite_size, self.sheet)
		
		if pygame.sprite.spritecollide(self, bullet_list, True):
			damage = randint(1, 9)
			self.damage_taken += damage	
			main.player.damage_done += damage
			
		if self.damage_taken < self.hp:
			self.damage = pygame.Surface((self.hp - self.damage_taken, 7))
			self.damage.fill((0, 255, 0))
			self.screen.blit(self.hp_bar, (self.rect.x + 5, self.rect.y - 15))
			self.screen.blit(self.damage, (self.rect.x + 5, self.rect.y - 15))
		else:
			pygame.sprite.Group.remove(enemy_list, self)
			main.player.enemies_killed += 1
			global score
			score += 10
		
		if self.enemy_bullet_counter > self.bullet_counter and main.player.alive:
			enemy_bullet = Bullet((main.player.rect.x, main.player.rect.y), [self.rect.x, self.rect.y], r'C:\Users\ton\rpg\sprites\enemy_spell.png')
			main.enemy_bullet_list.add(enemy_bullet)
			self.enemy_bullet_counter = 0
		
		self.enemy_bullet_counter += 1
		
# turha
class Console(object):
	def __init__(self, text):
		font = pygame.font.Font(None, 24)
		button = font.render(text, 1, (255, 255, 255))
			
		self.image = pygame.Surface([150, 50])
		self.image.blit(button, (0, 0))
		self.image.set_colorkey((0, 0, 0))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

def get_stats():
	global screen
	window = pygame.Surface([140, 150])
	window.fill((0, 50, 0))
	
	font = pygame.font.Font(None, 18)
	difficulty = font.render('Difficulty: %s' % main.difficulty_level, 1, (255, 255, 255))
	damage_done_stat = font.render('Damage done: %d' % main.player.damage_done, 1, (255, 255, 255))
	enemies_killed_stat = font.render('Enemies killed: %d' % main.player.enemies_killed, 1, (255, 255, 255))
	
	main.screen.blit(window, (10, 100))
	main.screen.blit(difficulty, (10, 110))
	main.screen.blit(damage_done_stat, (10, 140))
	main.screen.blit(enemies_killed_stat, (10, 170))
	
		






		
class Menu(object):
	
	def __init__(self, text, x, y, text_width):
		self.text = text
		font = pygame.font.Font(None, 70)
		button = font.render(self.text, 1, (255, 255, 255))
			
		self.image = pygame.Surface([text_width, 50])
		self.image.blit(button, (0, 0))
		self.image.set_colorkey((0, 0, 0))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		
	def	mouse_click(self):
		mouse_pos = pygame.mouse.get_pos()
		mouse_click = pygame.Rect(mouse_pos, (1, 1))
		return mouse_click

def print_difficulty(level):
	font = pygame.font.Font(None, 24)
	difficulty_level = font.render('Difficulty: %s' % level, 1, (255, 255, 255))
	main.screen.blit(difficulty_level, (400, 100))

# make death menu		
menu_items = ['Play Again', 'Main Menu', 'Quit']
items = []
gap = 0
for item in menu_items:
	x = Menu(item, 400, 200 + gap, 300)
	items.append(x)
	gap += 50
	

class Main():
	def __init__(self):
		scr_width = 1028
		scr_height = 480
		self.screen = pygame.display.set_mode((scr_width, scr_height), 0, 32)
	
		self.map = pygame.image.load(r'C:\Users\ton\rpg\sprites\map.jpg').convert()
		self.sheet = r'C:\Users\ton\rpg\sprites\Grue.png'
		self.image = get_image((0, 0), (56, 71), self.sheet)
		self.image_x, self.image_y = 300, 10
		self.move_x, self.move_y = 5, 0

		
		self.difficulty_pressed = False
		self.difficulty = ['Easy', 'Medium', 'Impossibru', 'Back']
		self.d_items = []
		self.difficulty_level = 'Easy'
		
		self.menu_items = ['Play', 'difficulty', 'Quit']
		self.items = []
		
		self.player = Player(self.screen)
		self.enemy_time_counter = 0	
		self.enemy_list = pygame.sprite.Group()
		self.player_bullet_list = pygame.sprite.Group()
		self.enemy_bullet_list = pygame.sprite.Group()
		self.bullet_counter = 0
		
	def menu_animation(self, image, move_x, move_y, image_x, image_y, sheet):
		right = 0, 0
		left = 0, 71
		up = 56, 0
		down = 56, 71
		size = 56, 71

		image_x += move_x
		image_y += move_y
		
		if move_x == 5 and image_x == 750:
			move_x = 0
			move_y = 5
			image = get_image(down, size, sheet)
		if move_y == 5 and image_y == 400:
			move_y = 0
			move_x = -5
			image = get_image(left, size, sheet)
		if move_x == -5 and image_x == 200:
			move_x = 0
			move_y = -5
			image = get_image(up, size, sheet)
		if move_y == -5 and image_y == 10:
			move_y = 0
			move_x = 5
			image = get_image(right, size, sheet)
		
		return image, image_x, image_y, move_x, move_y
	
	def menu(self):
	
		gap = 0	
		# create menu items
		for item in self.menu_items:
			x = Menu(item, 400, 200 + gap, 270)
			self.items.append(x)
			gap += 50
		gap = 0
		# create difficulty items
		for item in self.difficulty:
			x = Menu(item, 400, 200 + gap, 270)
			self.d_items.append(x)
			gap += 50
			
		# main loop
		while True:
			clock = pygame.time.Clock()	
			clock.tick(30)
			self.screen.blit(self.map, (0, 0))
			
			# main menu animation
			self.image, self.image_x, self.image_y, self.move_x, self.move_y = self.menu_animation(self.image, self.move_x, self.move_y, self.image_x, self.image_y, self.sheet)
			
			self.screen.blit(self.image, (self.image_x, self.image_y))
			
			if not self.difficulty_pressed:
				# draw menu texts
				for item in self.items:
					self.screen.blit(item.image, (item.rect.x, item.rect.y))
			
			if self.difficulty_pressed:
				for d_item in self.d_items:
					self.screen.blit(d_item.image, (d_item.rect.x, d_item.rect.y))
				
			
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()
				
				if self.difficulty_pressed:
					for menu in self.d_items:
						if menu.rect.colliderect(menu.mouse_click()):
							menu.image.set_colorkey((0, 0, 100))
							if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
								if menu.text == self.difficulty[0]:
									self.difficulty_level = 'Easy'
								if menu.text == self.difficulty[1]:
									self.difficulty_level = 'Medium'
								if menu.text == self.difficulty[2]:
									self.difficulty_level = 'Impossibru'
								if menu.text == self.difficulty[3]:
									self.difficulty_pressed = False
						else:	
							menu.image.set_colorkey((0, 0, 0))
								
				if not self.difficulty_pressed:				
					for menu in self.items:
						if menu.rect.colliderect(menu.mouse_click()):
							menu.image.set_colorkey((0, 0, 100))
							if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
								if menu.text == self.menu_items[0]:
									self.run()					
								if menu.text == self.menu_items[1]:
									self.difficulty_pressed = True
								if menu.text == self.menu_items[2]:
									sys.exit()		
						else:	
							menu.image.set_colorkey((0, 0, 0))
			
			# print difficulty
			if self.difficulty_pressed:
				print_difficulty(self.difficulty_level)
			
			pygame.display.flip()
	
	def run(self):
		
		
		# Timer for delaying walking animation after shooting.
		# After this timer player.shooting changes to False and
		# walking animations are available when pressing movement keys.
		shooting_direction_timer = 0
		
		if self.difficulty_level == 'Easy':
			enemy_spawn = 80
		if self.difficulty_level == 'Medium':
			enemy_spawn = 50
		if self.difficulty_level == 'Impossibru':
			enemy_spawn = 20
			
		while True:
			clock = pygame.time.Clock()	
			clock.tick(30)
			self.screen.blit(self.map, (0, 0))
						
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()
			# create a bullet when clicking mouse button
			# add shooting delay and prevent the player from shooting if dead
			pos = pygame.mouse.get_pos()
			mouse = pygame.mouse.get_pressed()
			if self.bullet_counter > 4:		
				if mouse[0] and self.player.alive:
					bullet = Bullet(pos, [self.player.rect.x, self.player.rect.y], r'C:\Users\ton\rpg\sprites\spell.png')
					self.player_bullet_list.add(bullet)
					self.bullet_counter = 0
					self.player.shooting_direction()
					self.player.shooting = True
					shooting_direction_timer = 0
			self.bullet_counter += 1
			
			if self.player.shooting == True and shooting_direction_timer > 10:
				self.player.shooting = False
				shooting_direction_timer = 0
			shooting_direction_timer += 1
			
			# reduce enemy spawn. spawn every x frames / 30fps. Stops spawning enemies if the player is dead.
			if self.enemy_time_counter > enemy_spawn and self.player.alive:
				enemy = Enemy(self.screen)
				self.enemy_list.add(enemy)
				self.enemy_time_counter = 0
			self.enemy_time_counter += 1
						
						
			# update stuff and things
			self.enemy_list.update(self.player_bullet_list, self.enemy_list)
			self.player_bullet_list.update(self.player_bullet_list)
			self.enemy_bullet_list.update(self.enemy_bullet_list)
						
							
			# print HP
			font = pygame.font.Font(None, 24)
			print_hp = font.render('HP:  %d ' % (self.player.hp - self.player.damage_taken), 1, (255, 255, 255))
			self.player.screen.blit(print_hp, (900, 20))
						
						
			# draw stuff and things
			self.enemy_list.draw(self.screen)
			self.screen.blit(self.player.image, (self.player.rect.x, self.player.rect.y))
			self.player_bullet_list.draw(self.screen)
			self.enemy_bullet_list.draw(self.screen)
			print_score(self.screen)
					
			key = pygame.key.get_pressed()
			if key[pygame.K_TAB]:
				get_stats()
				
			# only update player if it's alive, else print death animation	
			if self.player.alive:
				self.player.update(self.enemy_bullet_list, self.enemy_list)
			else:
				self.death_screen()
					
			pygame.display.flip()

	
	def death_screen(self):
		date = datetime.date.today()
		
		if os.path.isfile('highscores.txt') == True:
			with open('highscores.txt', 'r') as f:
				line = f.readline()
				piste = line[:2]
			
			with open('highscores.txt', 'r+') as f:
				if score > int(piste):
					line = str(score) + '     ' + str(date)
					for l in line:
						f.write(l)
				
					
		else:
			with open('highscores.txt', 'w') as f:
				f.write(str(score) + '     ' + str(date))
		
		for item in items:
			self.screen.blit(item.image, (item.rect.x, item.rect.y))
							
		mouse_pressed = pygame.mouse.get_pressed()
		for menu in items:
			if menu.rect.colliderect(menu.mouse_click()):	
				menu.image.set_colorkey((0, 0, 100))
				
				if mouse_pressed[0]:
					if menu.text == menu_items[0]:
						play_again()	
					if menu.text == menu_items[1]:
						break
					if menu.text == menu_items[2]:
						sys.exit()
			else:
				menu.image.set_colorkey((0, 0, 0))
		
		self.player.screen.blit(self.player.damage_bar, (self.player.rect.x - 5, self.player.rect.y - 15))
		self.player.sheet = r'C:\Users\ton\rpg\sprites\player_dead.png'
		self.player.dead = 96, 0
		self.player.sprite_size = 48, 32
		self.player.image = get_image(self.player.dead, self.player.sprite_size, self.player.sheet)
		
		dead_font = pygame.font.Font(None, 70)
		game_over = dead_font.render('Game Over', 1, (255, 255, 255))
		self.screen.blit(game_over, (400, 0))	
		
	

def play_again():
	main = Main()
	main.run()		
		
while True:
	main = Main()
	main.menu()



# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# #
# # 	LISAA TOIMINTOJA
# #	
# # - vihuille spawn range  OK
# # 
# # - main menuun taytetta  OK
# #
# # - kavelyanimaatiot  OK
# #
# # - valikoille mouseover highlight  OK
# #
# # - lisaa kenttia
# #
# # - kenttiin taytetta
# #
# # - pisteraja kentille
# #
# #	- statsit (damge ja tapot)  OK
# #
# # - console
# #
# # - random damage  OK
# #
# # - damage done / damage taken combat text
# #
# # - vaikeustason valinta OK
# #
# # - highscoret, tallennus tekstitiedostoon
# #
# # - experience ja levelit
# #
# #
# #
# #		BUGEJA
# #
# # - pelin restart ei toimi kuoleman jalkeen OK
# # 
# # - vihuja spawnaa pelaajan paalle ja peli kaatuu  OK
# # 
# # - pelaaja ei kuole 0hp:lla  OK
# #
# # - pelaaja ei kaanny hiirta kohti castatessa  OK
# #
# # - valikkojen napit ei valilla toimi OK
# #
# # - vihut kulkevat paallekkain  OK
# #
# # - kavelyanimaatiot valilla tekee pelaajan ja vihut nakymattomiks  OK
# #
# #
# #		PARANNUKSIA KOODIIN
# #
# # - pelin pitaisi toimia classi instancena eika global variableilla. run()
# #
# # - pelin uudelleen aloitus uudella classi instancella, eika nollaamalla global variableja. death_screen()
# #
# # - magic numberit pois
# #
# # - collision funktio ettei tarvi jokaista kirjottaa uudestaan
# #
# #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 




	
		

