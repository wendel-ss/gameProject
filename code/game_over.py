import pygame
import os
import math
from .settings import *
from .database import ScoreDatabase

class GameOver:
    def __init__(self, score, victory=False):
        self.score = score
        self.victory = victory
        self.font_big = pygame.font.Font(None, 120)
        self.font = pygame.font.Font(None, 74)
        self.small_font = pygame.font.Font(None, 36)
        self.db = ScoreDatabase()
        self.player_name = ""
        self.options = ['Salvar', 'Sair']
        self.selected_option = 0
        self.state = 'choosing'  # Estados: 'choosing', 'entering_name'
        self.animation_timer = 0

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'
            
            if self.state == 'choosing':
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        self.selected_option = (self.selected_option + 1) % len(self.options)
                    elif event.key == pygame.K_RETURN:
                        if self.selected_option == 0:  # Salvar
                            self.state = 'entering_name'
                        else:  # Sair
                            return 'menu'
            
            elif self.state == 'entering_name':
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and self.player_name.strip():
                        self.db.save_score(self.player_name, self.score)
                        return 'menu'
                    elif event.key == pygame.K_BACKSPACE:
                        self.player_name = self.player_name[:-1]
                    elif event.key == pygame.K_ESCAPE:
                        self.state = 'choosing'
                    else:
                        if len(self.player_name) < 15:  # Limite de 15 caracteres
                            self.player_name += event.unicode
        return None

    def draw(self, screen):
        screen.fill(BLACK)
        
        # Título (GAME OVER ou VITÓRIA)
        title_text = "VITÓRIA!" if self.victory else "GAME OVER"
        title_color = GREEN if self.victory else RED
        
        # Efeito de pulsar
        pulse = (math.sin(pygame.time.get_ticks() * 0.004) + 1) * 0.2 + 0.8
        title_size = int(120 * pulse)
        font_pulse = pygame.font.Font(None, title_size)
        
        title = font_pulse.render(title_text, True, title_color)
        title_shadow = font_pulse.render(title_text, True, BLACK)
        
        title_rect = title.get_rect(center=(WINDOW_WIDTH/2, 150))
        screen.blit(title_shadow, (title_rect.x + 4, title_rect.y + 4))
        screen.blit(title, title_rect)
        
        # Pontuação
        score_text = f"Pontuação: {self.score}"
        score_surface = self.font.render(score_text, True, WHITE)
        score_rect = score_surface.get_rect(center=(WINDOW_WIDTH/2, 250))
        screen.blit(score_surface, score_rect)

        if self.state == 'choosing':
            # Opções (Salvar/Sair)
            for i, option in enumerate(self.options):
                color = RED if i == self.selected_option else WHITE
                text = self.font.render(option, True, color)
                rect = text.get_rect(center=(WINDOW_WIDTH/2, 350 + i * 70))
                screen.blit(text, rect)
            
            # Instruções modificadas
            inst = self.small_font.render("Use SETAS para selecionar e ENTER para confirmar", True, WHITE)
            inst_rect = inst.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT - 100))
            screen.blit(inst, inst_rect)

        elif self.state == 'entering_name':
            # Campo de nome
            name_prompt = self.font.render("Digite seu nome:", True, WHITE)
            name_rect = name_prompt.get_rect(center=(WINDOW_WIDTH/2, 350))
            screen.blit(name_prompt, name_rect)
            
            name_text = self.font.render(self.player_name + "_", True, WHITE)
            name_text_rect = name_text.get_rect(center=(WINDOW_WIDTH/2, 420))
            screen.blit(name_text, name_text_rect)
            
            # Instruções
            inst = self.small_font.render("Pressione ENTER para salvar ou ESC para voltar", True, WHITE)
            inst_rect = inst.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT - 100))
            screen.blit(inst, inst_rect)

        pygame.display.flip() 