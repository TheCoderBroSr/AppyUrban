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
player = Player((screen_width//2, screen_height//2), screen, G)
sample_collision_obj = pygame.Rect(screen_width, 100, 100, 130)

moving_sprites = pygame.sprite.Group()
moving_sprites.add(player)
while True:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill(BG)

    #Drawing a sample collision obj
    pygame.draw.rect(screen, (0,0,0), sample_collision_obj)

    #Giving player ability to move
    player.move()

    moving_sprites.draw(screen)
    moving_sprites.update()

    #Moving the sample collsion obj
    sample_collision_obj.x -= G

    if sample_collision_obj.x <= -sample_collision_obj.width:
        sample_collision_obj.x = screen_width

    pygame.display.update()