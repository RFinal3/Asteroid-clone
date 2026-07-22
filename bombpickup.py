import pygame
from pickup import Pickup
from constants import LINE_WIDTH

class BombPickup(Pickup):
    def __init__(self, x, y):
        super().__init__(x, y)


    def draw(self, screen):
        pygame.draw.circle(screen, "black", self.position, self.radius, 0)
        pygame.draw.circle(screen, "red", self.position, self.radius, LINE_WIDTH)


    def apply(self, player):
        player.add_bomb