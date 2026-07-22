import pygame
from constants import (
    SCREEN_HEIGHT, 
    SCREEN_WIDTH, 
    LAYER_SCREEN_FLASH
)

class ScreenFlash(pygame.sprite.Sprite):
    containers: pygame.sprite.Group
    _layer = LAYER_SCREEN_FLASH


    def __init__(self, duration):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.duration = duration    
        self.timer = duration
        self.surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.surface.fill("white")


    def update(self, dt):
        self.timer -= dt
        if self.timer <= 0:
            self.kill()

    
    def draw(self, screen):
        progress = self.timer / self.duration
        alpha = int(255 * progress)
        self.surface.set_alpha(alpha)

        screen.blit(self.surface, (0, 0))