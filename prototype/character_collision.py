import pygame, sys
from character_obj import Player

# General setup
pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()

# Game Screen
screen_width = 900
screen_height = 600
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Character Obj - Collision")

# Creating the sprites and groups
G=3
FPS = 120
BG = (230, 152, 131)
# player = Player((450, 450), (screen_width, screen_height), G)

while True:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill(BG)

    pygame.display.update()