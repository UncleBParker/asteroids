# shot.py 
import pygame
from circleshape import CircleShape
from constants import LINE_WIDTH, SHOT_RADIUS

class Shot(CircleShape):
	def __init__(self, x, y, radius=SHOT_RADIUS):
		#print("creating shot")
		super().__init__(x, y, radius)

	def draw(self, screen):
		#print("drawing shot at", self.position)
		pygame.draw.circle(screen, "white", self.position, self.radius, LINE_WIDTH)

	def update(self, dt):
		self.position += self.velocity * dt