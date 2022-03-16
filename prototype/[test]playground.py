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
pygame.display.set_caption("Demo - using OOP")

#Important Game Vars
G=3
FPS = 120
BG = (230, 152, 131)
BLUE = (5, 23, 61)
WHITE = (255, 255, 255)
START_GAME = False
TITTLE_FONT = pygame.font.SysFont('Cooper Black', 70)
INTRO_FONT = pygame.font.SysFont('comicsans ms', 30)

title = TITTLE_FONT.render("Demo - using OOP", 1, BLUE)
start_line = INTRO_FONT.render("Press space bar to start, or q to quit", 1, WHITE)

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

    #Check is user has started game
    if START_GAME:

        #Drawing and updating the sprite groups
        collision_sprites.draw(screen)
        collision_sprites.update()

        moving_sprites.update()

        obstacle_generation(collision_sprites, 300, screen)
        player.move()

        #Checking for collisions
        for obstacle in collision_sprites.sprites():
            if obstacle.can_collide:
                #Getting the two non passable zones of the obstacle
                npz1, npz2 = obstacle.non_passable_zones()

                #Checking if the player is colliding with these zones
                x1_collide, y1_collide = player.collision_det(npz1, 30)
                x2_collide, y2_collide = player.collision_det(npz2, 30)

                if ((x1_collide and y1_collide) or (x2_collide and y2_collide)) and (not player.respawn_animation):
                    obstacle.can_collide = False
                    player.respawn()

                #If the obstacle has passed the player, then it can't collide with the player
                if obstacle.x + obstacle.width < player.x:
                    obstacle.can_collide = False

    moving_sprites.draw(screen)
    if not START_GAME:
        screen.blit(title, (((screen_width - title.get_width())//2),60))
        screen.blit(start_line, (((screen_width - start_line.get_width())//2),screen_height - 100))

    pygame.display.update()