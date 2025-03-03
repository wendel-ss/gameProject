#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame
import os
import random
from .enemy_bullet import EnemyBullet
from .settings import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_type):
        super().__init__()
        self.enemy_type = enemy_type  # Guarda o tipo do inimigo
        self.image = pygame.image.load(os.path.join('assets', 'images', f'Enemy{enemy_type}.png'))
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()
        
        # Posição inicial aleatória no topo da tela
        self.rect.x = random.randint(0, WINDOW_WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -50)
        
        # Configurações baseadas no tipo de inimigo
        if enemy_type == 1:
            self.damage = 2
            self.shoot_delay = 2000  # Atira mais rápido
            self.speed_y = 1
        elif enemy_type == 2:
            self.damage = 5
            self.shoot_delay = 2500
            self.speed_y = 1.5
        else:  # enemy_type 3
            self.damage = 10
            self.shoot_delay = 3000  # Atira mais devagar
            self.speed_y = 2
        
        self.speed_x = random.choice([-2, -1, 1, 2])
        self.last_shot = pygame.time.get_ticks()
        self.health = 100
        self.bullets = pygame.sprite.Group()  # Grupo para rastrear os tiros deste inimigo
    
    def update(self):
        # Movimento
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        
        # Muda direção ao atingir as bordas
        if self.rect.left < 0 or self.rect.right > WINDOW_WIDTH:
            self.speed_x *= -1
            
        # Reposiciona quando sair da tela
        if self.rect.top > WINDOW_HEIGHT:
            self.reposition()
            
        # Verifica se deve atirar
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.shoot()
            self.last_shot = now
    
    def shoot(self):
        bullet = EnemyBullet(self.rect.centerx, self.rect.bottom)
        bullet.enemy_type = self.enemy_type  # Adiciona o tipo do inimigo ao projétil
        self.bullets.add(bullet)
        return bullet
    
    def reposition(self):
        self.rect.x = random.randint(0, WINDOW_WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -50)
        self.speed_x = random.choice([-2, -1, 1, 2])
    
    def take_damage(self, damage):
        self.health -= damage
        return self.health <= 0

    def get_damage(self):
        return self.damage
