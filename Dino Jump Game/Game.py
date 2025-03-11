import pygame
#import Obstacle_class

pygame.init()
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption('DIno jump')
clock = pygame.time.Clock()


#BACKGROUND
background = pygame.image.load('Background1.jpg').convert()
background = pygame.transform.scale(background, (760,500))
background_position = 0

def background_scroll():
	global background_position
	screen.blit(background, (background_position, 240))
	screen.blit(background, (background.get_width() + background_position, 240))
	background_position -= 4
	if abs(background_position) > background.get_width():
		background_position = 0

				
#PLATFORM
platform= pygame.image.load('Background(0).png').convert_alpha()
platform = pygame.transform.scale(platform, (2000,170))
platform_position = 0

def platform_animation():
	global platform_position
	screen.blit(platform, (platform_position, 510))
	screen.blit(platform, (platform.get_width() + platform_position, 510))
	platform_position -= 10
	if abs(platform_position) > platform.get_width():
		platform_position = 0


#DINOSAUR
dino_walk1 = pygame.image.load('dino_walk1.png').convert_alpha()
dino_walk2 = pygame.image.load('dino_walk2.png').convert_alpha()
dinosaur_jump = pygame.image.load("Dino_jump.png").convert_alpha()

dino_walk1 = pygame.transform.scale(dino_walk1, (100,100))
dino_walk2 = pygame.transform.scale(dino_walk2, (100,100))
dinosaur_jump=  pygame.transform.scale(dinosaur_jump,(100,100))

dino_frames = [dino_walk1, dino_walk2]
dinosaur_index = 0
dino_rect = dinosaur_jump.get_rect(midbottom=(80, 615))

def dino_animation():
	global dinosaur, dinosaur_index
	if dino_rect.bottom<615:
		dinosaur = dinosaur_jump
	else:
		dinosaur_index +=0.3
		if dinosaur_index >= len(dino_frames):
			dinosaur_index = 0
		dinosaur = dino_frames[int(dinosaur_index)]

dino_animation()
dino_rect = dinosaur.get_rect(midbottom=(100, 615))


#PTEROSAUR
pterosaur1 = pygame.image.load("pterosaur1.png").convert_alpha()
pterosaur2 = pygame.image.load("pterosaur2.png").convert_alpha()
pterosaur1 = pygame.transform.scale(pterosaur1,(120,90))
pterosaur2 = pygame.transform.scale(pterosaur2,(120,90))


#METEOR
meteor1 = pygame.image.load("meteor1.png").convert_alpha()
meteor2 = pygame.image.load("meteor2.png").convert_alpha()
meteor1 = pygame.transform.scale(meteor1,(130, 55))
meteor2 = pygame.transform.scale(meteor2,(130,55))






#An obstacle class
class Obstacles:
	def __init__(self, img1, img2):
		self.img1 = img1
		self.img2 = img2
		self.frames = [img1, img2]
		self.frame_index = 0
		
	def attack(self):
		global obstacle
		self.frame_index += 0.15
		if self.frame_index >= len(self.frames):
			self.frame_index = 0
		obstacle = self.frames[int(self.frame_index)]
		

meteor = Obstacles(meteor1, meteor2)
meteor.attack()
meteor_rect = obstacle.get_rect(midbottom=(500,590))


pterosaur = Obstacles(pterosaur1, pterosaur2)
pterosaur.attack()
pterosaur_rect = obstacle.get_rect(midbottom=(500,450))




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
	




#GAME OVER MESSAGE
game_over_message_font = pygame.font.SysFont('Arial', 65)
game_over_message= game_over_message_font.render(f"Game Over", True, (0,0,0))
game_over_rect=game_over_message.get_rect(center=(380,500))

def game_over_display():
	#Positioning objects on game over screen
		screen.blit(background,(0,240))	
		screen.blit(platform,(0,570))
		
		#Creating game over score rect
		game_over_score_font = pygame.font.SysFont('Arial', 35)
		game_over_score = game_over_score_font.render(f"You scored: {score}", False, (0,0,0))
		game_over_rect=game_over_message.get_rect(center=(380,500))
		
		#Dislaying text on game over screen
		screen.blit(game_over_message,(180,350))
		screen.blit(game_over_score,game_over_rect)
		



#SOUNDS
sound = pygame.mixer.Sound('sound.mp3')
sound.play()
jump_sound= pygame.mixer.Sound("jump_sound2.mp3")
game_over_sound = pygame.mixer.Sound('game-over.mp3')

#Setting player gravity
gravity =0

#game active set to true so far as game is not over
game_active = True

running = True

#MAIN GAME LOOP	
while running:
	screen.fill((0,0,0))
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:	
			running = False
		if event.type == pygame.FINGERDOWN and dino_rect.bottom == 615:
			jump_sound.play()
			gravity = -20
			
	if game_active:
    	#Background animation
		background_scroll()
		platform_animation()
		
		
		display_score()
		score = curr_time
		
		
	    #Meteor animation
		meteor.attack()
		meteor_rect.left-=15
		if meteor_rect.right<=0:
			meteor_rect.left=800
		screen.blit(obstacle, meteor_rect)
		
		#Pterosaur animation
		pterosaur.attack()
		pterosaur_rect.left-=13
		if pterosaur_rect.right<=0:
			pterosaur_rect.left=800
		screen.blit(obstacle, pterosaur_rect)
		
		
    	#Dinosaur jump
		gravity += 1.4
		dino_rect.y += gravity
		if dino_rect.bottom >= 615:
			dino_rect.bottom = 615
		dino_animation()
		screen.blit(dinosaur, dino_rect)
		
	#Checking for collision and printing message
	if dino_rect.colliderect(pterosaur_rect):
		game_active = False
		game_over_display()
		#game_over_sound.play()
		
		if event.type == pygame.FINGERDOWN:
		    game_active = True
		    pterosaur_rect.left = 800
		    #Create time reset
		    
		    
		    	
	pygame.display.update()
	clock.tick(60)