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
G = 3 #Is the acceleration

START = False

title = TITTLE_FONT.render("Press 'p' to start the simulation, and 'q' to stop", 1, BLUE)

obstacle = pygame.Rect(screen_width//2, 0, 60, screen_height)
obstacle.x -= obstacle.width//2

player_dummy = pygame.Rect(100, screen_height - 150, 50, 50)

collided = 0
reset_counter = 0

initial_player_x = player_dummy.x
initial_player_y = player_dummy.y

target_y = random.randint(obstacle.y, obstacle.y + obstacle.height)
target_x = random.randint(obstacle.x, obstacle.x + obstacle.width)
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

        #Determining the Gx and Gy
        # (target_y - obstacle.y)^2 + (Gx)^2 = (D)^2
        D = ((target_x - obstacle.x)**2 + (target_y - obstacle.y)**2)**0.5 #Euclidean Distance
        Gx = (D**2 - (target_y - obstacle.y)**2)**0.5 #By Pythagoras Theoram
        Gy = (D**2 - Gx**2)**0.5

        while Gx > G:
            Gx //= 2

        while Gy > G:
            Gy //= 2

        #Determine the direction
        if initial_player_x < obstacle.x//2:
            player_dummy.x += Gx
        else:
            player_dummy.x -= Gx

        if initial_player_y > obstacle.y//2:
            player_dummy.y -= Gy
        else:
            player_dummy.y += Gy

        #Checking if dummy player has collided
        if player_dummy.colliderect(obstacle):
            if obstacle.height > obstacle.width: #Checking if obstacle is vertical
                Gx *= -1
            else:
                Gy *= -1
            collided = 1

        print(Gx, Gy)

        if collided == 1:
            reset_counter += 1

        if reset_counter == FPS:
            Gx = 2*G
            Gy = G
            collided = 0
            testcase_no += 1

            #Randomly generating AND placing the obstacle
            obstacle.x = random.randint(20, screen_width - 20)
            obstacle.y = random.randint(20, screen_height - 20)
            obstacle.width = random.randint(20, screen_width)
            obstacle.height = random.randint(20, screen_height)

            while obstacle.x not in range(screen_width) and (obstacle.x + obstacle.width) not in range(screen_width) and obstacle.y not in range(screen_height) and (obstacle.y + obstacle.height) not in range(screen_height):
                obstacle.x = random.randint(20, screen_width - 20)
                obstacle.y = random.randint(20, screen_height - 20)
                obstacle.width = random.randint(20, screen_width)
                obstacle.height = random.randint(20, screen_height)

            #Randomly placing the player
            player_dummy.x = random.randint(10, screen_width - 75)
            player_dummy.y = random.randint(10, screen_height - 100)

            #Checking for dead zones
            while player_dummy.colliderect(obstacle):
                player_dummy.x = random.randint(10, screen_width - 75)
                player_dummy.y = random.randint(10, screen_height - 100)

            initial_player_x = player_dummy.x
            initial_player_y = player_dummy.y

            D = ((target_x - obstacle.x)**2 + (target_y - obstacle.y)**2)**0.5 #Euclidean Distance
            Gx = (D**2 - (target_y - obstacle.y)**2)**0.5 #By Pythagoras Theoram
            Gy = (D**2 - Gx**2)**0.5

            #Resetting the vars
            collided = 0
            reset_counter = 0

            pygame.time.delay(1000)

    pygame.display.update()