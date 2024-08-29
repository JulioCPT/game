import pygame
import sys
import math
import random
from model import HighscoreModel
from view import GameView

class MenuController:
    def __init__(self, view, model):
        self.view = view
        self.model = model

    def iniciar_menu(self):
        while True:
            opcoes = {
                "Novo Jogo": (485, 300),
                "Highscores": (480, 400),
                "Sair": (560, 500)
            }
            self.view.exibir_menu(opcoes)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if 300 <= y <= 370:  # Novo Jogo
                        return "novo_jogo"
                    elif 400 <= y <= 470:  # Highscores
                        return "highscores"
                    elif 500 <= y <= 570:  # Sair
                        pygame.quit()
                        sys.exit()

    def mostrar_highscores(self):
            highscores = self.model.get_highscores()
            while True:
                self.view.mostrar_highscores(highscores)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        # Voltar ao menu se o usuário clicar
                        return

class GameController:
    def __init__(self, view, model):
        self.view = view
        self.model = model
        self.todos_sprites = pygame.sprite.Group()
        self.sprites_inimigos = pygame.sprite.Group()
        self.player = Player(self.todos_sprites, self.sprites_inimigos)

    def iniciar_jogo(self):
        self.todos_sprites.add(self.player)
        tempo_inicio = pygame.time.get_ticks()
        relogio = pygame.time.Clock()
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            teclas = pygame.key.get_pressed()
            self.player.mover(teclas)

            colisoes = pygame.sprite.spritecollide(self.player, self.sprites_inimigos, True)
            for inimigo in colisoes:
                self.player.vida -= 10

            tempo_atual = pygame.time.get_ticks()
            if tempo_atual - self.player.tempo_criacao_inimigo > 1000:
                novo_inimigo = Enemy(self.player)
                self.todos_sprites.add(novo_inimigo)
                self.sprites_inimigos.add(novo_inimigo)
                self.player.tempo_criacao_inimigo = tempo_atual

            self.player.vida = max(0, min(self.player.vida, 100))
            tempo_decorrido = (tempo_atual - tempo_inicio) // 1000

            self.view.janela.fill(self.view.cores["preto"])
            for sprite in self.todos_sprites:
                sprite.update()
                self.view.janela.blit(sprite.image, sprite.rect)
            self.view.desenhar_barra_de_vida(self.player.vida)

            pygame.display.flip()
            relogio.tick(60)

            if self.player.vida == 0:
                running = False
                self.model.save_highscore(tempo_decorrido)
                self.view.desenhar_game_over(tempo_decorrido)

class Player(pygame.sprite.Sprite):
    def __init__(self, todos_sprites, sprites_inimigos):
        super().__init__()
        self.image = pygame.image.load("Alucard.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (80, 80))
        self.rect = self.image.get_rect()
        self.rect.center = (640, 360)
        self.velocidade_x = 0
        self.velocidade_y = 0
        self.vida = 100
        self.todos_sprites = todos_sprites
        self.sprites_inimigos = sprites_inimigos
        self.tempo_criacao_inimigo = pygame.time.get_ticks()

    def mover(self, teclas):
        if teclas[pygame.K_a]:
            self.velocidade_x = -4
        elif teclas[pygame.K_d]:
            self.velocidade_x = 4
        else:
            self.velocidade_x = 0

        if teclas[pygame.K_w]:
            self.velocidade_y = -4
        elif teclas[pygame.K_s]:
            self.velocidade_y = 4
        else:
            self.velocidade_y = 0

        self.rect.x += self.velocidade_x
        self.rect.y += self.velocidade_y

    def update(self):
        self.rect.x += self.velocidade_x
        self.rect.y += self.velocidade_y

class Enemy(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()
        self.image = pygame.image.load("padre.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (60, 60))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, 1280)
        self.rect.y = random.randint(0, 720)
        self.player = player

    def update(self):
        direcao_x = self.player.rect.centerx - self.rect.centerx
        direcao_y = self.player.rect.centery - self.rect.centery
        distancia = math.sqrt(direcao_x ** 2 + direcao_y ** 2)
        if distancia != 0:
            velocidade = 8
            self.rect.x += (direcao_x / distancia) * velocidade
            self.rect.y += (direcao_y / distancia) * velocidade
