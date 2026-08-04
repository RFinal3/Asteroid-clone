from circleshape import CircleShape
from constants import LAYER_PICKUPS, PICKUP_LIFETIME_SECONDS, PICKUP_RADIUS


class Pickup(CircleShape):
    _layer = LAYER_PICKUPS

    def __init__(self, x, y, sound_manager):
        super().__init__(x, y, PICKUP_RADIUS)
        self.lifetime = PICKUP_LIFETIME_SECONDS
        self.sound_manager = sound_manager

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
