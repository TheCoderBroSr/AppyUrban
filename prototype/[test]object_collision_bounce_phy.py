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
G = 1

obstacle = pygame.Rect(screen_width - 300, 0, 60, screen_height)
player_dummy = pygame.Rect(100, screen_height - 150, 50, 50)

player_dummy_positions = [player_dummy.topleft]
while True:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type==pygame.KEYDOWN and event.key == pygame.K_q):
            pygame.quit()
            sys.exit()

    screen.fill((255, 255, 255))

    pygame.draw.rect(screen, (0,0,0), obstacle)
    pygame.draw.rect(screen, (20, 50, 90), player_dummy)

    #Tracking player_dummy positions
    player_dummy_positions += [player_dummy.topleft]

    if len(player_dummy_positions) > 1:
        player_dummy_positions = player_dummy_positions[-2:]

    player_latest_position = player_dummy_positions[-1]
    player_2nd_latest_position = player_dummy_positions[-2]

    if player_latest_position[0] + player_dummy.width < obstacle.x:
        #Moving dummy player
        player_dummy.x += 2*G
        player_dummy.y -= G
    else:
        new_change = []
        if player_2nd_latest_position != player_latest_position:
            new_change += [player_latest_position[0] - player_2nd_latest_position[0]]
            new_change += [player_latest_position[1] - player_2nd_latest_position[1]]

        player_dummy.x -= new_change[0]
        print(new_change)

    pygame.display.update()