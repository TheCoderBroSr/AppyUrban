import pygame, sys, os, random

# General setup
pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()

# Game Screen
screen_width = 900
screen_height = 600
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Obstacle Obj")

# Creating the sprites and groups
G=3
FPS = 120

moving_sprites = pygame.sprite.Group()
# moving_sprites.add(player)

while True:
	clock.tick(FPS)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

	# Drawing
	screen.fill((230, 152, 131))
	pygame.display.flip()