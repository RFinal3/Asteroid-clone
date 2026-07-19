import random
import pygame
from circleshape import CircleShape
from constants import LINE_WIDTH, ASTEROID_MIN_RADIUS
from logger import log_event
from utils import wrap_position

class Asteroid(CircleShape):
    def __init__(self, x: float, y: float, radius: float) -> None:
        super().__init__(x, y, radius)
        self.vertices = []
        vertex_count = 10
        angle_step = 360 / vertex_count

        for index in range(vertex_count):
            angle = index * angle_step

            radius_scale = random.uniform(0.60, 1.00)
            vertex_radius = self.radius * radius_scale
            vertex = pygame.Vector2(0, vertex_radius)

            rotation = vertex.rotate(angle)
            self.vertices.append(rotation)

    
    def world_vertices(self):
        points = []
        for vertex in self.vertices:
            point = self.position + vertex
            points.append(point)
        return points


    def draw(self, screen):
        points = self.world_vertices()
        pygame.draw.polygon(screen, "black", points, 0)
        pygame.draw.polygon(screen, "white", points, LINE_WIDTH)


    def update(self, dt):
        self.position += self.velocity * dt
        wrap_position(self.position, self.radius)

    
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
