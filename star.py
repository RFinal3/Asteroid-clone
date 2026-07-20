import pygame
import random
from constants import (
    STAR_SYMBOLS, 
    MIN_TWINKLE_INTERVAL, 
    MAX_TWINKLE_INTERVAL
)

class Star():
    def __init__(self, x, y):
        self.position: pygame.Vector2 = pygame.Vector2(x, y)
        self.symbol = random.choice(STAR_SYMBOLS)
        self.twinkle_interval = random.uniform(MIN_TWINKLE_INTERVAL, MAX_TWINKLE_INTERVAL)
        self.twinkle_timer = self.twinkle_interval
    
    def draw(self, screen, star_surface):
        star_center = star_surface.get_rect(center=self.position)
        screen.blit(star_surface, star_center)

    def update(self, dt):
        self.twinkle_timer -= dt
        if self.twinkle_timer <= 0:
            self.symbol = random.choice(STAR_SYMBOLS)
            self.twinkle_timer = self.twinkle_interval