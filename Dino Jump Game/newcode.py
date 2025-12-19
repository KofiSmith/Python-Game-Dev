#THIS GAME IS BASED ON THE CHROME DINOSAUR RUN GAME
import pygame

all_sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()

import random
from parallax_background import ParallaxBG

#initializing pygame
pygame.init()
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption('Dino Run')
clock = pygame.time.Clock()


#LOADING AND TRANSFORMING BACKGROUND IMAGE
background = pygame.image.load('backsky1.jpg').convert()
background = pygame.transform.scale(background, (800,420))
background_position = 0


#LOADING AND TRANSFORMING MOUNTAIN IMAGE
mountain = pygame.image.load('mountain1.jpg').convert()
mountain = pygame.transform.scale(mountain, (800,400))
mountain.set_colorkey((0,0,0))
mountain_position = 0


#LOADING AND TRANSFORMING PLATFORM IMAGE
platform= pygame.image.load('foreground1.jpg').convert_alpha()
platform.set_colorkey((0,0,0))
platform = pygame.transform.scale(platform, (800,400))
platform_position = 0

background = ParallaxBG(platform, mountain, background)



#LOADING AND TRANSFORMING DINOSAUR IMAGE
dino_walk1 = pygame.image.load('dino_walk1.jpg').convert_alpha()
dino_walk2 = pygame.image.load('dino_walk2.jpg').convert_alpha()
dinosaur_jump = pygame.image.load("dino_jump.jpg").convert_alpha()

dino_walk1 = pygame.transform.scale(dino_walk1, (100,100))
dino_walk2 = pygame.transform.scale(dino_walk2, (100,100))
dinosaur_jump=  pygame.transform.scale(dinosaur_jump,(100,100))

#Setting animation frame for dinosaur
dino_frames = [dino_walk1, dino_walk2]
dinosaur_index = 0
dino_rect = dinosaur_jump.get_rect(midbottom=(80, 680))

#Function below animates the dinosaur 
def dino_animation():
	global dinosaur, dinosaur_index
	if dino_rect.bottom<615:
		dinosaur = dinosaur_jump
	else:
		dinosaur_index +=0.2
		if dinosaur_index >= len(dino_frames):
			dinosaur_index = 0
		dinosaur = dino_frames[int(dinosaur_index)]

dino_animation()
dino_rect = dinosaur.get_rect(midbottom=(100, 680))


#PTEROSAUR OBSTACLE 
pterosaur1 = pygame.image.load("pterosaur1.jpg").convert_alpha()
pterosaur2 = pygame.image.load("pterosaur2.jpg").convert_alpha()
pterosaur1 = pygame.transform.scale(pterosaur1,(120,90))
pterosaur2 = pygame.transform.scale(pterosaur2,(120,90))


#METEOR OBSTACLE
meteor1 = pygame.image.load("meteor1.jpg").convert_alpha()
meteor2 = pygame.image.load("meteor2.jpg").convert_alpha()
meteor1 = pygame.transform.scale(meteor1,(130, 55))
meteor2 = pygame.transform.scale(meteor2,(130,55))


		
class Obstacles(pygame.sprite.Sprite):
	def __init__(self, img1, img2, midbottom_pos):  
		super().__init__()
		self.img1 = img1
		self.img2 = img2
		self.frames = [img1, img2] 
		self.frame_index = 0  
		self.image = img1
		#Store position as rect
		self.rect = self.image.get_rect(midbottom=midbottom_pos)  
		self.animation_speed = 0.15
		
	def animation(self):
		# Update frame index
		self.frame_index += self.animation_speed
		if self.frame_index >= len(self.frames):
			self.frame_index = 0
		
		# Update current image
		self.image = self.frames[int(self.frame_index)]
		
		# Keep the same position when changing frames
		current_pos = self.rect.midbottom
		self.rect = self.image.get_rect(midbottom=current_pos)
		
	def attack(self):
		# Move the obstacle
		self.rect.left -= 15
		
		# Reset position when off screen
		#if self.rect.right <= 0:
			#self.rect.left = 800
			
		# Draw to screen (usually this would be in main game loop)
		# screen.blit(self.image, self.rect)
		
	def update(self):
		# Common pattern: update animation and movement together
		self.animation()
		self.attack()    
		
meteor = Obstacles(meteor1,meteor2,(800,655)) 
pterosaur = Obstacles(pterosaur1, pterosaur2,(800,530))


all_sprites.add(meteor) 
#all_sprites.add(pterosaur)   

obstacle_list= [meteor,pterosaur]

