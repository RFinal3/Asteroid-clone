import random

import pygame

from bombpickup import BombPickup
from constants import PICKUP_DROP_CHANCE, PICKUP_SPAWN_DELAY_SECONDS
from shieldpickup import ShieldPickup
from speedpickup import SpeedPickup


class PickupSpawner(pygame.sprite.Sprite):
    containers: pygame.sprite.Group

    def __init__(self, sound_manager):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.elapsed_time = 0.0
        self.sound_manager = sound_manager

    def update(self, dt):
        self.elapsed_time += dt

    def try_spawn(self, position):
        if self.elapsed_time < PICKUP_SPAWN_DELAY_SECONDS:
            return False

        value = random.random()

        if value >= PICKUP_DROP_CHANCE:
            return False

        pickup_types = (ShieldPickup, SpeedPickup, BombPickup)

        pickup_weights = (70, 100, 30)
        chosen_pickup_class = random.choices(pickup_types, weights=pickup_weights, k=1)[
            0
        ]
        chosen_pickup_class(position.x, position.y, self.sound_manager)
        self.sound_manager.play("pickup_spawn")

        return True

    def force_spawn(self, pickup_type, position):
        pickup_types = {
            "shield": ShieldPickup,
            "speed": SpeedPickup,
            "bomb": BombPickup,
        }

        chosen_pickup_class = pickup_types[pickup_type]

        chosen_pickup_class(position.x, position.y, self.sound_manager)

        self.sound_manager.play("pickup_spawn")
