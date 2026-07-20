import pygame
from circleshape import CircleShape
from constants import (
    SHOT_RADIUS, 
    LINE_WIDTH, 
    LAYER_PROJECTILES,
    SHOT_LIFETIME_SECONDS
)

class Shot(CircleShape):
    _layer = LAYER_PROJECTILES
    def __init__(self, x, y):
        super().__init__(x, y, SHOT_RADIUS)
        self.lifetime = SHOT_LIFETIME_SECONDS

    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, LINE_WIDTH)

    def update(self, dt):
        self.position += self.velocity * dt
        self.lifetime -= dt

        if self.lifetime <= 0:
            self.kill()
            return