import pygame
import random
import math
from pygame.sprite import *

# Inicializa o Pygame
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("TRILHA_FODA.mp3")
pygame.mixer.music.play()
pygame.mixer.music.set_volume(0.3)
fonte_timer = pygame.font.Font(None, 36)

# Cores
BRANCO = (255, 255, 255)
VERMELHO = (255, 0, 0)
VERDE = (0, 255, 0)
PRETO = (0, 0, 0)

# Tamanho da tela
largura_janela = 1280
altura_janela = 920
janela = pygame.display.set_mode((largura_janela, altura_janela), pygame.RESIZABLE)

# Classe do jogador
class player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load("Alucard.png")
        self.image = pygame.transform.scale(self.image, (80, 80))

        self.rect = self.image.get_rect()
        self.rect.center = (largura_janela // 2, altura_janela // 2)

        self.velocidade_x = 0
        self.velocidade_y = 0
        self.vida = 100

    def update(self):
        self.rect.x += self.velocidade_x
        self.rect.y += self.velocidade_y

class enemy(pygame.sprite.Sprite):
    def __init__(self, sprite_principal, todos_inimigos):
        super().__init__()

        self.image = pygame.image.load("padre.png")
        self.image = pygame.transform.scale(self.image, (60, 60))
        self.rect = self.image.get_rect()
        self.vida = 25

        self.sprite_principal = sprite_principal
        self.todos_inimigos = todos_inimigos

        distancia_spawn = 1800

        while True:
            spawn_x = random.randint(self.sprite_principal.rect.x - distancia_spawn, self.sprite_principal.rect.x + distancia_spawn)
            spawn_y = random.randint(self.sprite_principal.rect.y - distancia_spawn, self.sprite_principal.rect.y + distancia_spawn)

            colide_com_outro_inimigo = False
            for outro_inimigo in self.todos_inimigos:
                if pygame.sprite.collide_rect(self, outro_inimigo):
                    colide_com_outro_inimigo = True
                    break

            if not colide_com_outro_inimigo:
                self.rect.x = spawn_x
                self.rect.y = spawn_y
                break

    def update(self):
        direcao_x = self.sprite_principal.rect.centerx - self.rect.centerx
        direcao_y = self.sprite_principal.rect.centery - self.rect.centery
        distancia = math.sqrt(direcao_x ** 2 + direcao_y ** 2)

        if distancia != 0:
            velocidade = 8
            self.rect.x += (direcao_x / distancia) * velocidade
            self.rect.y += (direcao_y / distancia) * velocidade

            for outro_inimigo in self.todos_inimigos:
                if outro_inimigo != self and pygame.sprite.collide_rect(self, outro_inimigo):
                    direcao_x = outro_inimigo.rect.centerx - self.rect.centerx
                    direcao_y = outro_inimigo.rect.centery - self.rect.centery
                    distancia = math.sqrt(direcao_x ** 2 + direcao_y ** 2)

                    if distancia != 0:
                        self.rect.x -= (direcao_x / distancia) * velocidade
                        self.rect.y -= (direcao_y / distancia) * velocidade

def desenhar_barra_de_vida(surface, x, y, largura, altura, vida):
    if vida < 0:
        vida = 0
    largura_barra = int(largura * (vida / 100.0))
    cor = VERDE if vida > 50 else VERMELHO
    pygame.draw.rect(surface, cor, (x, y, largura_barra, altura))
    pygame.draw.rect(surface, BRANCO, (x, y, largura, altura), 2)

def tela_game_over(tempo_sobrevivido):
    tela_game_over = True
    fonte_game_over = pygame.font.Font(None, 72)
    
    while tela_game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        fundo_game_over = pygame.Surface((largura_janela, altura_janela))
        fundo_game_over.fill(PRETO)
        janela.blit(fundo_game_over, (0, 0))
        pygame.mixer.music.stop()

        mensagem_game_over = fonte_game_over.render("Game Over", True, BRANCO)
        retangulo_mensagem = mensagem_game_over.get_rect(center=(largura_janela // 2, altura_janela // 2 - 50))
        janela.blit(mensagem_game_over, retangulo_mensagem)

        mensagem_tempo = fonte_timer.render(f"Tempo sobrevivido: {tempo_sobrevivido}s", True, BRANCO)
        retangulo_tempo = mensagem_tempo.get_rect(center=(largura_janela // 2, altura_janela // 2 + 50))
        janela.blit(mensagem_tempo, retangulo_tempo)

        pygame.display.flip()

def iniciar_jogo():
    todos_sprites = pygame.sprite.Group()
    sprites_inimigos = pygame.sprite.Group()
    meu_sprite = player()
    todos_sprites.add(meu_sprite)

    tempo_inicio = pygame.time.get_ticks()

    posicao_timer = (largura_janela // 2, 12)
    tempo_criacao_inimigo = 0
    intervalo_criacao_inimigo = 1000

    personagem_direita = pygame.image.load("Alucard_direita.png").convert_alpha()
    personagem_esquerda = pygame.image.load("Alucard_esquerda.png").convert_alpha()

    relogio = pygame.time.Clock()

    running = True
    camera_x = 0
    camera_y = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        teclas = pygame.key.get_pressed()

        if teclas[pygame.K_a]:
            meu_sprite.velocidade_x = -4
            meu_sprite.image = personagem_esquerda
        elif teclas[pygame.K_d]:
            meu_sprite.velocidade_x = 4
            meu_sprite.image = personagem_direita
        else:
            meu_sprite.velocidade_x = 0

        if teclas[pygame.K_w]:
            meu_sprite.velocidade_y = -4
        elif teclas[pygame.K_s]:
            meu_sprite.velocidade_y = 4
        else:
            meu_sprite.velocidade_y = 0

        meu_sprite.rect.x += meu_sprite.velocidade_x
        meu_sprite.rect.y += meu_sprite.velocidade_y

        colisoes = pygame.sprite.spritecollide(meu_sprite, sprites_inimigos, True)

        for inimigo in colisoes:
            meu_sprite.vida -= 10

        meu_sprite.vida = max(0, min(meu_sprite.vida, 100))

        tempo_atual = pygame.time.get_ticks()
        if tempo_atual - tempo_criacao_inimigo > intervalo_criacao_inimigo:
            novo_inimigo = enemy(meu_sprite, sprites_inimigos)
            todos_sprites.add(novo_inimigo)
            sprites_inimigos.add(novo_inimigo)
            tempo_criacao_inimigo = tempo_atual

        tempo_decorrido_milissegundos = tempo_atual - tempo_inicio

        segundos = (tempo_decorrido_milissegundos // 1000) % 60
        minutos = (tempo_decorrido_milissegundos // 1000) // 60

        fundo = pygame.image.load("Floor.png").convert()
        fundo = pygame.transform.scale(fundo, (1280, 920))
        janela.blit(fundo, (0, 0))

        texto_timer = fonte_timer.render(f"Tempo sobrevivido: {minutos}m {segundos}s", True, BRANCO)
        retangulo_timer = texto_timer.get_rect(center=posicao_timer)
        janela.blit(texto_timer, retangulo_timer)

        if meu_sprite.rect.left < camera_x:
            camera_x = meu_sprite.rect.left
        elif meu_sprite.rect.right > camera_x + largura_janela:
            camera_x = meu_sprite.rect.right - largura_janela

        if meu_sprite.rect.top < camera_y:
            camera_y = meu_sprite.rect.top
        elif meu_sprite.rect.bottom > camera_y + altura_janela:
            camera_y = meu_sprite.rect.bottom - altura_janela

        for sprite in todos_sprites:
            sprite.update()
            janela.blit(sprite.image, (sprite.rect.x - camera_x, sprite.rect.y - camera_y))

        desenhar_barra_de_vida(janela, 10, 10, 200, 20, meu_sprite.vida)

        pygame.display.flip()
        relogio.tick(60)

        if meu_sprite.vida == 0:
            running = False
            tempo_fim = pygame.time.get_ticks()
            tempo_sobrevivido = (tempo_fim - tempo_inicio) // 1000
            tela_game_over(tempo_sobrevivido)
