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
        self.x, self.y = position

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

    def non_passable_zones(self):
        #Creating the recangles that represent the non-passable zones of the obstacle
        npz1 = pygame.Rect(self.rect.x, self.rect.y, self.rect.width, self.rect.y + self.space.y)
        npz2 = pygame.Rect(self.rect.x, self.space.y + self.space.height, self.rect.width, abs((self.rect.y + self.rect.height) - (self.rect.y + self.space.y + self.space.height)))

        return (npz1, npz2) #Returns tuple of the non passable zones

    def copy(self, position):
        return Obstacle(position, self.screen, self.width, self.space_color, self.border_color, self.G)

    def update(self):
        #Changing x, y values to be the same as the obstacle's rect values
        self.x, self.y = self.rect.x, self.rect.y

        # Moving the obstacles
        self.bottom_border.x = self.top_border.x = self.space.x = self.rect.x
        self.rect.x -= self.G

        #Drawing space and borders
        pygame.draw.rect(self.screen, self.space_color, self.space)
        pygame.draw.rect(self.screen, self.border_color, self.top_border)
        pygame.draw.rect(self.screen, self.border_color, self.bottom_border)

def obstacle_generation(obstacles, obstacle_seperation, screen):
    first_obstacle = obstacles.sprites()[0]
    last_obstacle = obstacles.sprites()[-1]
    if last_obstacle.rect.x <= (screen.get_width() - obstacle_seperation): #Check the last obstacles position
        obstacles.add(first_obstacle.copy((screen.get_width(), 0))) #Add new obstacle

    if first_obstacle.rect.x <= -first_obstacle.width: #Deleting Obstacle, when not on screen
        first_obstacle.kill()