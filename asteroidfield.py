import random
from collections.abc import Callable
import pygame
from asteroid import Asteroid
from constants import (
    ASTEROID_KINDS,
    ASTEROID_MAX_RADIUS,
    ASTEROID_MIN_RADIUS,
    ASTEROID_SPAWN_RATE_SECONDS,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    ASTEROID_STARTING_MAX_COUNT,
    ASTEROID_CAP_INCREASE_PER_LEVEL,
    ASTEROID_SPAWN_RATE_DECREASE_PER_LEVEL,
    ASTEROID_MAX_SCALING_LEVEL
)

Edge = tuple[pygame.Vector2, Callable[[float], pygame.Vector2]]


class AsteroidField(pygame.sprite.Sprite):
    containers: pygame.sprite.Group

    edges: list[Edge] = [
        (
            pygame.Vector2(1, 0),
            lambda y: pygame.Vector2(-ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT),
        ),
        (
            pygame.Vector2(-1, 0),
            lambda y: pygame.Vector2(
                SCREEN_WIDTH + ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT
            ),
        ),
        (
            pygame.Vector2(0, 1),
            lambda x: pygame.Vector2(x * SCREEN_WIDTH, -ASTEROID_MAX_RADIUS),
        ),
        (
            pygame.Vector2(0, -1),
            lambda x: pygame.Vector2(
                x * SCREEN_WIDTH, SCREEN_HEIGHT + ASTEROID_MAX_RADIUS
            ),
        ),
    ]


    def __init__(self, asteroids, game) -> None:
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.spawn_timer = 0.0
        self.asteroids = asteroids
        self.spawning_paused = False
        self.spawn_pause_timer = 0.0
        self.game = game
        

    def spawn(
        self, radius: float, position: pygame.Vector2, velocity: pygame.Vector2
    ) -> None:
        asteroid = Asteroid(position.x, position.y, radius)
        asteroid.velocity = velocity


    def update(self, dt: float) -> None:
        current_spawn_rate = self.get_current_spawn_rate()

        if self.spawn_timer > current_spawn_rate:
            self.spawn_pause_timer = max(
                0.0,
                self.spawn_pause_timer - dt,
            )

        if self.spawning_paused or self.spawn_pause_timer > 0:
            return

        self.spawn_timer += dt
        if self.spawn_timer > ASTEROID_SPAWN_RATE_SECONDS:
            self.spawn_timer = 0
            current_cap = self.get_current_cap()

            if len(self.asteroids) >= current_cap:
                return

            self.spawn_random_asteroid()

    
    def spawn_random_asteroid(self):
        edge = random.choice(self.edges)
        speed = random.randint(40, 100)
        velocity = edge[0] * speed
        velocity = velocity.rotate(random.randint(-30, 30))
        position = edge[1](random.uniform(0, 1))
        kind = random.randint(1, ASTEROID_KINDS)
        self.spawn(ASTEROID_MIN_RADIUS * kind, position, velocity)

    
    def toggle_spawning(self):
        self.spawning_paused = not self.spawning_paused


    def pause_spawning(self, duration):
        self.spawn_pause_timer = max(self.spawn_pause_timer, duration)

    
    def get_current_spawn_rate(self):
        scaling_level = min(self.game.difficulty_level, ASTEROID_MAX_SCALING_LEVEL)

        levels_above_one = scaling_level - 1

        rate_reduction = (levels_above_one * ASTEROID_SPAWN_RATE_DECREASE_PER_LEVEL)

        return ASTEROID_SPAWN_RATE_SECONDS - rate_reduction

    def get_current_cap(self):
        scaling_level = min(
            self.game.difficulty_level,
            ASTEROID_MAX_SCALING_LEVEL,
        )
        levels_above_one = scaling_level - 1

        cap_increase = (
            levels_above_one
            * ASTEROID_CAP_INCREASE_PER_LEVEL
        )

        return ASTEROID_STARTING_MAX_COUNT + cap_increase