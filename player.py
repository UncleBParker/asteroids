import pygame
from circleshape import CircleShape
from constants import PLAYER_RADIUS, LINE_WIDTH, PLAYER_TURN_SPEED, PLAYER_SPEED, PLAYER_SHOOT_SPEED, PLAYER_SHOT_COOLDOWN_SECONDS
from shot import Shot
from asteroid import Asteroid
from utils import triangle_circle_collision

class Player(CircleShape):
	def __init__(self, x, y):
		super().__init__(x, y, PLAYER_RADIUS)
		self.rotation = 0
		self.shot_cooldown_timer = 0

	def triangle(self):
		forward = pygame.Vector2(0, 1).rotate(self.rotation)
		right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
		a = self.position + forward * self.radius
		b = self.position - forward * self.radius - right
		c = self.position - forward * self.radius + right
		return [a, b, c]
	
	def draw(self, screen_obj):
		#print("drawing player")
		pygame.draw.polygon(screen_obj, "white", self.triangle(), LINE_WIDTH)

	def rotate(self, dt):
		self.rotation += PLAYER_TURN_SPEED * dt

	def move(self, dt):
		unit_vector = pygame.Vector2(0, 1)
		rotated_vector = unit_vector.rotate(self.rotation)
		rotated_with_speed_vector = rotated_vector * PLAYER_SPEED * dt
		self.position += rotated_with_speed_vector

	def update(self, dt):
		keys = pygame.key.get_pressed()
		self.shot_cooldown_timer -= dt

		if keys[pygame.K_a]:
			self.rotate(-dt)
		if keys[pygame.K_d]:
			self.rotate(dt)
		if keys[pygame.K_w]:
			self.move(dt)
		if keys[pygame.K_s]:
			self.move(-dt)
		if keys[pygame.K_SPACE]:
			self.shoot()

	def shoot(self):
		#print("shoot called")
		if self.shot_cooldown_timer > 0:
			pass
		else:
			self.shot_cooldown_timer = PLAYER_SHOT_COOLDOWN_SECONDS
			shot = Shot(*self.position)
			shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED

	def triangle_circle_collision(tri_points, cx, cy, radius):
		if pygame.point_in_triangle((cx, cy), tri_points):
			return True

	def collides_with(self, other):
		if isinstance(self, Player) and isinstance(other, Asteroid):
			return triangle_circle_collision(self.triangle(), other.position, other.radius)
		if isinstance(self, Asteroid) and isinstance(other, Player):
			return triangle_circle_collision(other.triangle(), self.position, self.radius)
		# Fallback: circle–circle for everything else
		return self.position.distance_to(other.position) < (self.radius + other.radius)