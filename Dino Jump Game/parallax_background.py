import pygame

all_platforms= pygame.sprite.Group()

pygame.init()
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption('DIno jump')
clock = pygame.time.Clock()

background_position = 0
platform_position = 0
mountain_position = 0

class ParallaxBG(pygame.sprite.Sprite):
	def __init__(self, ground, mountain, sky):
		super().__init__()
		self.ground = ground
		self.mountain = mountain
		self.sky = sky
		
	def foreground(self):
		global platform_position
		screen.blit(self.ground, (platform_position, 330))
		screen.blit(self.ground, (self.ground.get_width()+platform_position, 330))
		platform_position -=10
		if abs(platform_position)>self.ground.get_width():
			platform_position = 0
		
	def mountains(self):
	    global mountain_position
	    screen.blit(self.mountain, (mountain_position, 290))
	    screen.blit(self.mountain, (self.mountain.get_width() + mountain_position, 290))
	    mountain_position -= 5
	    if abs(mountain_position) > self.mountain.get_width():
		    mountain_position = 0
		
	def backsky(self):
	    global background_position
	    screen.blit(self.sky, (background_position, 240))
	    screen.blit(self.sky, (self.sky.get_width() + background_position, 240))
	    background_position -= 3
	    if abs(background_position) > self.sky.get_width():
		    background_position = 0
		
	def animate(self):	
		self.backsky()
		self.mountains()
		self.foreground()
		