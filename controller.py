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
                    
            
class Camera:
    def __init__(self, largura, altura):
        self.camera = pygame.Rect(0, 0, largura, altura)
        self.largura = largura
        self.altura = altura

    def aplicar(self, rect):
        return rect.move(self.camera.topleft)

    def centralizar(self, target):
        x = -target.rect.centerx + int(self.largura / 2)
        y = -target.rect.centery + int(self.altura / 2)

        # Limitar a câmera para que ela não mostre áreas fora dos limites do mapa
        x = max(-(self.largura - 1280), min(0, x))
        y = max(-(self.altura - 920), min(0, y))

        self.camera = pygame.Rect(x, y, self.largura, self.altura)





class GameController:
    def __init__(self, view, model):
        self.view = view
        self.model = model
        self.todos_sprites = pygame.sprite.Group()
        self.sprites_inimigos = pygame.sprite.Group()
        self.player = Player(self.todos_sprites, self.sprites_inimigos)
        self.camera = Camera(1280 * 2, 920 * 2)

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
            self.view.janela.blit(texto, (640 - texto.get_width() // 2, 300))
            
            texto_nome = fonte.render(nome_jogador, True, self.view.cores["branco"])
            self.view.janela.blit(texto_nome, (640 - texto_nome.get_width() // 2, 400))
            
            pygame.display.flip()
            relogio.tick(30)
        
        return nome_jogador

    def iniciar_jogo(self):
        self.todos_sprites.empty()  # Limpa todos os sprites da última sessão
        self.sprites_inimigos.empty()  # Limpa todos os inimigos da última sessão
        self.player = Player(self.todos_sprites, self.sprites_inimigos)  # Cria um novo player
        self.todos_sprites.add(self.player)
        fundo = pygame.image.load("C:/Users/Aluno/Desktop/Flavio/game-teste2/Floor.png").convert()
        fundo = pygame.transform.scale(fundo, (1280 * 4, 720 * 4))
        tempo_inicio = pygame.time.get_ticks()
        relogio = pygame.time.Clock()
        running = True
        nome_jogador = self.obter_nome_do_jogador()  # Obter o nome do jogador

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            teclas = pygame.key.get_pressed()
            self.player.mover(teclas)
            self.camera.centralizar(self.player)

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

            # Desenhar fundo ajustado pela câmera
            self.view.janela.blit(fundo, self.camera.aplicar(fundo.get_rect()))

            # Desenhar sprites
            for sprite in self.todos_sprites:
                sprite.draw(self.view.janela, self.camera)

            self.view.desenhar_barra_de_vida(self.player.vida)

            pygame.display.flip()
            relogio.tick(60)

            if self.player.vida == 0:
                running = False
                self.model.save_highscore(nome_jogador, tempo_decorrido)
                self.view.desenhar_game_over(tempo_decorrido)


class Player(pygame.sprite.Sprite):
    def __init__(self, todos_sprites, sprites_inimigos):
        super().__init__()
        self.image = pygame.image.load("C:/Users/Aluno/Desktop/Flavio/game-teste2/Alucard.png").convert_alpha()
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

        # Atualiza a posição do jogador
        self.rect.x += self.velocidade_x
        self.rect.y += self.velocidade_y

        # Limita a posição do jogador dentro dos limites do mapa
        self.rect.x = max(0, min(self.rect.x, 1280 * 4 - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, 720 * 4 - self.rect.height))

    def draw(self, surface, camera):
        # Desenhar o jogador na posição correta com base na câmera
        center_x = surface.get_width() // 2
        center_y = surface.get_height() // 2
        draw_rect = pygame.Rect(center_x - self.rect.width // 2, center_y - self.rect.height // 2, self.rect.width, self.rect.height)
        surface.blit(self.image, draw_rect)

    def update(self):
        self.rect.x += self.velocidade_x
        self.rect.y += self.velocidade_y





class Enemy(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()
        self.image = pygame.image.load("C:/Users/Aluno/Desktop/Flavio/game-teste2/padre.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (60, 60))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, 1280 * 4)  # Ajuste conforme o tamanho do mapa
        self.rect.y = random.randint(0, 720 * 4)   # Ajuste conforme o tamanho do mapa
        self.player = player

    def update(self):
        direcao_x = self.player.rect.centerx - self.rect.centerx
        direcao_y = self.player.rect.centery - self.rect.centery
        distancia = math.sqrt(direcao_x ** 2 + direcao_y ** 2)
        if distancia != 0:
            velocidade = 4  # Ajuste a velocidade conforme necessário
            self.rect.x += (direcao_x / distancia) * velocidade
            self.rect.y += (direcao_y / distancia) * velocidade

    def draw(self, surface, camera):
        # Desenhar o inimigo na tela, ajustando a posição com base na câmera
        surface.blit(self.image, camera.aplicar(self.rect))