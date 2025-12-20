#hud.py
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
        current_score = self.score(self.asteroids_destroyed)

        score_surf = self.font.render(f"Score: {current_score}", True, self.color)
        lives_surf = self.font.render(f"Lives: {self.lives}", True, self.color)

        screen.blit(score_surf, (self.x, self.y))
        screen.blit(lives_surf, (self.x, self.y + self.line_height))