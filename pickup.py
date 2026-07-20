from circleshape import CircleShape
from constants import (
    LAYER_PICKUPS, 
    PICKUP_RADIUS
)

class Pickup(CircleShape):
    _layer = LAYER_PICKUPS
    def __init__(self, x, y):
        super().__init__(x, y, PICKUP_RADIUS)

    def draw(self, screen):
        raise NotImplementedError

    def collect(self, player):
        self.apply(player)
        self.kill()

    def apply(self, player):
        raise NotImplementedError