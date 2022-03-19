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

START = False

title = TITTLE_FONT.render("Press 'p' to start the simulation, and 'q' to stop", 1, BLUE)

obstacle = pygame.Rect(screen_width//2, 0, 100, screen_height)

player_dummy = pygame.Rect(100, screen_height - 150, 50, 50)

collided = 0
reset_counter = 0

initial_player_x = player_dummy.x
initial_player_y = player_dummy.y

target_y = random.randint(obstacle.y + player_dummy.height, obstacle.y + obstacle.height - player_dummy.height)
target_x = random.randint(obstacle.x + player_dummy.width, obstacle.x + obstacle.width - player_dummy.width)


#Determining the Gx and Gy
D = ((target_x - obstacle.x)**2 + (target_y - obstacle.y)**2)**0.5 #Euclidean Distance
Gx = (D**2 - (target_y - obstacle.y)**2)**0.5 #By Pythagoras Theoram
Gy = (D**2 - Gx**2)**0.5

while Gx > 3:
    Gx //= 2

while Gy > 3:
    Gy //= 2
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

        if collided == 1:
            reset_counter += 1

        if reset_counter == FPS:
            collided = 0
            testcase_no += 1

            #Randomly generating AND placing the obstacle
            obstacle.width = random.choice([100, screen_width])
            obstacle.height = [screen_height, 100][obstacle.width == screen_width]
            obstacle.x = [random.randint(120, screen_width-120),0][obstacle.width == screen_width]
            obstacle.y = [random.randint(120, screen_height-120),0][obstacle.height == screen_height]

            #Randomly placing the player
            player_dummy.x = random.choice([y for y in range(50, obstacle.x - player_dummy.width - 50)] + [x for x in range(obstacle.x + obstacle.width + player_dummy.width + 50)])
            player_dummy.y = random.choice([x for x in range(50, obstacle.y - player_dummy.height - 50)] + [y for y in range(obstacle.y + obstacle.height + player_dummy.height + 50)])

            while player_dummy.colliderect(obstacle):
                player_dummy.x = random.choice([y for y in range(50, obstacle.x - player_dummy.width - 50)] + [x for x in range(obstacle.x + obstacle.width + player_dummy.width + 50)])
                player_dummy.y = random.choice([x for x in range(50, obstacle.y - player_dummy.height - 50)] + [y for y in range(obstacle.y + obstacle.height + player_dummy.height + 50)])

            initial_player_x = player_dummy.x
            initial_player_y = player_dummy.y

            print(initial_player_x, initial_player_y)

            target_y = random.randint(obstacle.y + player_dummy.height, obstacle.y + obstacle.height - player_dummy.height)
            target_x = random.randint(obstacle.x + player_dummy.width, obstacle.x + obstacle.width - player_dummy.width)

            D = ((target_x - obstacle.x)**2 + (target_y - obstacle.y)**2)**0.5 #Euclidean Distance
            Gx = (D**2 - (target_y - obstacle.y)**2)**0.5 #By Pythagoras Theoram
            Gy = (D**2 - Gx**2)**0.5

            while Gx > 4:
                Gx //= 2

            while Gy > 4:
                Gy //= 2

            #Resetting the vars
            collided = 0
            reset_counter = 0

            pygame.time.delay(1000)

    pygame.display.update()