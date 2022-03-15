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
		self.is_move = False

		self.G = G
		self.screen_height = screen.get_height()

	def respawn(self, sound_channel, collision_sound):
		self.respawn_animation = True
		sound_channel.play(collision_sound)

		self.rect.x -= 110

		return 30

	def move(self):
		#Simulating Gravity
		if self.rect.y < self.screen_height - self.rect.height: #Constraints
			self.rect.y += self.G

		#Getting the Keys Pressed
		keys_pressed = pygame.key.get_pressed()
		if keys_pressed[pygame.K_SPACE] and self.rect.y > 0: #Checking if space bar is pressed and adding contraints
			self.is_move = True

	def collision_det(self, obj):
		return pygame.Rect.colliderect(self.rect, obj)

	def update(self, speed=0.0275):
		#Movement
		if self.is_move:
			self.rect.y -= self.G*4
			self.is_move = False

		#Respawn Animation
		if self.respawn_animation == True:
			self.current_sprite += speed
			if int(self.current_sprite) >= len(self.sprites):
				self.current_sprite = 0
				self.respawn_animation = False

		self.image = self.sprites[int(self.current_sprite)]