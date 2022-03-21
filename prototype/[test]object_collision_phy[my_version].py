from distutils.spawn import spawn
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

#Helper Functions
def randomly_generate_obstacle(screen, width):
    screen_width = screen.get_width()
    screen_height = screen.get_height()
    
    obstacle = pygame.Rect(0,0,0,0)
    obstacle.width = random.choice([width, screen_width])
    obstacle.height = [screen_height, width][obstacle.width == screen_width]
    obstacle.x = [random.randint(width + 20, screen_width - width - 20),0][obstacle.width == screen_width]
    obstacle.y = [random.randint(width + 20, screen_height - width - 20),0][obstacle.height == screen_height]

    return obstacle

def randomly_generate_player(screen, size):
    screen_width = screen.get_width()
    screen_height = screen.get_height()

    player = pygame.Rect(0,0,size,size)
    player.x = random.randint(10, screen_width - size - 10)
    player.y = random.randint(10, screen_height - size - 10)
    
    return player

def spawn(offset):
    obstacle = randomly_generate_obstacle(screen, 100)
    player_dummy = randomly_generate_player(screen, 50)


    spawn_offset = player_dummy.width + offset
    no_player_spawn_zone = pygame.Rect(obstacle.x - spawn_offset//2, obstacle.y - spawn_offset//2, obstacle.width + spawn_offset, obstacle.height + spawn_offset)

    while player_dummy.colliderect(no_player_spawn_zone):
        player_dummy = randomly_generate_player(screen, 50)

    return obstacle, player_dummy

def generate_target_point(obstacle):
    target_x = random.randint(obstacle.x + 50, obstacle.x + obstacle.width - 50)
    target_y = random.randint(obstacle.y + 50, obstacle.y + obstacle.height - 50)
    target_point = (target_x, target_y)

    return target_point

def determine_speed(player, target_point, time=120):
    target_point_x, target_point_y = target_point

    #Euclidean Distance
    slant_distance = ((player.x - target_point_x)**2 + (player.y - target_point_y)**2)**0.5

    #Using trignometry
    Dx = target_point_x - player.x
    Dy = target_point_y - player.y
 
    #speeds
    Vx = round(Dx/time)
    Vy = round(Dy/time)

    if Vx == 0:
        Vx = 1

    if Vy == 0:
        Vy = 1

    return (Vx, Vy)

def init():
    obstacle, player_dummy = spawn(20)

    collided = 0
    reset_counter = 0

    initial_player_x, initial_player_y = (player_dummy.x + (player_dummy.width//2), player_dummy.y + (player_dummy.height//2))
    target_x, target_y = generate_target_point(obstacle)

    #Determining the Gx and Gy
    Gx, Gy = determine_speed(player_dummy, (target_x, target_y))

    x_collided = 1
    y_collided = 1

    return (obstacle, player_dummy, collided, reset_counter, target_x, target_y, Gx, Gy, x_collided, y_collided)

obstacle, player_dummy, collided, reset_counter, target_x, target_y, Gx, Gy, x_collided, y_collided = init()

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

            if event.key == pygame.K_w:
                collided = 1

    screen.fill(BG)

    if not START:
        screen.blit(title, ((screen_width - title.get_width())//2, screen_height//2))

    if START:
        #Drawing the obstacle and player
        pygame.draw.rect(screen, (0,0,0), obstacle)
        pygame.draw.rect(screen, (20, 50, 90), player_dummy)

        #Target for the player
        pygame.draw.circle(screen, (255, 0, 0), (target_x, target_y), 5, 2)

        #The Path
        pygame.draw.line(screen, (134,56,105), (player_dummy.x + (player_dummy.width//2), player_dummy.y + (player_dummy.height//2)), (target_x, target_y), width=2)

        #Displaying Testcase No.
        testcase = TITTLE_FONT.render(f"Case No. {testcase_no}", 1, BLUE)
        screen.blit(testcase, ((screen_width - testcase.get_width() - 30), 10))

        print(Gx, Gy)

        #Moving the player
        player_dummy.x += Gx * x_collided
        player_dummy.y += Gy * y_collided

        #Checking if dummy player has collided
        if player_dummy.colliderect(obstacle):
            if obstacle.height > obstacle.width: #Checking if obstacle is vertical
                x_collided = -1
            else:
                y_collided = -1
            collided = 1

        if collided == 1:
            reset_counter += 1

        if reset_counter == FPS:
            testcase_no += 1
            obstacle, player_dummy, collided, reset_counter, target_x, target_y, Gx, Gy, x_collided, y_collided = init()

            pygame.time.delay(1000)

    pygame.display.update()