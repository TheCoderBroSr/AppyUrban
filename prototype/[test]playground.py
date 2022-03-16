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

#Important Game Vars
G=3
FPS = 120
BG = (230, 152, 131)
BLUE = (5, 23, 61)
WHITE = (255, 255, 255)
START_GAME = False
INTRO_FONT = pygame.font.SysFont('comicsans ms', 30)

text = INTRO_FONT.render("Press space bar to start, or q to quit", 1, WHITE)

#Sprite Groups
moving_sprites = pygame.sprite.Group()
collision_sprites = pygame.sprite.Group()

#Initializing player and obstacle objects
player = Player((screen_width//2, screen_height//2), screen, G)
obstacle = Obstacle((screen_width, 0), screen, 80, BG, BLUE, G)

#Adding them to their respective sprite group
moving_sprites.add(player)
collision_sprites.add(obstacle)
while True:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                START_GAME = True

            if event.key == pygame.K_q:
                pygame.quit()
                sys.exit()

    screen.fill(BG)

    if START_GAME:

        #Drawing and updating the sprite groups
        collision_sprites.draw(screen)
        collision_sprites.update()

        moving_sprites.update()

        obstacle_generation(collision_sprites, 300, screen)
        player.move()

    moving_sprites.draw(screen)
    if not START_GAME:
        screen.blit(text, (((screen_width - text.get_width())//2),screen_height - 60))

    pygame.display.update()