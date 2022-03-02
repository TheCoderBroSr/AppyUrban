import os
import pygame
import random
import sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900, 600
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
FPS = 120

BLACK = (0,0,0)
BLUE = (5, 23, 61)
WHITE = (255, 255, 255)
RED = (255, 0, 50)
BG = (230, 152, 131)
G = 3
D = 550
STAY = False

INTRO_FONT = pygame.font.SysFont('comicsans ms', 40)
SCORE_FONT = pygame.font.SysFont('comicsans ms', 80)
MENU_SCORE_FONT = pygame.font.SysFont('comicsans ms', 50)
WINNER_FONT = pygame.font.SysFont('comicsans ms', 120)

player_looks = pygame.image.load(resource_path("assets/player.png"))
respawn_player_looks = pygame.image.load(resource_path("assets/respawn_player.png"))
obstacle_looks = pygame.image.load(resource_path("assets/obstacle.png"))
live_heart_looks = pygame.image.load(resource_path("assets/live_heart.png"))
death_heart_looks = pygame.image.load(resource_path("assets/death_heart.png"))
cloud_looks = pygame.image.load("assets/cloud.png")

COLLISION_SOUND = pygame.mixer.Sound(resource_path('sounds/collide.wav'))
LOSE_SOUND = pygame.mixer.Sound(resource_path('sounds/lose.wav'))
GAME_MUSIC = pygame.mixer.Sound(resource_path('sounds/music.mp3'))
def create_obstacle(player):
    obstacle = pygame.Rect(WIDTH, 0, 80, HEIGHT)
    obstacle_space = pygame.Rect(obstacle.x, random.randint(HEIGHT/3, HEIGHT - (HEIGHT/3)), obstacle.width, player.height*6)
    obstacle_space.y -= obstacle_space.height
    return (obstacle, obstacle_space)

