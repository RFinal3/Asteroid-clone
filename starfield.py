import random
import pygame
from star import Star
from constants import STAR_SYMBOLS

class StarField:
    def __init__(self, width, height, min_star_count, max_star_count):
        self.star_font = pygame.font.Font(None, 12)
        self.stars = []

        self.symbol_surfaces = {}
        for symbol in STAR_SYMBOLS:
            render_symbol = self.star_font.render(symbol, True, "white")
            self.symbol_surfaces[symbol] = render_symbol
        star_count = random.randint(min_star_count, max_star_count)

        for _ in range(star_count):
            position_x = random.randint(0, width - 1)
            position_y = random.randint(0, height - 1)
            star_true_position = Star(position_x, position_y)
            self.stars.append(star_true_position)

    def draw(self, screen):
        for star in self.stars:
            star_surface = self.symbol_surfaces[star.symbol]
            star.draw(screen, star_surface)

    
    def update(self, dt):
        for star in self.stars:
            star.update(dt)