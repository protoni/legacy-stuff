import pygame, sys
from random import randint
pygame.init()
screen = pygame.display.set_mode((1028, 480))

class Pallo(object):
	def __init__(self, pos):
		self.color = self.color()
		self.pos = pos
		self.radius = self.radius()
		self.thickness = 0
		self.paikka = self.paikka()
		self.x = 0
		self.y = 5
		
	def color(self):
		color = []
		for x in range(3):
			x = randint(0, 255)
			color.append(x)
		return color[:]
	
	def paikka(self):
		paikka = []
		paikka.append(self.pos[0])
		paikka.append(self.pos[1])	
		return paikka[:]
		
	def radius(self):
		
		return randint(10, 100)
	
	def update(self):
		self.collision()
		self.paikka[0] += self.x
		self.paikka[1] += self.y
		
	
	def collision(self):
		'''wall collision'''
		if self.paikka[0] < 0 + self.radius:
			self.x = 5
		elif self.paikka[0] > 1028 - self.radius:
			self.x = -5
		elif self.paikka[1] < 0 + self.radius:
			self.y = 5
		elif self.paikka[1] > 480 - self.radius:
			self.y = -5

pallot = []
pallo_coords = []
	
while True:
	clock = pygame.time.Clock()	
	clock.tick(30)
	pos = pygame.mouse.get_pos()	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		if event.type == pygame.MOUSEBUTTONDOWN:
			pallo = Pallo(pos)
			pallot.append(pallo)
	
					
	screen.fill((255, 255, 255))
	for i in pallot:
		pygame.draw.circle(screen, i.color, i.paikka, i.radius, i.thickness)
		i.update()
		
	pygame.display.flip()
		


