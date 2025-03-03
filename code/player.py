#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame
import os
from .settings import *
from .bullet import Bullet
from .missile import Missile

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Carrega as imagens
        self.normal_image = pygame.image.load(os.path.join('assets', 'images', 'player1.png'))
        
        # Redimensiona as imagens se necessário (ajuste o tamanho conforme precisar)
        self.normal_image = pygame.transform.scale(self.normal_image, (50, 50))
        
        self.image = self.normal_image
        self.rect = self.image.get_rect()
        self.rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        
        self.speed = PLAYER_SPEED
        self.health = 100
        self.invulnerable = False
        self.invulnerable_timer = 0
        
        # Controle de tiro
        self.is_shooting = False
        self.shoot_timer = 0
        self.shoot_delay = 300  # Tempo entre tiros em milissegundos
        
        self.missiles = 0  # Contador de mísseis
        self.max_missiles = 5  # Limite máximo de mísseis
        self.missile_shoot_delay = 500  # Delay entre disparos de mísseis (500ms)
    
    def update(self):
        keys = pygame.key.get_pressed()
        
        # Movimento
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed
            
        # Tiro (usando a tecla ESPAÇO)
        current_time = pygame.time.get_ticks()
        if keys[pygame.K_SPACE]:
            if current_time - self.shoot_timer > self.shoot_delay:
                self.is_shooting = True
                self.shoot_timer = current_time
        else:
            self.is_shooting = False
            
        # Mantém o jogador dentro da tela
        self.rect.clamp_ip(pygame.display.get_surface().get_rect())
        
        # Controle de invulnerabilidade
        if self.invulnerable:
            if current_time - self.invulnerable_timer > 1000:
                self.invulnerable = False
    
    def shoot(self):
        # Cria um novo projétil
        bullet = Bullet(self.rect.centerx, self.rect.top)
        return bullet

    def shoot_missile(self):
        if self.missiles > 0:
            self.missiles -= 1  # Subtrai apenas um míssil
            return Missile(self.rect.centerx, self.rect.top)
        return None

    def collect_powerup(self):
        if self.missiles < self.max_missiles:
            self.missiles += 1

    def take_damage(self, damage_amount):
        if not self.invulnerable:
            self.health -= damage_amount
            self.invulnerable = True
            self.invulnerable_timer = pygame.time.get_ticks()

    def update_ship(self, ship_image):
        self.image = pygame.image.load(os.path.join('assets', 'images', ship_image))
        self.image = pygame.transform.scale(self.image, (50, 50))  # Ajuste o tamanho conforme necessário
