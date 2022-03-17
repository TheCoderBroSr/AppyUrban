import pygame, sys, os
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

obstacle = Obstacle((screen_width, 0), screen, space_color = BG, border_color = BLUE)

moving_sprites = pygame.sprite.Group()
moving_sprites.add(obstacle)

while True:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    # Drawing
    screen.fill(BG)
    moving_sprites.draw(screen)
    moving_sprites.update()

    # Procedural Generation
    obstacle_generation(moving_sprites, 300, screen)
    print(moving_sprites)

    #Player fill in
    pygame.draw.rect(screen, (0,0,0), pygame.Rect(screen_width//2, screen_height//2, 50, 50))

    pygame.display.update()