from circleshape import CircleShape
from constants import (
    LAYER_PICKUPS, 
    PICKUP_RADIUS,
    PICKUP_LIFETIME_SECONDS
)

class Pickup(CircleShape):
    _layer = LAYER_PICKUPS
    def __init__(self, x, y):
        super().__init__(x, y, PICKUP_RADIUS)
        self.lifetime = PICKUP_LIFETIME_SECONDS


    def draw(self, screen):
        raise NotImplementedError


    def collect(self, player):
        self.apply(player)
        self.kill()


    def apply(self, player):
        raise NotImplementedError


    def update(self, dt):
        self.lifetime -= dt
        
        if self.lifetime <= 0:
            self.kill()
            return