import pygame
from character_obj import Player

# General setup
pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()

# Game Screen
screen_width = 900
screen_height = 600
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Character Obj - Effects")

# Creating the sprites and groups
G=3
FPS = 120
BG = (230, 152, 131)
player = Player((450, 450), (screen_width, screen_height), G)

moving_sprites = pygame.sprite.Group()
moving_sprites.add(player)

while True:
    clock.tick(FPS)

    screen.fill(BG)

    pygame.diplay.update()