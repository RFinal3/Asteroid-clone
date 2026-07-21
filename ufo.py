import pygame
from circleshape import CircleShape
from ufobullet import UFOBullet
from constants import (
    UFO_RADIUS,
    LAYER_UFO,
    LINE_WIDTH,
    UFO_COLOR,
    UFO_MIN_DISTANCE,
    UFO_MAX_DISTANCE,
    UFO_ACCELERATION,
    UFO_DECELERATION,
    UFO_MAX_SPEED,
    UFO_SHOOT_COOLDOWN_SECONDS,
    UFO_SHOOT_SPEED,
    SCREEN_WIDTH,
    SCREEN_HEIGHT
)

class UFO(CircleShape):
    _layer = LAYER_UFO
    def __init__(self, x, y, player):
        super().__init__(x, y, UFO_RADIUS)
        self.target = player
        self.acceleration = UFO_ACCELERATION
        self.max_speed = UFO_MAX_SPEED
        self.shot_cooldown = UFO_SHOOT_COOLDOWN_SECONDS

        self.vertices = [
            pygame.Vector2(-self.radius * 0.35, -self.radius * 0.55),
            pygame.Vector2(self.radius * 0.35, -self.radius * 0.55),
            pygame.Vector2(self.radius * 0.60, -self.radius * 0.20),
            pygame.Vector2(self.radius, 0),
            pygame.Vector2(self.radius * 0.60, self.radius * 0.35),
            pygame.Vector2(-self.radius * 0.60, self.radius * 0.35),
            pygame.Vector2(-self.radius, 0),
            pygame.Vector2(-self.radius * 0.60, -self.radius * 0.20),
        ]

    def world_vertices(self):
        points = []

        for vertex in self.vertices:
            points.append(self.position + vertex)

        return points


    def draw(self, screen):
        points = self.world_vertices()
        pygame.draw.polygon(screen, UFO_COLOR, points, 0)
        pygame.draw.polygon(screen, "black", points, LINE_WIDTH)

        pygame.draw.line(
            screen,
            "black",
            points[7],
            points[2],
            LINE_WIDTH,
        )

    
    def shoot(self):
        if self.shot_cooldown > 0:
            return

        to_target = self.target.position - self.position

        if to_target.length_squared() == 0:
            return

        self.shot_cooldown = UFO_SHOOT_COOLDOWN_SECONDS

        bullet = UFOBullet(self.position.x, self.position.y)
        bullet_vector = to_target.normalize()
        bullet_vector = bullet_vector * UFO_SHOOT_SPEED
        bullet.velocity = bullet_vector


    def update(self, dt):
        to_target = self.target.position - self.position
        distance_to_target = to_target.length()
        correcting_position = self.keep_on_screen(dt)

        if not correcting_position:

            if distance_to_target > UFO_MAX_DISTANCE:
                self.move(dt, to_target)

            elif distance_to_target < UFO_MIN_DISTANCE:
                self.move(dt, -to_target)

            else:
                self.velocity.move_towards_ip(pygame.Vector2(0, 0), UFO_DECELERATION * dt)

            self.shoot()
        
        self.position += self.velocity * dt
        self.shot_cooldown -= dt

    
    def move(self, dt, to_target):
        if to_target.length_squared() == 0:
            return

        direction_to_target = to_target.normalize()
        acceleration = direction_to_target * self.acceleration * dt
        self.velocity += acceleration

        if self.velocity.length_squared() > 0:
            self.velocity.clamp_magnitude_ip(self.max_speed)

    
    def keep_on_screen(self, dt):
        correcting_position = False

        if self.position.x < self.radius:
            self.move(dt, pygame.Vector2(1, 0))
            correcting_position = True

        if self.position.x > SCREEN_WIDTH - self.radius:
            self.move(dt, pygame.Vector2(-1, 0))
            correcting_position = True
        
        if self.position.y < self.radius:
            self.move(dt, pygame.Vector2(0, 1))
            correcting_position = True

        if self.position.y > SCREEN_HEIGHT - self.radius:
            self.move(dt, pygame.Vector2(0, -1))
            correcting_position = True
        
        return correcting_position