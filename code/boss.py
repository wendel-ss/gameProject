#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame
import os
from .settings import *
from .enemy_bullet import EnemyBullet
from .boss_bullet import BossBullet

class Boss(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Carrega a imagem do boss
        self.image = pygame.image.load(os.path.join('assets', 'images', 'Boss.png'))
        self.image = pygame.transform.scale(self.image, (150, 150))  # Ajuste o tamanho conforme necessário
        self.rect = self.image.get_rect()
        
        # Posição inicial
        self.rect.centerx = WINDOW_WIDTH // 2
        self.rect.y = 100
        
        # Atributos
        self.health = 500
        self.max_health = 500
        self.speed = 3
        self.direction = 1  # 1 para direita, -1 para esquerda
        
        # Ajusta controle de tiro
        self.shoot_delay = 1000  # 3 segundos entre sequências de tiros
        self.last_shot = pygame.time.get_ticks()
        self.can_shoot = True
    
    def update(self):
        # Movimento lateral
        self.rect.x += self.speed * self.direction
        
        # Muda direção nas bordas
        if self.rect.right > WINDOW_WIDTH - 50:
            self.direction = -1
        elif self.rect.left < 50:
            self.direction = 1
            
        # Atualiza tiros
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot > self.shoot_delay:
            self.can_shoot = True
    
    def shoot(self):
        if self.can_shoot:
            self.can_shoot = False
            self.last_shot = pygame.time.get_ticks()
            return BossBullet(self.rect.centerx, self.rect.bottom)
        return None
    
    def take_damage(self, damage):
        self.health -= damage
        return self.health <= 0
