import pygame
from constants import LINE_WIDTH
from pickup import Pickup

class ShieldPickup(Pickup):
    def __init__(self, x, y):
        super().__init__(x, y)


    def draw(self, screen):
        pygame.draw.circle(screen, "black", self.position, self.radius, 0)
        pygame.draw.circle(screen, "blue", self.position, self.radius, LINE_WIDTH)


    def apply(self, player):
        player.add_shield


