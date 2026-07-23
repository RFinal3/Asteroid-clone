import random
import pygame
from ufo import UFO
from constants import (
    UFO_INITIAL_SPAWN_DELAY_SECONDS,
    UFO_CAP_INCREASE_INTERVAL_SECONDS,
    UFO_MAX_COUNT,
    UFO_SPAWN_CHANCE,
    UFO_RADIUS,
    SCREEN_HEIGHT,
    SCREEN_WIDTH
)

class UFOSpawner:
    def __init__(self, player, ufos, game):
        self.target = player
        self.ufos = ufos
        self.elapsed_time = 0.0
        self.game = game


    def get_current_cap(self):
        if self.game.elapsed_time < UFO_INITIAL_SPAWN_DELAY_SECONDS:
            return 0

        completed_intervals = int(
            (self.game.elapsed_time - UFO_INITIAL_SPAWN_DELAY_SECONDS) 
        // UFO_CAP_INCREASE_INTERVAL_SECONDS
        )

        current_cap = completed_intervals + 1

        return min(current_cap, UFO_MAX_COUNT)

    
    def try_spawn(self):
        current_cap = self.get_current_cap()


        if len(self.ufos) >= current_cap:
            return False


        value = random.random()


        if value >= UFO_SPAWN_CHANCE:
            return False

        
        self.spawn_random_ufo()
        return True


    def spawn_random_ufo(self):
        edge = random.choice(("left", "right", "top", "bottom"))


        if edge == "left":
            position = pygame.Vector2(
                -UFO_RADIUS,
                random.uniform(0, SCREEN_HEIGHT)
            )
            
        elif edge == "right":
            position = pygame.Vector2(
                SCREEN_WIDTH + UFO_RADIUS,
                random.uniform(0, SCREEN_HEIGHT)
            )

        elif edge == "top":
            position = pygame.Vector2(
                random.uniform(0, SCREEN_WIDTH),
                -UFO_RADIUS
            )

        elif edge == "bottom":
            position = pygame.Vector2(
                random.uniform(0, SCREEN_WIDTH),
                SCREEN_HEIGHT + UFO_RADIUS
            )

        UFO(position.x, position.y, self.target)
            