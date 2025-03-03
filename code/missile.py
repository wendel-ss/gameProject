import pygame
import os
from .settings import *

class Missile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load(os.path.join('assets', 'images', 'powerUpMissile.png'))
        self.image = pygame.transform.scale(self.image, (30, 50))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = -10  # Mais rápido que o tiro normal

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill() 