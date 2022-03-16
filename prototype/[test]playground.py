import pygame, sys
from character_obj import Player
from obstacle_obj import Obstacle, obstacle_generation

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
BG = (230, 152, 131)
BLUE = (5, 23, 61)

obstacle = Obstacle((screen_width, 0), screen, 80, BG, BLUE, G)

collision_sprites = pygame.sprite.Group()
collision_sprites.add(obstacle)

while True:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill(BG)

    collision_sprites.draw(screen)
    collision_sprites.update()

    obstacle_generation(collision_sprites, 300, screen)

    pygame.display.update()