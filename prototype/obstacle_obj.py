import pygame, os, random

# Obstacle Class
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, position, surface, **properties):
    # def __init__(self, position, surface, width, space_color, border_color, G):
        super().__init__()
        self.can_collide = True
        self.G = 3
        if "G" in properties:
            self.G = properties["G"]
        
        self.surface = surface
        self.height = surface.get_height()

        self.width = 80
        if "width" in properties:
            self.width = properties["width"]
        
        position = (surface.get_width(), 0)
        self.x, self.y = position

        self.image = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'obstacle.png')), (self.width, self.height))

        self.rect = self.image.get_rect()
        self.rect.topleft = position

        #Space from where the player can pass
        self.space_height = random.randint(int((6/13) * self.height), int((11/13) * self.height))
        self.space = pygame.Rect(self.rect.x, self.space_height, self.width, 200)
        self.space_color = (255,255,255)
        if "space_color" in properties:
            self.space_color = properties["space_color"]

        self.space.y -= self.space.height

        #Borders to make it look cohesive
        self.top_border = pygame.Rect(self.space.x, self.space.y - 10, self.space.width, 10)
        self.bottom_border = pygame.Rect(self.space.x, self.space.y + self.space.height, self.space.width, 10)
        self.border_color = (0,0,0)
        if "border_color" in properties:
            self.border_color = properties["border_color"]

    def non_passable_zones(self):
        #Creating the recangles that represent the non-passable zones of the obstacle
        npz1 = pygame.Rect(self.rect.x, self.rect.y, self.rect.width, self.rect.y + self.space.y)
        npz2 = pygame.Rect(self.rect.x, self.space.y + self.space.height, self.rect.width, abs((self.rect.y + self.rect.height) - (self.rect.y + self.space.y + self.space.height)))

        return (npz1, npz2) #Returns tuple of the non passable zones

    def copy(self, position):
        return Obstacle(position, self.surface, width=self.width, space_color=self.space_color, border_color=self.border_color, G=self.G)

    def update(self):
        #Changing x, y values to be the same as the obstacle's rect values
        self.x, self.y = self.rect.x, self.rect.y

        # Moving the obstacles
        self.bottom_border.x = self.top_border.x = self.space.x = self.rect.x
        self.rect.x -= self.G

        #Drawing space and borders
        pygame.draw.rect(self.surface, self.space_color, self.space)
        pygame.draw.rect(self.surface, self.border_color, self.top_border)
        pygame.draw.rect(self.surface, self.border_color, self.bottom_border)

def obstacle_generation(obstacles, obstacle_seperation, surface):
    first_obstacle = obstacles.sprites()[0]
    last_obstacle = obstacles.sprites()[-1]
    if last_obstacle.rect.x <= (surface.get_width() - obstacle_seperation): #Check the last obstacles position
        obstacles.add(first_obstacle.copy((surface.get_width(), 0))) #Add new obstacle

    if first_obstacle.rect.x <= -first_obstacle.width: #Deleting Obstacle, when not on surface
        first_obstacle.kill()