import pygame

pygame.init()
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption('DIno jump')
clock = pygame.time.Clock()

background_position = 0
platform_position = 0



class ParallaxBG:
	
	def __init__(self, ground, sky):
		self.ground = ground
		#self.mountain = mountain
		self.sky = sky
		
	def foreground(self):
		global platform_position
		screen.blit(self.ground, (platform_position, 570))
		screen.blit(self.ground, (self.ground.get_width()+platform_position, 570))
		platform_position -=10
		if abs(platform_position)>self.ground.get_width():
			platform_position = 0
		
		
		
	"""
	def mountains(self):
	    global mountain_position
	    screen.blit(self.mountain, (mountain_position, 580))
	    screen.blit(self.mountain, (self.mountain.get_width() + mountain_position, 580))
	    mountain_position -= 6
	    if abs(mountain_position) > self.mountain.get_width():
		    mountain_position = 0"""
		
	def backsky(self):
	    global background_position
	    screen.blit(self.sky, (background_position, 240))
	    screen.blit(self.sky, (self.sky.get_width() + background_position, 240))
	    background_position -= 3
	    if abs(background_position) > self.sky.get_width():
		    background_position = 0
		
	def animate(self):	
		
		self.backsky()
		#self.mountains()
		self.foreground()
		