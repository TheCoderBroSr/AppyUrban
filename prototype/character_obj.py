import pygame, os

class Player(pygame.sprite.Sprite):
	def __init__(self, position, screen, G):
		super().__init__()
		self.respawn_animation = False
		self.sprites = []

		for _ in range(4):
			self.sprites.append(pygame.transform.scale(pygame.image.load(os.path.join('assets', 'player.png')), (50,50)))
			self.sprites.append(pygame.transform.scale(pygame.image.load(os.path.join('assets', 'respawn_player.png')), (50,50)))

		self.current_sprite = 0
		self.image = self.sprites[self.current_sprite]

		self.rect = self.image.get_rect()
		self.rect.topleft = position
		self.x, self.y = position
		self.can_move = False

		self.G = G
		self.screen_height = screen.get_height()

	def respawn(self):
		self.respawn_animation = True

	def move(self):
		#Simulating Gravity
		if self.rect.y < self.screen_height - self.rect.height: #Constraints
			self.rect.y += self.G

		#Getting the Keys Pressed
		keys_pressed = pygame.key.get_pressed()
		if keys_pressed[pygame.K_SPACE] and self.rect.y > 0: #Checking if space bar is pressed and adding contraints
			self.can_move = True

	def collision_det(self, obj, precision=0):
		x_range = range(obj.x + precision, obj.x + obj.width - precision)
		y_range = range(obj.y + precision, obj.y + obj.height - precision)

		#testing
		# x_range_rect = pygame.Rect(obj.x + precision, obj.x + obj.width - precision, 10, 10)
		# y_range_rect = pygame.Rect(obj.y + precision, obj.y + obj.width - precision, 10, 10)
		
		horizontal_collision = (self.x in x_range) or (self.x + self.rect.width in x_range)
		vertical_collision = (self.y in y_range) or (self.y + self.rect.height in y_range)

		# return (horizontal_collision, vertical_collision, x_range_rect, y_range_rect)
		return (horizontal_collision, vertical_collision)

	def update(self, speed=0.0275):
		#Changing x, y values to be the same as the player's rect values
		self.x, self.y = self.rect.x, self.rect.y

		#Movement
		if self.can_move:
			self.rect.y -= self.G*4
			self.can_move = False

		#Respawn Animation
		if self.respawn_animation == True:
			self.current_sprite += speed
			if int(self.current_sprite) >= len(self.sprites):
				self.current_sprite = 0
				self.respawn_animation = False

		self.image = self.sprites[int(self.current_sprite)]