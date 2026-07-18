import pygame
from constants import *
from circleshape import *
from shot import *

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shot_cooldown = 0
        self.lives = PLAYER_STARTING_LIVES
        self.invulnerability_timer = 0
        self.velocity = pygame.Vector2(0, 0)
    

    def draw(self, screen):
        pygame.draw.polygon(screen, "white", self.triangle(), LINE_WIDTH)

    
    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def move(self, dt):
        unit_vector = pygame.Vector2(0, 1)
        rotated_vector = unit_vector.rotate(self.rotation)
        acceleration = rotated_vector * PLAYER_ACCELERATION * dt
        self.velocity += acceleration

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

        self.position += self.velocity * dt

        self.shot_cooldown -= dt
        self.invulnerability_timer -= dt


    # in the Player class
    def triangle(self) -> list[pygame.Vector2]:
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
        