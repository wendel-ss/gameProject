import pygame
import os
from .settings import *
from .database import ScoreDatabase

class Options:
    def __init__(self):
        self.font = pygame.font.Font(None, 74)
        self.small_font = pygame.font.Font(None, 36)
        self.options = ['Escolher Nave', 'High Scores', 'Voltar']
        self.selected_option = 0
        self.state = 'main'  # Estados: 'main', 'ships', 'scores'
        self.db = ScoreDatabase()
        
        # Carrega o background do menu
        background_path = os.path.join('assets', 'images', 'backgroundMenu.png')
        self.background = pygame.image.load(background_path)
        self.background = pygame.transform.scale(self.background, (WINDOW_WIDTH, WINDOW_HEIGHT))
        
        # Carrega as imagens das naves
        self.ships = [
            {
                'image': pygame.image.load(os.path.join('assets', 'images', 'player1.png')),
                'name': 'Nave 1',
                'selected': True
            },
            {
                'image': pygame.image.load(os.path.join('assets', 'images', 'player2.png')),
                'name': 'Nave 2',
                'selected': False
            }
        ]
        
        # Redimensiona as imagens das naves
        for ship in self.ships:
            ship['image'] = pygame.transform.scale(ship['image'], (100, 100))
    
    def draw(self, screen):
        # Desenha o background em todos os estados
        screen.blit(self.background, (0, 0))
        
        if self.state == 'main':
            # Menu principal de opções
            for i, option in enumerate(self.options):
                color = RED if i == self.selected_option else WHITE
                text = self.font.render(option, True, color)
                rect = text.get_rect(center=(WINDOW_WIDTH/2, 200 + i * 100))
                screen.blit(text, rect)
                
        elif self.state == 'ships':
            # Menu de seleção de nave
            title = self.font.render('Escolha sua Nave', True, WHITE)
            screen.blit(title, title.get_rect(center=(WINDOW_WIDTH/2, 100)))
            
            for i, ship in enumerate(self.ships):
                # Desenha a nave
                ship_rect = ship['image'].get_rect(center=(WINDOW_WIDTH/3 + i * WINDOW_WIDTH/3, 300))
                screen.blit(ship['image'], ship_rect)
                
                # Desenha o nome
                name_color = RED if ship['selected'] else WHITE
                name_text = self.small_font.render(ship['name'], True, name_color)
                name_rect = name_text.get_rect(center=(ship_rect.centerx, ship_rect.bottom + 30))
                screen.blit(name_text, name_rect)
            
            # Instruções
            inst_text = self.small_font.render('Use SETAS para selecionar e ENTER para confirmar', True, WHITE)
            screen.blit(inst_text, inst_text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT - 100)))
            
        elif self.state == 'scores':
            # Tela de high scores
            title = self.font.render('High Scores', True, WHITE)
            screen.blit(title, title.get_rect(center=(WINDOW_WIDTH/2, 100)))
            
            scores = self.db.get_top_scores(5)
            for i, (name, score) in enumerate(scores):
                score_text = self.small_font.render(f'{i+1}. {name}: {score}', True, WHITE)
                score_rect = score_text.get_rect(center=(WINDOW_WIDTH/2, 200 + i * 50))
                screen.blit(score_text, score_rect)
            
            if not scores:
                no_scores = self.small_font.render('Nenhuma pontuação registrada', True, WHITE)
                screen.blit(no_scores, no_scores.get_rect(center=(WINDOW_WIDTH/2, 250)))
            
            # Instrução para voltar
            back_text = self.small_font.render('Pressione ENTER para voltar', True, WHITE)
            screen.blit(back_text, back_text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT - 100)))
    
    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'
            
            if event.type == pygame.KEYDOWN:
                if self.state == 'main':
                    if event.key == pygame.K_UP:
                        self.selected_option = (self.selected_option - 1) % len(self.options)
                    elif event.key == pygame.K_DOWN:
                        self.selected_option = (self.selected_option + 1) % len(self.options)
                    elif event.key == pygame.K_RETURN:
                        if self.selected_option == 0:  # Escolher Nave
                            self.state = 'ships'
                        elif self.selected_option == 1:  # High Scores
                            self.state = 'scores'
                        elif self.selected_option == 2:  # Voltar
                            return 'menu'
                
                elif self.state == 'ships':
                    if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                        # Alterna entre as naves
                        self.ships[0]['selected'] = not self.ships[0]['selected']
                        self.ships[1]['selected'] = not self.ships[1]['selected']
                    elif event.key == pygame.K_RETURN:
                        self.state = 'main'
                
                elif self.state == 'scores':
                    if event.key == pygame.K_RETURN:
                        self.state = 'main'
        
        return None
    
    def get_selected_ship(self):
        for ship in self.ships:
            if ship['selected']:
                return 'player1.png' if ship['name'] == 'Nave 1' else 'player2.png' 