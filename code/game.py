import pygame
import os
import random
from .settings import *
from .player import Player
from .menu import Menu
from .game_over import GameOver
from .asteroid import Asteroid
from .enemy import Enemy
from .powerup import PowerUp
from .boss import Boss
from .options import Options

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Meu Jogo 2D")
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = 'menu'
        
        # Carrega o background
        background_path = os.path.join('assets', 'images', 'background.png')  # ou .jpg ou .gif
        self.background = pygame.image.load(background_path)
        self.background = pygame.transform.scale(self.background, (WINDOW_WIDTH, WINDOW_HEIGHT))
        
        # Sprites
        self.all_sprites = pygame.sprite.Group()
        self.asteroids = pygame.sprite.Group()
        self.player = Player()
        
        self.all_sprites.add(self.player)
        
        # Cria asteroides
        asteroid_images = ['asteroid.png', 'asteroid2.png', 'Meteor_01.png', 'Meteor02.png', 'satelite.png']
        for _ in range(6):  # Cria 6 asteroides (ajuste conforme necessário)
            asteroid = Asteroid(random.choice(asteroid_images))
            self.all_sprites.add(asteroid)
            self.asteroids.add(asteroid)
        
        # Menu
        self.menu = Menu()
        
        # Adicione após as outras inicializações:
        self.score = 0
        self.game_over_screen = None
        self.bullets = pygame.sprite.Group()  # Novo grupo para os projéteis
        self.enemies = pygame.sprite.Group()
        self.enemy_bullets = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.missiles = pygame.sprite.Group()
        self.last_powerup_spawn = pygame.time.get_ticks()
        self.powerup_spawn_delay = 10000  # 10 segundos entre power-ups
        self.boss = None
        self.boss_bullets = pygame.sprite.Group()
        self.boss_score_threshold = 1000  # Pontuação necessária para o boss aparecer
        self.boss_mode = False
        self.boss_spawn_timer = 0
        self.boss_waiting = True
        
        # Carrega o background do boss
        self.boss_background = pygame.image.load(os.path.join('assets', 'images', 'backgroundBoss.png'))
        self.boss_background = pygame.transform.scale(self.boss_background, (WINDOW_WIDTH, WINDOW_HEIGHT))
        
        # Cria inimigos iniciais
        self.spawn_enemies()
        
        self.options = Options()
        self.selected_ship = 'player1.png'  # Nave padrão
        
        # Inicializa o mixer do pygame
        pygame.mixer.init()
        
        # Carrega as músicas
        self.menu_music = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'menu_music.mp3'))
        self.game_music = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'game_music.mp3'))
        self.boss_music = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'boss_music.mp3'))
        
        # Ajusta o volume (0.0 a 1.0)
        self.menu_music.set_volume(0.5)
        self.game_music.set_volume(0.5)
        self.boss_music.set_volume(0.5)
        
        # Controle de música atual
        self.current_music = None
        
    def spawn_enemies(self):
        # Garante um de cada tipo
        for enemy_type in [1, 2, 3]:
            enemy = Enemy(enemy_type)
            self.enemies.add(enemy)
            self.all_sprites.add(enemy)
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
    def update(self):
        if self.state == 'playing':
            # Atualiza todos os sprites
            self.all_sprites.update()
            self.bullets.update()
            self.enemy_bullets.update()
            
            # Tiro do jogador
            if self.player.is_shooting:
                bullet = self.player.shoot()
                self.bullets.add(bullet)
                self.all_sprites.add(bullet)
            
            # Disparo de mísseis
            keys = pygame.key.get_pressed()
            current_time = pygame.time.get_ticks()
            if keys[pygame.K_m] and current_time - self.player.shoot_timer > self.player.shoot_delay:
                missile = self.player.shoot_missile()
                if missile:
                    self.missiles.add(missile)
                    self.all_sprites.add(missile)
                    self.player.shoot_timer = current_time

            # Colisão de tiros normais com asteroides (movido para fora do else)
            hits = pygame.sprite.groupcollide(self.asteroids, self.bullets, True, True)
            for asteroid in hits:
                self.score += 50  # 50 pontos por asteroide destruído
                
            # Colisão de mísseis com asteroides (movido para fora do else)
            hits = pygame.sprite.groupcollide(self.asteroids, self.missiles, True, True)
            for asteroid in hits:
                self.score += 100  # 100 pontos por asteroide destruído com míssil
                
            # Reposiciona novos asteroides quando alguns são destruídos (movido para fora do else)
            while len(self.asteroids) < 6:
                asteroid_images = ['asteroid.png', 'asteroid2.png', 'Meteor_01.png', 'Meteor02.png', 'satelite.png']
                asteroid = Asteroid(random.choice(asteroid_images))
                self.all_sprites.add(asteroid)
                self.asteroids.add(asteroid)

            # Colisão do jogador com asteroides (movido para fora do else)
            hits = pygame.sprite.spritecollide(self.player, self.asteroids, False, pygame.sprite.collide_mask)
            if hits:
                self.player.take_damage(10)
                if self.player.health <= 0:
                    self.game_over_screen = GameOver(self.score, victory=False)
                    self.state = 'game_over'

            # Verifica se deve iniciar o modo boss
            if not self.boss_mode and self.score >= self.boss_score_threshold:
                self.start_boss_mode()
            
            if self.boss_mode:
                current_time = pygame.time.get_ticks()
                
                if self.boss_waiting:
                    if current_time - self.boss_spawn_timer > 5000:
                        self.boss = Boss()
                        self.all_sprites.add(self.boss)
                        self.boss_waiting = False
                elif self.boss:
                    self.boss_bullets.update()
                    
                    # Tiros do boss
                    bullet = self.boss.shoot()
                    if bullet:
                        self.boss_bullets.add(bullet)
                        self.all_sprites.add(bullet)
                    
                    # Colisão de tiros normais com boss
                    hits = pygame.sprite.spritecollide(self.boss, self.bullets, True)
                    for bullet in hits:
                        if self.boss.take_damage(10):  # 10 de dano por tiro normal
                            self.victory()
                    
                    # Colisão de mísseis com boss
                    hits = pygame.sprite.spritecollide(self.boss, self.missiles, True)
                    for missile in hits:
                        if self.boss.take_damage(50):  # 50 de dano por míssil
                            self.victory()
                    
                    # Colisão de tiros do boss com jogador
                    hits = pygame.sprite.spritecollide(self.player, self.boss_bullets, True)
                    if hits:
                        self.player.take_damage(20)
                        if self.player.health <= 0:
                            self.game_over_screen = GameOver(self.score, victory=False)
                            self.state = 'game_over'
            else:
                # Código normal do jogo (inimigos, etc.)
                # Tiros dos inimigos
                for enemy in self.enemies:
                    if random.random() < 0.01:  # 1% de chance de atirar a cada frame
                        bullet = enemy.shoot()
                        self.enemy_bullets.add(bullet)
                        self.all_sprites.add(bullet)
                
                # Colisão de tiros do jogador com inimigos
                hits = pygame.sprite.groupcollide(self.enemies, self.bullets, False, True)
                for enemy, bullets in hits.items():
                    for bullet in bullets:
                        if enemy.take_damage(34):  # 3 tiros para destruir
                            enemy.kill()
                            if enemy.enemy_type == 1:
                                self.score += 100  # Inimigo tipo 1
                            elif enemy.enemy_type == 2:
                                self.score += 150  # Inimigo tipo 2
                            else:
                                self.score += 200  # Inimigo tipo 3
                
                # Colisão de tiros inimigos com jogador (versão simplificada)
                hits = pygame.sprite.spritecollide(self.player, self.enemy_bullets, True)
                for bullet in hits:
                    for enemy in self.enemies:
                        if enemy.enemy_type == bullet.enemy_type:  # Usa o tipo do inimigo para determinar o dano
                            self.player.take_damage(enemy.get_damage())
                            break
                
                if self.player.health <= 0:
                    self.game_over_screen = GameOver(self.score, victory=False)
                    self.state = 'game_over'
                
                # Respawn de inimigos
                if len(self.enemies) < 3:
                    self.spawn_enemies()
                
                # Spawn de power-ups (movido para dentro do else)
                now = pygame.time.get_ticks()
                if now - self.last_powerup_spawn > self.powerup_spawn_delay:
                    if len(self.powerups) < 1:
                        powerup = PowerUp()
                        self.powerups.add(powerup)
                        self.all_sprites.add(powerup)
                        self.last_powerup_spawn = now

                # Atualiza power-ups
                self.powerups.update()
                self.missiles.update()

                # Coleta de power-ups
                hits = pygame.sprite.spritecollide(self.player, self.powerups, True)
                if hits:
                    self.player.collect_powerup()

                # Colisão de mísseis com inimigos
                hits = pygame.sprite.groupcollide(self.enemies, self.missiles, True, True)
                for enemy in hits:
                    if enemy.enemy_type == 1:
                        self.score += 200  # Dobro de pontos usando míssil
                    elif enemy.enemy_type == 2:
                        self.score += 300
                    else:
                        self.score += 400

        elif self.state == 'menu':
            action = self.menu.handle_input()
            if action == 'play':
                self.state = 'playing'
                self.score = 0  # Reseta o score ao começar
            elif action == 'quit':
                self.running = False
        elif self.state == 'game_over':
            action = self.game_over_screen.handle_input()
            if action == 'menu':
                self.state = 'menu'
            elif action == 'quit':
                self.running = False
        pygame.display.flip()
        
    def run(self):
        # Começa com a música do menu
        self.play_music(self.menu_music)
        
        while self.running:
            if self.state == 'menu':
                if self.current_music != self.menu_music:
                    self.play_music(self.menu_music)
                action = self.menu.handle_input()
                if action == 'play':
                    self.reset_game()
                elif action == 'options':
                    self.state = 'options'
                elif action == 'quit':
                    self.running = False
            elif self.state == 'options':
                action = self.options.handle_input()
                if action == 'menu':
                    self.selected_ship = self.options.get_selected_ship()
                    self.state = 'menu'
                elif action == 'quit':
                    self.running = False
            elif self.state == 'playing':
                if not self.boss_mode and self.current_music != self.game_music:
                    self.play_music(self.game_music)
                self.handle_events()
                self.update()
            elif self.state == 'game_over':
                action = self.game_over_screen.handle_input()
                if action == 'menu':
                    self.state = 'menu'
                elif action == 'quit':
                    self.running = False
            
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
    
    def check_game_over_condition(self):
        # Implemente sua lógica de game over aqui
        # Por exemplo: colisão com inimigo, fim da demo, etc.
        return False
    
    def start_boss_mode(self):
        self.boss_mode = True
        
        # Remove todos os inimigos e seus tiros
        for enemy in self.enemies:
            enemy.kill()
        for bullet in self.enemy_bullets:
            bullet.kill()
        
        # Remove todos os power-ups da tela
        for powerup in self.powerups:
            powerup.kill()
        
        # Muda o background e inicia o timer para o boss aparecer
        self.boss_spawn_timer = pygame.time.get_ticks()
        self.boss_waiting = True  # Nova flag para controlar a entrada do boss
        self.boss = None
        
        self.play_music(self.boss_music)
    
    def victory(self):
        self.game_over_screen = GameOver(self.score, victory=True)
        self.state = 'game_over'
        
    def draw(self):
        if self.state == 'menu':
            self.menu.draw(self.screen)
        elif self.state == 'options':
            self.options.draw(self.screen)
        elif self.state == 'playing':
            # Escolhe o background apropriado
            if self.boss_mode:
                self.screen.blit(self.boss_background, (0, 0))
            else:
                self.screen.blit(self.background, (0, 0))
            
            self.all_sprites.draw(self.screen)
            
            # Desenha barra de vida do jogador (mantém à esquerda)
            health_width = 200 * (self.player.health / 100)
            pygame.draw.rect(self.screen, RED, (10, 40, 200, 20))
            pygame.draw.rect(self.screen, GREEN, (10, 40, health_width, 20))
            
            # Desenha barra de vida do Boss (alinhada à direita)
            if self.boss_mode and self.boss and not self.boss_waiting:
                boss_health_width = 300 * (self.boss.health / self.boss.max_health)
                boss_bar_x = WINDOW_WIDTH - 310  # 10 pixels de margem da direita
                pygame.draw.rect(self.screen, RED, (boss_bar_x, 40, 300, 20))
                pygame.draw.rect(self.screen, BLUE, (boss_bar_x, 40, boss_health_width, 20))
            
            score_text = pygame.font.Font(None, 36).render(f'Score: {self.score}', True, WHITE)
            self.screen.blit(score_text, (10, 10))
            
            # Desenha contador de mísseis
            missile_text = pygame.font.Font(None, 36).render(f'Mísseis: {self.player.missiles}', True, WHITE)
            self.screen.blit(missile_text, (10, 70))
        elif self.state == 'game_over':
            self.game_over_screen.draw(self.screen)
        pygame.display.flip()
        
    def reset_game(self):
        # Reset score e estado
        self.score = 0
        self.state = 'playing'
        
        # Reset player
        self.player.health = 100
        self.player.missiles = 0
        self.player.rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        
        # Limpa todos os sprites
        for sprite in self.all_sprites:
            if sprite != self.player:
                sprite.kill()
        
        self.bullets.empty()
        self.enemy_bullets.empty()
        self.enemies.empty()
        self.powerups.empty()
        self.missiles.empty()
        self.boss_bullets.empty()
        
        # Reset boss mode
        self.boss_mode = False
        self.boss = None
        self.boss_waiting = True
        
        # Recria asteroides
        asteroid_images = ['asteroid.png', 'asteroid2.png', 'Meteor_01.png', 'Meteor02.png', 'satelite.png']
        for _ in range(6):
            asteroid = Asteroid(random.choice(asteroid_images))
            self.all_sprites.add(asteroid)
            self.asteroids.add(asteroid)
        
        # Recria inimigos
        self.spawn_enemies()
        
        # Atualiza a nave do jogador
        self.player.update_ship(self.selected_ship)
        
    def play_music(self, music):
        # Para a música atual se houver
        if self.current_music:
            self.current_music.stop()
        
        # Toca a nova música
        music.play(-1)  # -1 significa loop infinito
        self.current_music = music
        