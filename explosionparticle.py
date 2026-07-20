import random
import pygame
from circleshape import CircleShape
from constants import (
    EXPLOSION_RADIUS, 
    EXPLOSION_TIMER, 
    LINE_WIDTH, 
    LAYER_EFFECTS
)

class ExplosionParticle(CircleShape):
    _layer = LAYER_EFFECTS
    def __init__(self, x, y):
        super().__init__(x, y, EXPLOSION_RADIUS)
        self.timer = EXPLOSION_TIMER

        vector = pygame.Vector2(1, 0)
        random_angle = random.uniform(0, 360)
        vector = vector.rotate(random_angle)

        self.velocity = vector * random.uniform(60, 160) * 1.2

    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, LINE_WIDTH)

    def update(self, dt):
        self.position += self.velocity * dt
        self.timer -= dt

        if self.timer <= 0:
            self.kill()