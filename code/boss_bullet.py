import pygame
import os
from .settings import *

class BossBullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load(os.path.join('assets', 'images', 'shotBoss.png'))
        self.image = pygame.transform.scale(self.image, (40, 40))  # Ajuste o tamanho conforme necessário
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.top = y
        self.speed = 8
        self.damage = 20  # Dano do tiro do boss
        
    def update(self):
        self.rect.y += self.speed
        if self.rect.top > WINDOW_HEIGHT:
            self.kill() 