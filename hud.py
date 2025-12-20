# hud.py
import pygame

class HUD(pygame.sprite.Sprite):
	def __init__(self, font, x=10, y=10, line_height=30, color=(255, 255, 255)):
		if hasattr(self, "containers"):
			super().__init__(self.containers)
		else:
			super().__init__()
			
		self.font = font
		self.x = x
		self.y = y
		self.line_height = line_height
		self.color = color
		self.lives = 3
		self.asteroids_destroyed = {1:0, 2:0, 3:0}
		
	def score(self):
		return (
			self.asteroids_destroyed[1] * 100 +
			self.asteroids_destroyed[2] * 50 +
			self.asteroids_destroyed[3] * 10
		)

	def draw(self, screen):
		current_score = self.score()

		lives_surf = self.font.render(f"Lives: {self.lives}", True, self.color)
		blank1_surf = self.font.render("", True, self.color)  # optional, can skip
		kills_label_surf = self.font.render("Asteroids Destroyed:", True, self.color)
		sm_kills_surf = self.font.render(f"Type 1: {self.asteroids_destroyed[1]}", True, self.color)
		med_kills_surf = self.font.render(f"Type 2: {self.asteroids_destroyed[2]}", True, self.color)
		lg_kills_surf = self.font.render(f"Type 3: {self.asteroids_destroyed[3]}", True, self.color)
		score_surf = self.font.render(f"Score: {current_score}", True, self.color)

		# Lives
		screen.blit(lives_surf,      (self.x, self.y + self.line_height * 0))
		# blank line (just skip drawing, or leave this comment as a spacer)
		# Asteroids Destroyed label
		screen.blit(kills_label_surf,(self.x, self.y + self.line_height * 2))
		# Types
		screen.blit(sm_kills_surf,   (self.x, self.y + self.line_height * 3))
		screen.blit(med_kills_surf,  (self.x, self.y + self.line_height * 4))
		screen.blit(lg_kills_surf,   (self.x, self.y + self.line_height * 5))
		# blank line
		# Score
		screen.blit(score_surf,      (self.x, self.y + self.line_height * 7))