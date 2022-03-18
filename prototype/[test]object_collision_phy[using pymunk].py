import pygame, pymunk, sys

# General setup
pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()

# Game Screen
screen_width = 900
screen_height = 600
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Character Collision Bounce - Physics [MY WAY]")

# Some important vars
TITTLE_FONT = pygame.font.SysFont('Cooper Black', 30)
FPS = 120
BG = (230, 152, 131)
BLUE = (5, 23, 61)

#Acceleration
G=1
Gx = 2*G
Gy = G

player_dummy = pygame.Rect(100, screen_height-100, 50, 50)
obstacle = pygame.Rect(screen_width - 300, 0, 40, screen_height)

#Pymunk Phy Important Vars
space = pymunk.space()

while True:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                pygame.quit()
                sys.exit()
    
    screen.fill(BG)

    #Drawing the obstacle and player
    pygame.draw.rect(screen, (0,0,0), obstacle)
    pygame.draw.rect(screen, BLUE, player_dummy)

    #Moving the player
    player_dummy.x += Gx
    player_dummy.y -= Gy

    pygame.display.update()