# circleshape.py 
import pygame

# Base class for game objects
class CircleShape(pygame.sprite.Sprite):
    def __init__(self, x, y, radius):
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()

        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.radius = radius
        self.can_wrap = False
        

    def draw(self, screen):
        # must override
        pass

    def update(self, dt):
        # must override
        pass
    
    def collides_with(self, other): # only circle / circle collision
        return self.position.distance_to(other.position) < (self.radius + other.radius)
    
    def wrap_around_screen(self, screen_width, screen_height):
        if self.can_wrap == True:
            # Wrap horizontally
            if self.position.x > screen_width:
                self.position.x = 0
            elif self.position.x < 0:
                self.position.x = screen_width
            
            # Wrap vertically
            if self.position.y > screen_height:
                self.position.y = 0
            elif self.position.y < 0:
                self.position.y = screen_height