def obstacle_procedural_generation(obstacles, obstacle_looks, obstacle_seperation, WIDTH, player, STAY):
    for obj, obj_space in obstacles:
        obstacle_looks = pygame.transform.scale(obstacle_looks, (obj.width, obj.height))
        WIN.blit(obstacle_looks, (obj.x, obj.y))

        pygame.draw.rect(WIN, BG, obj_space)
        # obj_space_surface = pygame.Surface((obj_space.width, obj_space.height)) Transparent BG
        # obj_space_surface.set_alpha(128)
        # obj_space_surface.fill(WHITE)
        # WIN.blit(obj_space_surface, (obj_space.x, obj_space.y))

        #For Aesthetics
        top_border = pygame.Rect(obj_space.x, obj_space.y - 10, obj_space.width, 10)
        bottom_border = pygame.Rect(obj_space.x, obj_space.y + obj_space.height, obj_space.width, 10)
        pygame.draw.rect(WIN, BLUE, top_border)
        pygame.draw.rect(WIN, BLUE, bottom_border)

        #Gravity
        if STAY:
            obj.x -= G
            obj_space.x = obj.x

        check = WIDTH - obstacle_seperation
        if obj.x == check - (check%G):
            obstacles += [create_obstacle(player)]

        #Removing objects that aren't on screen, for optimization
        if len(obstacles) == (WIDTH//obstacle_seperation)+2:
            obstacles.pop(0)

def check_player_collision(player, obstacles, obstacle_seperation, WIDTH):
    #900, 100 -> 6  8
    #900, 300 -> 2  6
    #WIDTH - player.x 425/100
    #425/300
    for obj, obj_space in obstacles[round((WIDTH - player.x + 30)/obstacle_seperation)*-1:]:
        col_obj = pygame.Rect.colliderect(player, obj)
        pass_obj = pygame.Rect.colliderect(player, obj_space)

        if col_obj and not pass_obj:
            return 1

        if pass_obj:
            return 0

        if (not col_obj) and (not pass_obj):
            return 2

def lose(text, font, surface, color):
    winner = font.render(text, 1, color)
    surface.blit(winner, ((WIDTH - winner.get_width())/2 , (HEIGHT - winner.get_height())/2))
    pygame.display.update()

def intro(STAY, WIN, player, player_looks, clock, last_game_score, highscore, delay):
    while not STAY:
        clock.tick(FPS)
        WIN.fill(BG)

        title = SCORE_FONT.render("Flappy Bird - My Way", 1, BLUE)
        WIN.blit(title, (((WIDTH - title.get_width())//2), 50))

        last_score = MENU_SCORE_FONT.render(f"Last Game Score: {last_game_score}", 1, RED)
        highest_score = MENU_SCORE_FONT.render(f"Highest Game Score: {highscore}", 1, RED)

        WIN.blit(last_score, ((WIDTH - last_score.get_width())//2, HEIGHT - 175))
        WIN.blit(highest_score, ((WIDTH - highest_score.get_width())//2, HEIGHT - 235))

        text = INTRO_FONT.render("Press space bar to start, or q to quit", 1, WHITE)
        WIN.blit(text, ((WIDTH - text.get_width())//2, HEIGHT - 75))

        WIN.blit(player_looks, (player.x, player.y))
        pygame.display.update()

        pygame.time.delay(delay)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return True

            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                pygame.display.quit()
                pygame.quit()
                sys.exit()

def main(WIN, player_looks, respawn_player_looks, obstacle_looks, cloud_looks, live_heart_looks, death_heart_looks, STAY, delay):
    pygame.display.set_caption("Flappy Bird - MY WAY")
    clock = pygame.time.Clock()

    player = pygame.Rect(WIDTH//2, HEIGHT//2, 50 - 20, 50 - 20)
    player.x -= player.width//2
    player.y -= player.height//2

    player_looks = pygame.transform.scale(player_looks, (player.width + 20, player.height + 20))
    respawn_player_looks = pygame.transform.scale(respawn_player_looks, (player.width - 20, player.height - 20))
    cloud_looks = pygame.transform.scale(cloud_looks, (250, 200))

    obstacles = [create_obstacle(player)]
    obstacle_seperation = 300

    points = 0
    health = 3
    live_heart_looks = pygame.transform.scale(live_heart_looks, (50, 40))
    death_heart_looks = pygame.transform.scale(death_heart_looks, (50, 40))
    hearts = [live_heart_looks]*health
    collisions = [0,0]

    music = pygame.mixer.Channel(0)
    sound_effects = pygame.mixer.Channel(1)

    #Getting the scores
    file_scores = open(resource_path("scores.txt"), "r")
    scores = [int(score.replace("\n", "")) for score in list(file_scores)]
    last_game_score = scores[-1]
    highscore = max(scores)
    file_scores.close()

    STAY = intro(STAY, WIN, player, player_looks, clock, last_game_score, highscore, delay)

    if STAY:
        music.play(GAME_MUSIC, -1)
        
    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                sys.exit()

        WIN.fill(BG)

        # WIN.blit(cloud_looks, (WIDTH - 350, 100))Clouds

        obstacle_procedural_generation(obstacles, obstacle_looks, obstacle_seperation, WIDTH, player, STAY)

        if STAY:
            if player.y < HEIGHT-player.height:
                player.y += G#Gravity

            #Movement
            keys_pressed = pygame.key.get_pressed()

            if keys_pressed[pygame.K_SPACE] and player.y > 0:
                player.y -= G*4

        WIN.blit(player_looks, (player.x - 10, player.y - 10))

        is_collide = check_player_collision(player, obstacles, obstacle_seperation, WIDTH)
        if is_collide == 1:
            collisions += [2]
        elif is_collide == 0:
            collisions += [1]
        elif is_collide == 2:
            collisions += [0]

        prev = collisions[-2] 
        now  = collisions[-1]

        if prev == 0 and now == 1:
            points += 1

        if (prev == 0 or prev == 1) and now == 2:
            health -= 1 #Reducing Health
            
            pos = 3-health-1 #Replacing the Heart
            hearts.pop(pos)
            hearts.insert(pos, death_heart_looks)
            
            sound_effects.play(COLLISION_SOUND)
            if health > 0:
                pygame.time.delay(500)

        collisions = collisions[-2:] #Getting rid of unnecessary collisions

        if STAY:
            score = SCORE_FONT.render(str(points), 1, WHITE)
            WIN.blit(score, (10,10))
        
            i=1
            for heart in hearts:
                WIN.blit(heart, (WIDTH - (60*i), 10))
                i+=1

        if health == 0:
            #Storing the score
            file_scores = open(resource_path("scores.txt"), "a")
            file_scores.write(f"\n{points}") 
            file_scores.close()
            
            lose("You Lose", WINNER_FONT, WIN, RED)
            music.fadeout(400)
            music.play(LOSE_SOUND)
            pygame.time.delay(3000)
            STAY = False
            main(WIN, player_looks, respawn_player_looks, obstacle_looks, cloud_looks, live_heart_looks, death_heart_looks, STAY, 500)
        pygame.display.update()

if __name__ == "__main__":
    main(WIN, player_looks, respawn_player_looks, obstacle_looks, cloud_looks, live_heart_looks, death_heart_looks, STAY, 0)