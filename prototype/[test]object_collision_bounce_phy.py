import pygame, sys

# General setup
pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()

# Game Screen
screen_width = 900
screen_height = 600
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Character Collision Bounce - Physics")

# Some important vars
FPS = 120
G = 1 #Is the acceleration

Gx = 2*G
Gy = G

obstacle = pygame.Rect(screen_width - 300, 0, 60, screen_height)
player_dummy = pygame.Rect(100, screen_height - 150, 50, 50)

collided = 0
while True:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type==pygame.KEYDOWN and event.key == pygame.K_q):
            pygame.quit()
            sys.exit()

    screen.fill((255, 255, 255))

    pygame.draw.rect(screen, (0,0,0), obstacle)
    pygame.draw.rect(screen, (20, 50, 90), player_dummy)

    #Move the player
    player_dummy.x += Gx #The accelerations
    player_dummy.y -= Gy

    #Checking if dummy player has collided
    if player_dummy.x + player_dummy.width >= obstacle.x:
        Gx *= -1
        collided = 1

    if collided:
        if Gx <= 0 and Gy >= 0:
            Gx += 0.01
            Gy -= 0.01

        if Gy < 0:
            Gy = 0

        if Gx > 0:
            Gx = 0

    print(Gx, Gy)

    pygame.display.update()