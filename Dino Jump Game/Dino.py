import pygame

pygame.init()
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption('DIno jump')
clock = pygame.time.Clock()

#importing game objects
background = pygame.image.load('game_assets/Background.png').convert()
platform= pygame.image.load('game_assets/Platform.png').convert_alpha()
small_cactus = pygame.image.load("game_assets/Small_cactus.png").convert_alpha()
big_cactus = pygame.image.load("game_assets/Big_cactus.png").convert_alpha()
dinosaur_stand = pygame.image.load('game_assets/Dino.png').convert_alpha()
dinosaur_jump = pygame.image.load("game_assets/Dino_jump.png")
meteor = pygame.image.load('game_assets/Meteor.png').convert_alpha()
sound = pygame.mixer.Sound('game_assets/sound.mp3')


#Scaling and positioning game sprites
background = pygame.transform.scale(background, (760,500))
platform = pygame.transform.scale(platform, (720,90))

small_cactus = pygame.transform.scale(small_cactus,(35, 100))
small_cactus_rect = small_cactus.get_rect(midbottom=(380, 612))

big_cactus = pygame.transform.scale(big_cactus,(40, 120))
big_cactus_rect = big_cactus.get_rect(midbottom=(580, 612))

dinosaur_stand = pygame.transform.scale(dinosaur_stand, (110,110))
dinosaur_jump=  pygame.transform.scale(dinosaur_jump,(110,110))
dinosaur = dinosaur_stand
dino_rect = dinosaur.get_rect(midbottom=(80, 615))

meteor = pygame.transform.scale(meteor, (130,55))
meteor_rect = meteor.get_rect(midbottom=(500,590))
	





curr_time = int(pygame.time.get_ticks()/1000)
score_font = pygame.font.SysFont('Arial', 35)

#Score Counter
def display_score():
	curr_time = int((pygame.time.get_ticks()/1000)*10)
	score_surf = score_font.render(f"Score: {curr_time}", False, (0,0,0))
	score_rect = score_surf.get_rect(midleft=(30,270))
	pygame.draw.rect(screen,"#2AD2F2", score_rect)
	pygame.draw.rect(screen, "#2AD2F2", score_rect,10)
	screen.blit(score_surf, score_rect)
	return curr_time

score = 0	


#Game Over message

game_over_message_font = pygame.font.SysFont('Arial', 65)
game_over_message= game_over_message_font.render(f"Game Over", True, (0,0,0))

game_over_score_font = pygame.font.SysFont('Arial', 35)
game_over_score = game_over_score_font.render(f"You scored: {score}", False, (0,0,0))
game_over_rect=game_over_message.get_rect(center=(380,500))

#Dinosaur jump animation
def dino_animation():
	global dinosaur
	if dino_rect.bottom<615:
		dinosaur = dinosaur_jump
	else:
		dinosaur = dinosaur_stand


#Setting player gravity
gravity =0

#game active set to true so far as game is not over
game_active = True


running = True


#sound.play()

#Main gameloop	
while running:
	screen.fill((0,0,0))
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:	
			running = False
		if event.type == pygame.FINGERDOWN and dino_rect.bottom == 615:
			gravity = -20
			
	if game_active:
    	#positoning objects rects on game window
		screen.blit(background,(0,240))	
		screen.blit(platform,(0,570))
		screen.blit(small_cactus, small_cactus_rect)
		screen.blit(big_cactus, big_cactus_rect)	
		
		
		display_score()
		score = display_score()
	    #Meteor animation
		meteor_rect.left-=15
		if meteor_rect.right<=0:
		    meteor_rect.left=800
		screen.blit(meteor, meteor_rect)
		
	#Dinosaur jump
		gravity += 1
		dino_rect.y += gravity
		if dino_rect.bottom >= 615:
			dino_rect.bottom = 615
		dino_animation()
		screen.blit(dinosaur, dino_rect)
		
		
		#Checking for collision and printing messag amd score
	if dino_rect.colliderect(meteor_rect):
		game_active = False
		#Positioning objects on game over screen
		screen.blit(background,(0,240))	
		screen.blit(platform,(0,570))
		screen.blit(small_cactus, small_cactus_rect)
		screen.blit(big_cactus, big_cactus_rect)	
		
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
