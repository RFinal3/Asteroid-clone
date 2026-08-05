import pygame

from modernstroids.core.constants import LAYER_PROJECTILES, UFO_BULLET_RADIUS
from modernstroids.entities.shot import Shot


class UFOBullet(Shot):
    _layer = LAYER_PROJECTILES

    def __init__(self, x, y):
        super().__init__(x, y)
        self.radius = UFO_BULLET_RADIUS

    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, 0)
