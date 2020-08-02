import pygame, sys
from random import randint
pygame.init()
screen = pygame.display.set_mode((1028, 480))


class Palikka(pygame.sprite.Sprite):
	def __init__(self, color, size, pos):
		pygame.sprite.Sprite.__init__(self)
		self.width, self.height = size
		
		# create rectangle
		self.image = pygame.Surface((self.width, self.height))
		self.image.fill((color))
		self.rect = self.image.get_rect()
		
		# starting point for the block. created with mouse click.
		self.rect.x = pos[0] - self.width / 2
		self.rect.y = pos[1] - self.height / 2
		
		# change the speed of the block (30fps x pixels)
		self.speed = 5
		
		# speed vectors
		self.x = 0
		self.y = self.speed
		
			
	def update(self):
		# create copy for block collision detection
		last = self.rect.copy()
		
		# move block
		self.rect.x += self.x
		self.rect.y += self.y
		
		# check to see that the block can change color after being hit
		self.block_hit = False
		
		# wall collision
		if self.rect.x < 0:
			self.x = self.speed
			self.block_hit = True
		elif self.rect.x > 1028 - self.width:
			self.x = -self.speed
			self.block_hit = True			
		elif self.rect.y < 0:
			self.y = self.speed
			self.block_hit = True
		elif self.rect.y > 480 - self.height:
			self.y = -self.speed
			self.block_hit = True
			
			
		# block collision
		global palikat
		new = self.rect
		block_hit_list = pygame.sprite.spritecollide(self, palikat, False)
		for cell in block_hit_list:
			cell = cell.rect
			if last.right <= cell.left and new.right > cell.left:
				new.right = cell.left
				self.x = -self.speed
				self.block_hit = True
			if last.left >= cell.right and new.left < cell.right:
				new.left = cell.right
				self.x = self.speed
				self.block_hit = True
			if last.bottom <= cell.top and new.bottom > cell.top:
				new.bottom = cell.top
				self.y = -self.speed
				self.block_hit = True
			if last.top >= cell.bottom and new.top < cell.bottom:
				new.top = cell.bottom
				self.y = self.speed	
				self.block_hit = True
				
			# change the color of the block	
			if self.block_hit == True:
				self.image.fill(color())
				
					
# get random color
def color():
	color = []
	for x in range(3):
		x = randint(0, 255)
		color.append(x)
	return color[:]

# get random size	
def get_size():
	
	return randint(10, 50), randint(10, 50)		

	

palikat = pygame.sprite.Group()

# main loop
while True:
	clock = pygame.time.Clock()	
	clock.tick(30)
	screen.fill((255, 255, 255))
	pos = pygame.mouse.get_pos()
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		if event.type == pygame.MOUSEBUTTONDOWN:
			palikka = Palikka(color(), get_size(), pos)
			palikat.add(palikka)
				

	palikat.update()
	palikat.draw(screen)	
	pygame.display.flip()
		


