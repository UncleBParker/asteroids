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
	
	def scoreboard(self): # for print statements
		return (
			f"Lives: {self.lives}/3\n"
			f"Asteroids Destroyed: \n"
			f"- Small:  {self.asteroids_destroyed[1]}\n"
			f"- Medium: {self.asteroids_destroyed[2]}\n"
			f"- Large:  {self.asteroids_destroyed[3]}\n"
			f"Score: {self.score()}\n"
		)

	def draw(self, screen):
		current_score = self.score()

		lives_surf = self.font.render(f"Lives: {self.lives}", True, self.color)
		kills_label_surf = self.font.render("Asteroids Destroyed:", True, self.color)
		sm_kills_surf = self.font.render(f"Type 1: {self.asteroids_destroyed[1]}", True, self.color)
		med_kills_surf = self.font.render(f"Type 2: {self.asteroids_destroyed[2]}", True, self.color)
		lg_kills_surf = self.font.render(f"Type 3: {self.asteroids_destroyed[3]}", True, self.color)
		score_surf = self.font.render(f"Score: {current_score}", True, self.color)

		screen.blit(lives_surf,      (self.x, self.y + self.line_height * 0))
		# blank line
		screen.blit(kills_label_surf,(self.x, self.y + self.line_height * 2))
		screen.blit(sm_kills_surf,   (self.x, self.y + self.line_height * 3))
		screen.blit(med_kills_surf,  (self.x, self.y + self.line_height * 4))
		screen.blit(lg_kills_surf,   (self.x, self.y + self.line_height * 5))
		# blank line
		screen.blit(score_surf,      (self.x, self.y + self.line_height * 7))