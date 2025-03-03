import pygame
import os
import random
from .settings import *

class PowerUp(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(os.path.join('assets', 'images', 'powerUp.png'))
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()
        
        # Posição inicial aleatória
        self.rect.x = random.randint(50, WINDOW_WIDTH - 50)
        self.rect.y = -50
        self.speed_y = 1

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.top > WINDOW_HEIGHT:
            self.kill() 