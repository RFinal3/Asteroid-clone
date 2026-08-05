import pygame

from constants import LINE_WIDTH
from modernstroids.entities.pickups.pickup import Pickup


class SpeedPickup(Pickup):
    def draw(self, screen):
        pygame.draw.circle(screen, "black", self.position, self.radius, 0)
        pygame.draw.circle(screen, "green", self.position, self.radius, LINE_WIDTH)

    def apply(self, player):
        player.add_speed_boost()
        self.sound_manager.play("speed_boost_collected")
