#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame
import random
import os
from .settings import *

class Asteroid(pygame.sprite.Sprite):
    def __init__(self, image_name):
        super().__init__()
        # Carrega a imagem do asteroide
        image_path = os.path.join('assets', 'images', image_name)
        self.original_image = pygame.image.load(image_path)
        self.original_image = pygame.transform.scale(self.original_image, (50, 50))  # Ajuste o tamanho conforme necessário
        self.image = self.original_image
        self.rect = self.image.get_rect()
        
        # Posição inicial aleatória nas bordas da tela
        side = random.choice(['top', 'right', 'bottom', 'left'])
        if side == 'top':
            self.rect.x = random.randint(0, WINDOW_WIDTH)
            self.rect.y = -50
        elif side == 'right':
            self.rect.x = WINDOW_WIDTH + 50
            self.rect.y = random.randint(0, WINDOW_HEIGHT)
        elif side == 'bottom':
            self.rect.x = random.randint(0, WINDOW_WIDTH)
            self.rect.y = WINDOW_HEIGHT + 50
        else:
            self.rect.x = -50
            self.rect.y = random.randint(0, WINDOW_HEIGHT)
        
        # Velocidade e rotação
        self.min_speed = 1
        self.max_speed = 2
        self.reset_speed()
        self.rotation = 0
        self.rotation_speed = random.uniform(-2, 2)
    
    def reset_speed(self):
        """Define novas velocidades garantindo movimento adequado"""
        self.speed_x = random.uniform(-self.max_speed, self.max_speed)
        self.speed_y = random.uniform(-self.max_speed, self.max_speed)
        
        # Garante velocidade mínima em ambos os eixos
        if abs(self.speed_x) < self.min_speed:
            self.speed_x = self.min_speed if random.random() > 0.5 else -self.min_speed
        if abs(self.speed_y) < self.min_speed:
            self.speed_y = self.min_speed if random.random() > 0.5 else -self.min_speed
    
    def update(self):
        # Movimento
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        
        # Rotação
        self.rotation = (self.rotation + self.rotation_speed) % 360
        self.image = pygame.transform.rotate(self.original_image, self.rotation)
        self.rect = self.image.get_rect(center=self.rect.center)
        
        # Reposiciona quando sair da tela
        if self.rect.right < -50 or self.rect.left > WINDOW_WIDTH + 50 or \
           self.rect.bottom < -50 or self.rect.top > WINDOW_HEIGHT + 50:
            self.reposition()
    
    def reposition(self):
        side = random.choice(['top', 'right', 'bottom', 'left'])
        if side == 'top':
            self.rect.x = random.randint(0, WINDOW_WIDTH)
            self.rect.y = -50
        elif side == 'right':
            self.rect.x = WINDOW_WIDTH + 50
            self.rect.y = random.randint(0, WINDOW_HEIGHT)
        elif side == 'bottom':
            self.rect.x = random.randint(0, WINDOW_WIDTH)
            self.rect.y = WINDOW_HEIGHT + 50
        else:
            self.rect.x = -50
            self.rect.y = random.randint(0, WINDOW_HEIGHT)
        
        self.reset_speed()
    
    def bounce(self):
        """Melhorado sistema de ricochete"""
        # Inverte direções com um fator aleatório
        self.speed_x = -self.speed_x * random.uniform(0.8, 1.2)
        self.speed_y = -self.speed_y * random.uniform(0.8, 1.2)
        
        # Adiciona pequena variação aleatória
        self.speed_x += random.uniform(-0.5, 0.5)
        self.speed_y += random.uniform(-0.5, 0.5)
        
        # Garante velocidades mínimas e máximas
        if abs(self.speed_x) < self.min_speed:
            self.speed_x = self.min_speed if self.speed_x > 0 else -self.min_speed
        if abs(self.speed_y) < self.min_speed:
            self.speed_y = self.min_speed if self.speed_y > 0 else -self.min_speed
            
        # Limita velocidade máxima
        self.speed_x = max(min(self.speed_x, self.max_speed), -self.max_speed)
        self.speed_y = max(min(self.speed_y, self.max_speed), -self.max_speed)
