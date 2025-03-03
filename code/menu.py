import pygame
from .settings import *
import os

class Menu:
    def __init__(self):
        self.font = pygame.font.Font(None, 74)
        self.selected_option = 0
        self.options = ['Jogar', 'Opções', 'Sair']
        
        # Carrega e ajusta o background
        background_path = os.path.join('assets', 'images', 'backgroundMenu.png')
        self.background = pygame.image.load(background_path)
        self.background = pygame.transform.scale(self.background, (WINDOW_WIDTH, WINDOW_HEIGHT))
        
    def draw(self, screen):
        # Desenha o background
        screen.blit(self.background, (0, 0))
        
        # Desenha as opções do menu
        for i, option in enumerate(self.options):
            color = RED if i == self.selected_option else WHITE
            text = self.font.render(option, True, color)
            rect = text.get_rect(center=(WINDOW_WIDTH/2, 200 + i * 100))
            screen.blit(text, rect)
            
    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_option = (self.selected_option - 1) % len(self.options)
                elif event.key == pygame.K_DOWN:
                    self.selected_option = (self.selected_option + 1) % len(self.options)
                elif event.key == pygame.K_RETURN:
                    if self.selected_option == 0:
                        return 'play'
                    elif self.selected_option == 1:
                        return 'options'
                    elif self.selected_option == 2:
                        return 'quit'
        return None 