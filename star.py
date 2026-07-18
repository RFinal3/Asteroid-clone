import pygame
import random
from constants import *

class Star():
    def __init__(self, x, y):
        self.position: pygame.Vector2 = pygame.Vector2(x, y)
        self.symbol = random.choice(STAR_SYMBOLS)
    
    def draw(self, screen, font):
        star = font.render(self.symbol, True, "white")
        star_center = star.get_rect(center=self.position)
        screen.blit(star, star_center)
        