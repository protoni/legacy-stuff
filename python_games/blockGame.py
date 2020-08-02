import pygame, sys
from random import randint
import math
pygame.init()
screen = pygame.display.set_mode((1028, 480))


class Walls(pygame.sprite.Sprite):
	def __init__(self, pos):
		pygame.sprite.Sprite.__init__(self)
		self.width = 15
		self.height = 15
		self.image = pygame.Surface((self.width, self.height))
		self.image.fill((0, 200, 0))
		self.rect = self.image.get_rect()
		self.rect.x = pos
		self.rect.y = 480 - self.height
		
# make walls for the game		
wall_list = pygame.sprite.Group()		
def make_walls():
	for i in range (0, 1028, 15):
		wall = Walls(i)
		wall_list.add(wall)
make_walls()	

	
class Player(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.width = 15
		self.height = 15
		self.image = pygame.Surface((self.width, self.height))
		self.image.fill((0, 0, 0))
		self.rect = self.image.get_rect()
		
		# starting point for the player.
		self.rect.x = 500
		self.rect.y = 200
		
		#gravity
		self.resting = False
		self.dy = 0
		#speed
		self.speed = 5
		
	def update(self, dt, wall_list, palikat):
		key = pygame.key.get_pressed()
		last = self.rect.copy()
		if key[pygame.K_a]:
			self.rect.x -= 300 * dt
		if key[pygame.K_d]:
			self.rect.x += 300 * dt
		if self.resting and key[pygame.K_SPACE]:
			self.dy = -500
				
		self.dy = min(400, self.dy + 40)
		self.rect.y += self.dy * dt
		
		
		# check collision with walls
		new = self.rect
		self.resting = False
		block_hit_list = pygame.sprite.spritecollide(self, wall_list, False)
		for cell in block_hit_list:
			cell = cell.rect
			if last.right <= cell.left and new.right > cell.left:
				new.right = cell.left
				
			if last.left >= cell.right and new.left < cell.right:
				new.left = cell.right
				
			if last.bottom <= cell.top and new.bottom > cell.top:
				self.resting = True
				new.bottom = cell.top
				self.dy = 0
				
			if last.top >= cell.bottom and new.top < cell.bottom:
				new.top = cell.bottom
				self.dy = 0
				
		# check collision with blocks	
		block_hit_list = pygame.sprite.spritecollide(self, palikat, False)
		for cell in block_hit_list:
			cell = cell.rect
			if last.right <= cell.left and new.right > cell.left:
				new.right = cell.left
							
			if last.left >= cell.right and new.left < cell.right:
				new.left = cell.right
				
			if last.bottom <= cell.top and new.bottom > cell.top:
				self.resting = True
				new.bottom = cell.top
				self.dy = 0
			
			if last.top >= cell.bottom and new.top < cell.bottom:
				new.top = cell.bottom
				self.dy = 0
				
		
			

class Palikka(pygame.sprite.Sprite):
	def __init__(self, pos):
		pygame.sprite.Sprite.__init__(self)
		self.width, self.height = 15, 15
		
		# create rectangle
		self.image = pygame.Surface((self.width, self.height))
		self.image.fill((0, 200, 0))
		self.rect = self.image.get_rect()
		
		# starting point for the block. created with mouse click.
		self.rect.x = pos[0] - self.width / 2
		self.rect.y = pos[1] - self.height / 2
		
		# change the speed of the block (30fps x pixels)
		self.speed = 5
		
		# speed vectors
		self.x = 0
		self.y = self.speed
		
			
	def update(self, wall_list, bullet_list):
		# create copy for block collision detection
		last = self.rect.copy()
		
		# move block
		self.rect.x += self.x
		self.rect.y += self.y
		
		new1 = self.rect
		# wall collision
		global palikat
		block_hit_list = pygame.sprite.spritecollide(self, palikat, False)
		for cell in block_hit_list:
			cell = cell.rect
			if last.right <= cell.left and new1.right > cell.left:
				new1.right = cell.left
				
			if last.left >= cell.right and new1.left < cell.right:
				new1.left = cell.right
				
			if last.bottom <= cell.top and new1.bottom > cell.top:
				new1.bottom = cell.top
				
			if last.top >= cell.bottom and new1.top < cell.bottom:
				new1.top = cell.bottom			
			
		# block collision
	
		new = self.rect
		block_hit_list = pygame.sprite.spritecollide(self, wall_list, False)
		for cell in block_hit_list:
			cell = cell.rect
			if last.right <= cell.left and new.right > cell.left:
				new.right = cell.left
				
			if last.left >= cell.right and new.left < cell.right:
				new.left = cell.right
				
			if last.bottom <= cell.top and new.bottom > cell.top:
				new.bottom = cell.top
				
			if last.top >= cell.bottom and new.top < cell.bottom:
				new.top = cell.bottom
				
			new1 = self.rect
		# wall collision
		
		pygame.sprite.spritecollide(self, bullet_list, True)
	
				
class Bullet(pygame.sprite.Sprite):
	def __init__(self, pos, player):
		pygame.sprite.Sprite.__init__(self)
		self.width = 10
		self.height = 10
		self.image = pygame.Surface((self.width, self.height))
		self.image.fill((255, 0, 0))
		self.rect = self.image.get_rect()
		self.pos = pos
		self.rect.x = player[0] - Player().width / 2
		self.rect.y = player[1]
		self.move_x = 0
		self.move_y = 0
		
		self.mouse_x, self.mouse_y = pos[0], pos[1]
		self.player = player

	
			
		
	def update(self, palikat):
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
		
		# remove bullet when it hits a block
		pygame.sprite.spritecollide(self, palikat, True)
		
		
bullet_list = pygame.sprite.Group()	

palikat = pygame.sprite.Group()

player_list = pygame.sprite.Group()
player_in_game = False

bullet_counter = 0
# main loop
while True:
	clock = pygame.time.Clock()	
	dt = clock.tick(30)
	screen.fill((255, 255, 255))
	pos = pygame.mouse.get_pos()
	mouse = pygame.mouse.get_pressed()
	key = pygame.key.get_pressed()
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
			
	if key[pygame.K_LCTRL]:
		if player_in_game == False:
			player = Player()
			player_list.add(player)
			player_in_game = True
			
	if mouse[2]:
		palikka = Palikka(pos)
		palikat.add(palikka)	
	
	if bullet_counter > 20:
		if mouse[0]:
			bullet = Bullet(pos, [player.rect.x, player.rect.y])
			bullet_list.add(bullet)
			bullet_counter = 0
	
	
	wall_list.draw(screen)
	
	#limit the bullet count
	bullet_counter += 10
	
	bullet_list.update(palikat)
	bullet_list.draw(screen)
	
	player_list.update(dt / 1000., wall_list, palikat)
	player_list.draw(screen)
	
	palikat.update(wall_list, bullet_list)
	palikat.draw(screen)	
	pygame.display.flip()
		


