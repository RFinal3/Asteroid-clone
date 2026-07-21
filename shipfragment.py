import pygame
import random
from constants import (LAYER_EFFECTS, 
        LINE_WIDTH,
        SHIP_FRAGMENT_SPEED,
        SHIP_FRAGMENT_LIFETIME_SECONDS,
        SHIP_FRAGMENT_ROTATION_SPEED
        )


class ShipFragment(pygame.sprite.Sprite):
    containers: pygame.sprite.Group
    _layer = LAYER_EFFECTS


    def __init__(self, start, end, origin):
        pygame.sprite.Sprite.__init__(self, self.containers)

        sign_choice = random.choice((1, -1))
        start_point = pygame.Vector2(start)
        end_point = pygame.Vector2(end)
        self.position = (start_point + end_point) / 2
        outward_vector = self.position - origin

        if outward_vector.length_squared() > 0:
            outward_vector.normalize_ip()

        self.velocity = outward_vector * SHIP_FRAGMENT_SPEED
        self.local_start = start_point - self.position
        self.local_end = end_point - self.position
        self.lifetime = SHIP_FRAGMENT_LIFETIME_SECONDS
        self.rotation = 0.0
        self.rotation_speed = SHIP_FRAGMENT_ROTATION_SPEED * sign_choice
        


    def draw(self, screen):
        rotated_start = self.local_start.rotate(self.rotation)
        rotated_end = self.local_end.rotate(self.rotation)

        world_start = self.position + rotated_start
        world_end = self.position + rotated_end

        pygame.draw.line(screen, "white", world_start, world_end, LINE_WIDTH)

    
    def update(self, dt):
        self.position += self.velocity * dt
        self.lifetime -= dt
        self.rotation += self.rotation_speed * dt
        if self.lifetime <= 0:
            self.kill()


def spawn_ship_fragments(triangle_points, origin):
    ShipFragment(triangle_points[0], triangle_points[1], origin)
    ShipFragment(triangle_points[1], triangle_points[2], origin)
    ShipFragment(triangle_points[2], triangle_points[0], origin)
