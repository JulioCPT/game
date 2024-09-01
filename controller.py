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
                "Novo Jogo": (825, 300),
                "Highscores": (820, 400),
                "Créditos": (845, 500),
                "Sair": (900, 600)
            }
            self.view.exibir_menu(opcoes)  # Verifique se esta linha está correta

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
                    elif 500 <= y <= 570:  # Créditos
                        return "creditos"  # Corrigir aqui para retornar "creditos"
                    elif 600 <= y <= 670:  # Sair
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
                        return
                    
    def mostrar_creditos(self):
        while True:
            self.view.janela.fill(self.view.cores["preto"])
            self.view.desenhar_texto("Créditos", (820, 300))
            self.view.desenhar_texto("Júlio César Pinheiro Teixeira", (640, 400))
            self.view.desenhar_texto("Eric Domingues de Souza", (640, 450))
            self.view.desenhar_texto("Julio Cesar Cester", (640, 500))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    return
class GameController:
    def __init__(self, view, model):
        self.view = view
        self.model = model
        self.todos_sprites = pygame.sprite.Group()
        self.sprites_inimigos = pygame.sprite.Group()
        self.player = Player(self.todos_sprites, self.sprites_inimigos, self.view.largura, self.view.altura)

    
    def obter_nome_do_jogador(self):
        nome_jogador = ""
        fonte = pygame.font.Font(None, 74)
        relogio = pygame.time.Clock()
        
        entrada_ativa = True
        while entrada_ativa:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:  # Pressiona Enter para confirmar o nome
                        entrada_ativa = False
                    elif event.key == pygame.K_BACKSPACE:  # Backspace para apagar o último caractere
                        nome_jogador = nome_jogador[:-1]
                    else:
                        nome_jogador += event.unicode  # Adiciona o caractere digitado ao nome

            # Desenhar a tela de entrada
            self.view.janela.fill(self.view.cores["preto"])
            texto = fonte.render("Digite seu nome:", True, self.view.cores["branco"])
            self.view.janela.blit(texto, (980 - texto.get_width() // 2, 300))
            
            texto_nome = fonte.render(nome_jogador, True, self.view.cores["branco"])
            self.view.janela.blit(texto_nome, (970 - texto_nome.get_width() // 2, 400))
            
            pygame.display.flip()
            relogio.tick(30)

        return nome_jogador
    

    def iniciar_jogo(self):
        pygame.mixer.music.play(-1)  
        self.todos_sprites.empty()  # Limpa todos os sprites da última sessão
        self.sprites_inimigos.empty()  # Limpa todos os inimigos da última sessão
        self.player = Player(self.todos_sprites, self.sprites_inimigos, self.view.largura, self.view.altura)  # Cria um novo player
        self.todos_sprites.add(self.player)
        tempo_inicio = pygame.time.get_ticks()
        relogio = pygame.time.Clock()
        running = True
        nome_jogador = self.obter_nome_do_jogador()

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.VIDEORESIZE:
                    self.view.largura, self.view.altura = event.size
                    self.player.update_screen_dimensions(self.view.largura, self.view.altura)  # Atualiza os limites do jogador

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

            self.view.desenhar_fundo()
            for sprite in self.todos_sprites:
                sprite.update()
                self.view.janela.blit(sprite.image, sprite.rect)
            self.view.desenhar_barra_de_vida(self.player.vida)

            pygame.display.flip()
            relogio.tick(60)

            if self.player.vida == 0:
                running = False
                self.model.save_highscore(nome_jogador, tempo_decorrido)
                self.view.desenhar_game_over(tempo_decorrido)
                pygame.mixer.music.stop()
                pygame.display.flip()

                game_over_time = pygame.time.get_ticks()
                while pygame.time.get_ticks() - game_over_time < 3000:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()

        self.todos_sprites.empty()
        self.sprites_inimigos.empty()
                


class Player(pygame.sprite.Sprite):
    def __init__(self, todos_sprites, sprites_inimigos, screen_width, screen_height):
        super().__init__()
        self.image = pygame.image.load("Alucard.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (80, 80))
        self.rect = self.image.get_rect()
        self.rect.center = (955, 485)
        self.velocidade_x = 0
        self.velocidade_y = 0
        self.vida = 100
        self.todos_sprites = todos_sprites
        self.sprites_inimigos = sprites_inimigos
        self.tempo_criacao_inimigo = pygame.time.get_ticks()
        self.screen_width = screen_width
        self.screen_height = screen_height

    def update_screen_dimensions(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        # Garantir que o jogador permaneça dentro dos novos limites
        self.rect.x = max(0, min(self.rect.x, self.screen_width - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, self.screen_height - self.rect.height))

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

        # Restringir o jogador dentro dos limites da tela
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > self.screen_width:
            self.rect.right = self.screen_width
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > self.screen_height:
            self.rect.bottom = self.screen_height

    def update(self):
        self.rect.x += self.velocidade_x
        self.rect.y += self.velocidade_y

        # Restringir o jogador dentro dos limites da tela
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > self.screen_width:
            self.rect.right = self.screen_width
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > self.screen_height:
            self.rect.bottom = self.screen_height

class Enemy(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()
        self.player = player  # Defina self.player primeiro

        self.image = pygame.image.load("padre.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (60, 60))
        self.rect = self.image.get_rect()

        # Tamanho da tela
        screen_width = 1280
        screen_height = 720

        # Posição do jogador
        player_x, player_y = self.player.rect.center

        # Definir distância mínima
        distancia_minima = 200

        # Determinar área segura ao redor do jogador
        safe_zone = pygame.Rect(
            max(0, player_x - distancia_minima),
            max(0, player_y - distancia_minima),
            min(screen_width, player_x + distancia_minima) - max(0, player_x - distancia_minima),
            min(screen_height, player_y + distancia_minima) - max(0, player_y - distancia_minima)
        )

        # Gerar posição fora da zona segura
        while True:
            self.rect.x = random.randint(0, screen_width)
            self.rect.y = random.randint(0, screen_height)

            # Verificar se o inimigo está fora da zona segura
            if not safe_zone.collidepoint(self.rect.center):
                break

    def update(self):
        direcao_x = self.player.rect.centerx - self.rect.centerx
        direcao_y = self.player.rect.centery - self.rect.centery
        distancia = math.sqrt(direcao_x ** 2 + direcao_y ** 2)
        if distancia != 0:
            velocidade = 8
            self.rect.x += (direcao_x / distancia) * velocidade
            self.rect.y += (direcao_y / distancia) * velocidade