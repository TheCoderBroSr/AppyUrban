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
sample_collision_obj1 = pygame.Rect(screen_width, 100, 150, 150) #Spawing obstacle right
sample_collision_obj2 = pygame.Rect(0, 300, 150, 150) #Spawing obstacle left 
obj_color1 = (20,60,30)
obj_color2 = (20,50,60)

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
    pygame.draw.rect(screen, obj_color1, sample_collision_obj1)
    pygame.draw.rect(screen, obj_color2, sample_collision_obj2)

    #Giving player ability to move
    player.move()

    moving_sprites.draw(screen)
    moving_sprites.update()

    #Moving the sample collsion obj left
    sample_collision_obj1.x -= G

    #Moving the sample collsion obj right
    sample_collision_obj2.x += G

    #Teleporting obstacle left to right
    if sample_collision_obj1.x <= -sample_collision_obj1.width: 
        sample_collision_obj1.x = screen_width

    #Teleporting obstacle from right to left
    if sample_collision_obj2.x >= screen_width + sample_collision_obj2.width: 
        sample_collision_obj2.x = 0

    #Checking for collision
    if player.collision_det(sample_collision_obj1):
        obj_color1 = (255,0,0)
    else:
        obj_color1 = (20,60,30)

    if player.collision_det(sample_collision_obj2):
        obj_color2 = (255,0,0)
    else:
        obj_color2 = (20,50,60)
    pygame.display.update()