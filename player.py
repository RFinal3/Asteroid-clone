import pygame
from constants import (
    PLAYER_RADIUS, 
    PLAYER_STARTING_LIVES, 
    PLAYER_MAX_SPEED, 
    LINE_WIDTH, 
    PLAYER_TURN_SPEED, 
    PLAYER_ACCELERATION,
    PLAYER_DECELERATION, 
    PLAYER_SHOOT_COOLDOWN_SECONDS, 
    PLAYER_SHOOT_SPEED,
    LAYER_PLAYER
    )
from circleshape import CircleShape
from shot import Shot
from utils import wrap_position

class Player(CircleShape):
    _layer = LAYER_PLAYER
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shot_cooldown = 0
        self.lives = PLAYER_STARTING_LIVES
        self.invulnerability_timer = 0
        self.velocity = pygame.Vector2(0, 0)
        self.max_speed = PLAYER_MAX_SPEED
    

    def draw(self, screen):
        points = self.triangle()
        pygame.draw.polygon(screen, "black", points, 0)
        pygame.draw.polygon(screen, "white", points, LINE_WIDTH)

    
    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def move(self, dt):
        unit_vector = pygame.Vector2(0, 1)
        rotated_vector = unit_vector.rotate(self.rotation)
        acceleration = rotated_vector * PLAYER_ACCELERATION * dt
        self.velocity += acceleration
        self.velocity.clamp_magnitude_ip(self.max_speed)

    def decelerate(self, dt):
        self.velocity.move_towards_ip(pygame.Vector2(0, 0), PLAYER_DECELERATION * dt)
        

    def shoot(self):
        if self.shot_cooldown > 0:
            return

        self.shot_cooldown = PLAYER_SHOOT_COOLDOWN_SECONDS

        shot = Shot(self.position.x, self.position.y)
        shot_vector = pygame.Vector2(0, 1)
        shot_vector = shot_vector.rotate(self.rotation)
        shot_vector = shot_vector * PLAYER_SHOOT_SPEED
        shot.velocity = shot_vector
        

    def update(self, dt: float) -> None:
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rotation -= PLAYER_TURN_SPEED * dt
        if keys[pygame.K_d]:
            self.rotation += PLAYER_TURN_SPEED * dt
        if keys[pygame.K_w]:
            self.move(dt) 
        if keys[pygame.K_s]:
            self.move(-dt)
        if keys[pygame.K_SPACE]:
            self.shoot()
        if not keys[pygame.K_w] and not keys[pygame.K_s]:
            self.decelerate(dt)

        self.position += self.velocity * dt

        self.shot_cooldown -= dt
        self.invulnerability_timer -= dt

        wrap_position(self.position, self.radius)


    # in the Player class
    def triangle(self) -> list[pygame.Vector2]:
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]