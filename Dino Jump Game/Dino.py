import pygame

pygame.init()
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption('DIno jump')
clock = pygame.time.Clock()


#BACKGROUND
background = pygame.image.load('game_aasets/Background1.png').convert()
background = pygame.transform.scale(background, (760,500))
	
				
#PLATFORM
platform= pygame.image.load('game_assets/Background(0).png').convert_alpha()
platform = pygame.transform.scale(platform, (2000,170))
position = 0

def platform_animation():
	global position
	screen.blit(platform, (position, 510))
	screen.blit(platform, (platform.get_width() + position, 510))
	position -= 7.9
	
	if abs(position) > platform.get_width():
		position = 0


#DINOSAUR
dino_walk1 = pygame.image.load('game_assets/dino_walk1.png').convert_alpha()
dino_walk2 = pygame.image.load('game_assets/dino_walk2.png').convert_alpha()
dinosaur_jump = pygame.image.load("game_assets/Dino_jump.png").convert_alpha()

dino_walk1 = pygame.transform.scale(dino_walk1, (100,100))
dino_walk2 = pygame.transform.scale(dino_walk2, (100,100))
dinosaur_jump=  pygame.transform.scale(dinosaur_jump,(100,100))

dino_frames = [dino_walk1, dino_walk2]
dinosaur_index = 0
dino_rect = dinosaur_jump.get_rect(midbottom=(80, 615))

def dino_animation():
	global dinosaur, dino_rect, dinosaur_index
	if dino_rect.bottom<615:
		dinosaur = dinosaur_jump
	else:
		dinosaur_index +=0.25
		if dinosaur_index >= len(dino_frames):
			dinosaur_index = 0
		dinosaur = dino_frames[int(dinosaur_index)]

dino_animation()
dino_rect = dinosaur.get_rect(midbottom=(100, 615))


#PTEROSAUR
pterosaur1 = pygame.image.load("game_assets/pterosaur1.png").convert_alpha()
pterosaur2 = pygame.image.load("game_assets/pterosaur2.png").convert_alpha()
pterosaur1 = pygame.transform.scale(pterosaur1,(120,90))
pterosaur2 = pygame.transform.scale(pterosaur2,(120,90))
pterosaur_frames = [pterosaur1, pterosaur2]
pterosaur_index = 0

def ptero_animation():
	global pterosaur, pterosaur_rect, pterosaur_index
	pterosaur_index +=0.1
	if pterosaur_index >= len(pterosaur_frames):
		pterosaur_index = 0
	pterosaur = pterosaur_frames[int(pterosaur_index)]

ptero_animation()
pterosaur_rect = pterosaur.get_rect(midbottom=(500,450))



#METEOR
meteor = pygame.image.load('game_assets/Meteor.png').convert_alpha()
meteor = pygame.transform.scale(meteor, (130,55))
meteor_rect = meteor.get_rect(midbottom=(500,590))

#Score Counter
curr_time = int(pygame.time.get_ticks()/1000)
score_font = pygame.font.SysFont('Arial', 35)

def display_score():
	curr_time = int((pygame.time.get_ticks()/1000)*10)
	score_surf = score_font.render(f"Score: {curr_time}", False, (0,0,0))
	score_rect = score_surf.get_rect(midleft=(30,270))
	pygame.draw.rect(screen,"#2AD2F2", score_rect)
	pygame.draw.rect(screen, "#2AD2F2", score_rect,10)
	screen.blit(score_surf, score_rect)
	return curr_time

score = 0	


#GAME OVER MESSAGE
game_over_message_font = pygame.font.SysFont('Arial', 65)
game_over_message= game_over_message_font.render(f"Game Over", True, (0,0,0))

game_over_score_font = pygame.font.SysFont('Arial', 35)
game_over_score = game_over_score_font.render(f"You scored: {score}", False, (0,0,0))
game_over_rect=game_over_message.get_rect(center=(380,500))


#Sounds
sound = pygame.mixer.Sound('sound.mp3')
#sound.play()



#Setting player gravity
gravity =0

#game active set to true so far as game is not over
game_active = True

running = True


#Main gameloop	
while running:
	screen.fill((225,225,225))
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:	
			running = False
		if event.type == pygame.FINGERDOWN and dino_rect.bottom == 615:
			gravity = -20
			
	if game_active:
    	#positoning objects rects on game window
		screen.blit(background,(0,240))	
		platform_animation()
		
		
		display_score()
		score = display_score()
	    #Meteor animation
		meteor_rect.left-=15
		if meteor_rect.right<=0:
		    meteor_rect.left=800
		screen.blit(meteor, meteor_rect)
		
		#pterosaur animation
		ptero_animation()
		pterosaur_rect.left-=13
		if pterosaur_rect.right<=0:
			pterosaur_rect.left=800
		screen.blit(pterosaur, pterosaur_rect)
		
	#Dinosaur jump
		gravity += 1.4
		dino_rect.y += gravity
		if dino_rect.bottom >= 615:
			dino_rect.bottom = 615
		dino_animation()
		screen.blit(dinosaur, dino_rect)
		
		
		#Checking for collision and printing messag amd score
	if dino_rect.colliderect(pterosaur_rect):
		game_active = False
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
		
		if event.type == pygame.FINGERDOWN:
		    game_active = True
		    
		    	
	pygame.display.update()
	clock.tick(60)
