import pygame
import os

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Carrega a imagem do tiro
        self.image = pygame.image.load(os.path.join('assets', 'images', 'shotPlayer1.png'))
        self.image = pygame.transform.scale(self.image, (30, 30))  # Ajuste o tamanho conforme necessário
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = -20  # Velocidade negativa para ir para cima

    def update(self):
        self.rect.y += self.speed
        # Remove o projétil se sair da tela
        if self.rect.bottom < 0:
            self.kill() 