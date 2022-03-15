import pygame
import sys

WIDTH, HEIGHT = 900, 600

WIN = pygame.display.set_mode((WIDTH, HEIGHT))

BLACK = (0,0,0)
BLUE = (5, 23, 61)
WHITE = (255, 255, 255)
BG = (230, 152, 131)

respawn_player_looks = pygame.image.load("assets/respawn_player.png")
respawn_player = pygame.transform.scale(respawn_player_looks, (50, 50))

cloud = pygame.image.load("assets/cloud.png")
cloud = pygame.transform.scale(cloud, (250, 200))

clock = pygame.time.Clock()
while True:
    clock.tick(120)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            pygame.quit()
            sys.exit()

    WIN.fill(BG)

    WIN.blit(respawn_player, (WIDTH//2, HEIGHT//2))

    WIN.blit(cloud, (WIDTH-100-250, 100))

    pygame.display.update()