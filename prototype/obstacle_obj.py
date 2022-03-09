import pygame, sys, os, random

# Obstacle Class
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, position, screen, width, space_color, border_color, G):
        super().__init__()
        self.can_collide = True
        self.G = G
        self.screen = screen
        self.height = screen.get_height()
        self.width = width

        self.image = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'obstacle.png')), (self.width, self.height))

        self.rect = self.image.get_rect()
        self.rect.topleft = position

        #Space from where the player can pass
        self.random_height = random.randint(int((6/13) * self.height), int((11/13) * self.height))
        self.space = pygame.Rect(self.rect.x, self.random_height, self.width, 200)
        self.space_color = space_color
        self.space.y -= self.space.height

        #Borders to make it look cohesive
        self.top_border = pygame.Rect(self.space.x, self.space.y - 10, self.space.width, 10)
        self.bottom_border = pygame.Rect(self.space.x, self.space.y + self.space.height, self.space.width, 10)
        self.border_color = border_color

    def update(self):
        # Moving the obstacles
        self.bottom_border.x = self.top_border.x = self.rect.x
        self.space.x = self.rect.x
        self.rect.x -= G

        #Drawing space and borders
        pygame.draw.rect(self.screen, self.space_color, self.space)
        pygame.draw.rect(self.screen, self.border_color, self.top_border)
        pygame.draw.rect(self.screen, self.border_color, self.bottom_border)

# General setup
pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()

# Game Screen
screen_width = 900
screen_height = 600
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Obstacle Obj")

# Creating the sprites and groups
G=2
FPS = 120
BG = (230, 152, 131)
BLUE = (5, 23, 61)

obstacle = Obstacle((screen_width, 0), screen, 80, BG, BLUE, G)

moving_sprites = pygame.sprite.Group()
moving_sprites.add(obstacle)

while True:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    # Drawing
    screen.fill(BG)
    moving_sprites.draw(screen)
    moving_sprites.update()

    # Procedural Generation
    #Creating new obstacles
    obstacle_seperation = 300
    last_obstacle = moving_sprites.sprites()[-1]
    if last_obstacle.rect.x <= (screen_width - obstacle_seperation): #Check the last obstacles position
        moving_sprites.add(Obstacle((screen_width, 0), screen, 80, BG, BLUE, G)) #Add new obstacle 
    
    #Getting rid of obstacles not on screen
    first_obstacle = moving_sprites.sprites()[0]
    if first_obstacle.rect.x <= -first_obstacle.width:
        first_obstacle.kill()

    print(moving_sprites)

    pygame.display.update()