def change_sprite():
    rand = random.randint(0,1)
    for sprite in all_sprites.sprites():
        all_sprites.update()
        all_sprites.draw(screen)
        if sprite.rect.right<=0:
            
            #rand = random randint(1,2)
            all_sprites.empty()
            all_sprites.add(obstacle_list[rand])
            sprite.rect.right=800
            #all_sprites.update()
            #all_sprites.draw(screen)


#USE SPRITE GROUP TO CHECK IF THE ENEMY SPRITE IS STILL ON SCREEN, IF ENEMY SPRITE IS OFF THE SCREEN THEN YOU GENERATE ANOTHER RANDOM ENEMY


#SCORE COUNTER
score_font = pygame.font.SysFont('Arial', 35)

def display_score():
	global curr_time
	curr_time = int((pygame.time.get_ticks()/1000)*10)
	score_surf = score_font.render(f"Score: {curr_time}", False, (0,0,0))
	score_rect = score_surf.get_rect(midleft=(30,270))
	pygame.draw.rect(screen,"#2AD2F2", score_rect)
	pygame.draw.rect(screen, "#2AD2F2", score_rect,10)
	screen.blit(score_surf, score_rect)
	return curr_time


high_score = 0				
with open('high_score.txt', 'r') as file:
	high_score = int(file.readline())

high_score_font = pygame.font.SysFont('Arial', 23)
high_score_surf = high_score_font.render(f'High Score: {high_score}', False, (0,0,0))

def add_high_score():
	with open("high_score.txt", 'w') as file:
		file.write(f'{high_score}')
	file.close()

def display_high_score():
	high_score_rect = high_score_surf.get_rect(midleft=(30, 320))
	pygame.draw.rect(screen, "#2AD2F2", high_score_rect)
	pygame.draw.rect(screen, "#2AD2F2", high_score_rect,10)
	screen.blit(high_score_surf, high_score_rect)



#GAME OVER MESSAGE

game_over_message_font = pygame.font.SysFont('Arial', 65)
game_over_message= game_over_message_font.render(f"Game Over", True, (0,0,0))
game_over_score_rect=game_over_message.get_rect(center=(380,500))
game_over_score_font = pygame.font.SysFont('Arial', 35)
high_score_info = pygame.font.SysFont('Arial', 35)

def game_over_display():
	background.animate()
	#Creating game over score rect
	game_over_score = game_over_score_font.render(f"You scored: {score}", False, (0,0,0))
	game_over_high_score_info = high_score_info.render(f'High Score: {high_score}', False, (0,0,0))
	#Dislaying Game Over text on game over screen
	screen.blit(game_over_message,(180,350))
	screen.blit(game_over_score,game_over_score_rect)
	screen.blit(game_over_high_score_info, (240, 510))



#SOUNDS
sound = pygame.mixer.Sound('sound.mp3')
sound.play()
jump_sound= pygame.mixer.Sound("jump_sound2.mp3")
#game_over_sound = pygame.mixer.Sound('game_sound.mp3')

#Setting player gravity
gravity =0

#game active set to true so far as game is not over
game_active = True

running = True



#MAIN GAME LOOP	
while running:
	screen.fill((0,0,0))
	curr_time = int((pygame.time.get_ticks()/1000)*10)
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:	
			running = False
		if event.type == pygame.FINGERDOWN and dino_rect.bottom == 680:
			jump_sound.play()
			gravity = -20
	
			
	if curr_time%100==0:
		rand=random.randint(1,2)
			
	if game_active:
		#platform_animation()
		background.animate()
		
		#Score counter
		display_score()
		display_high_score()
		score = curr_time
		
		
		#animate_obstacle()
		
		#if score%100==0:
			#beep_sound.play()
		
		#Obstacle animation
		
		#all_sprites.update()
		#all_sprites.draw(screen)
		change_sprite()
		
		
		#Dinosaur jump
		gravity += 1.4
		dino_rect.y += gravity
		if dino_rect.bottom >= 680:
			dino_rect.bottom = 680
		dino_animation()
		screen.blit(dinosaur, dino_rect)
		
	#Checking for collision and printing message
	"""
	if dino_rect.colliderect(obstacle_rect):
		if score>int(high_score):
			high_score = score
			add_high_score()
		game_active = False
		game_over_display()
		#game_over_sound.play()
		
	if event.type == pygame.FINGERDOWN:
		game_active = True
		obstacle_rect.left = 800
		#Create time reset
	""" 
		    	
	pygame.display.flip()
	clock.tick(60)