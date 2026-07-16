from circleshape import *
from constants import *
from logger import *
import random

class Asteroid(CircleShape):
    def __init__(self, x: float, y: float, radius: float) -> None:
        super().__init__(x, y, radius)


    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, LINE_WIDTH)


    def update(self, dt):
        self.position += self.velocity * dt

    
    def split(self):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        
        log_event("asteroid_split")

        random_angle = random.uniform(20, 50)
        first_vector = self.velocity.rotate(random_angle)
        second_vector = first_vector.rotate(-random_angle)
        new_radius = self.radius - ASTEROID_MIN_RADIUS

        first_asteroid = Asteroid(self.position.x, self.position.y, new_radius)
        second_asteroid = Asteroid(self.position.x, self.position.y, new_radius)

        first_asteroid.velocity = first_vector * 1.2
        second_asteroid.velocity = second_vector * 1.2
