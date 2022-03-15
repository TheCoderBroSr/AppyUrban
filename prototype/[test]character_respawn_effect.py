import pygame, os, sys, random
from character_obj import Player

# General setup
pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()

# Game Screen
screen_width = 900
screen_height = 600
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Character Obj - Respawn Effect")

# Creating the sprites and groups
moving_sprites = pygame.sprite.Group()
G=3
FPS = 120
player = Player((450, 450), (screen_width, screen_height), G)
moving_sprites.add(player)

obj = pygame.Rect(screen_width, 0, 80, screen_height)

g=0
screen_shake = 0
COLLISION_SOUND = pygame.mixer.Sound(os.path.join('sounds', 'collide.wav'))
sound_effects = pygame.mixer.Channel(0)

respawn_player = pygame.USEREVENT + 1
while True:
	clock.tick(FPS)
	for event in pygame.event.get():
		if event.type == respawn_player:
			screen_shake = player.respawn(sound_effects, COLLISION_SOUND)
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

	# Drawing
	screen.fill((230, 152, 131))
	pygame.draw.rect(screen, (255, 255, 255), obj)

	player.move()

	moving_sprites.draw(screen)
	moving_sprites.update()

	if pygame.Rect.colliderect(player.rect, obj):
		if g==0:
			pygame.event.post(pygame.event.Event(respawn_player))
		g+=1
		FPS = 60 #Slowing down
	elif g>1:
		g=0

	if obj.x <= -obj.width:
		obj.x = screen_width
		obj.y = 0

	if g==0:
		FPS = 120

	obj.x -= 2

	if screen_shake>0:
		screen_shake -= 1

	offset = [0,0]
	if screen_shake:
		offset[0] = random.randint(0, 8) - 4
		offset[1] = random.randint(0, 8) - 4

	screen.blit(screen, offset)

	#Getting it back to its original x value
	if player.rect.x <= 450 and g==0:
		player.rect.x += 2

	pygame.display.flip()