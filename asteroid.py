# asteroid.py
import pygame
import random
from circleshape import CircleShape
from constants import LINE_WIDTH, ASTEROID_MIN_RADIUS
from logger import log_event

class Asteroid(CircleShape):
	def __init__(self, x, y, radius):
		super().__init__(x, y, radius)
		self.kind = radius // ASTEROID_MIN_RADIUS

	def draw(self, screen):
		pygame.draw.circle(screen, "white", self.position, self.radius, LINE_WIDTH)

	def update(self, dt):
		self.position += self.velocity * dt

	def split(self):
		self.kill()
		if self.radius <= ASTEROID_MIN_RADIUS:
			return
		log_event("asteroid_split")
		new_vector = random.uniform(20, 50)
		new_radius = self.radius - ASTEROID_MIN_RADIUS
		split1 = Asteroid(*self.position, new_radius)
		split1.velocity = self.velocity.rotate(new_vector)
		split2 = Asteroid(*self.position, new_radius)
		split2.velocity = self.velocity.rotate(-new_vector)