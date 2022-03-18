import pygame, random, sys

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
testcase_no = 1
G = 1 #Is the acceleration

Gx = 2*G
Gy = G
START = False

title = TITTLE_FONT.render("Press 'p' to start the simulation, and 'q' to stop", 1, BLUE)

obstacle = pygame.Rect(screen_width//2, 0, 60, screen_height)
obstacle.x -= obstacle.width//2

player_dummy = pygame.Rect(100, screen_height - 150, 50, 50)

collided = 0
reset_counter = 0

initial_player_x = player_dummy.x
initial_player_y = player_dummy.y
while True:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type==pygame.KEYDOWN: 
            if event.key == pygame.K_q:
                pygame.quit()
                sys.exit()

            if event.key == pygame.K_p:
                START = True

    screen.fill(BG)

    if not START:
        screen.blit(title, ((screen_width - title.get_width())//2, screen_height//2))

    if START:
        pygame.draw.rect(screen, (0,0,0), obstacle)
        pygame.draw.rect(screen, (20, 50, 90), player_dummy)

        testcase = TITTLE_FONT.render(f"Case No. {testcase_no}", 1, BLUE)
        screen.blit(testcase, ((screen_width - testcase.get_width() - 30), 10))

        #Move the player
        #The accelerations are Gx & Gy
        if initial_player_x < screen_width//2:
            player_dummy.x += Gx
        else:
            player_dummy.x -= Gx

        if initial_player_y > screen_height//2:
            player_dummy.y -= Gy
        else:
            player_dummy.y += Gy

        #Checking if dummy player has collided
        if player_dummy.colliderect(obstacle):
            Gx *= -1
            collided = 1

        if collided == 1:
            reset_counter += 1

        if reset_counter == FPS:
            Gx = 2*G
            Gy = G
            collided = 0
            testcase_no += 1

            player_dummy.x = random.randint(10, screen_width - 75)
            player_dummy.y = random.randint(10, screen_height - 100)

            #Checking for dead zones
            while player_dummy.x in range(obstacle.x - player_dummy.width, obstacle.x + obstacle.width + player_dummy.width):
                player_dummy.x = random.randint(10, screen_width - 75)

            initial_player_x = player_dummy.x
            initial_player_y = player_dummy.y

            #Resetting the vars
            collided = 0
            reset_counter = 0

            pygame.time.delay(1000)

    pygame.display.update()