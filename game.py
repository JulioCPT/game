import pygame
import random
import math
import pygame.mixer
from pygame.sprite import *

# Inicia o pygame
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

        self.velocidade_x = 0  # Velocidade horizontal
        self.velocidade_y = 0  # Velocidade vertical
        self.vida = 100  # Vida do sprite principal

    def update(self):
        # Atualize a posição horizontal do sprite principal
        self.rect.x += self.velocidade_x

        # Atualize a posição vertical do sprite principal
        self.rect.y += self.velocidade_y

class enemy(pygame.sprite.Sprite):
    def __init__(self, sprite_principal, todos_inimigos):
        super().__init__()

        self.image = pygame.image.load("padre.png")
        self.image = pygame.transform.scale(self.image, (60, 60))
        self.rect = self.image.get_rect()
        self.vida = 25

        # Guarde uma referência ao sprite principal e à lista de todos os inimigos
        self.sprite_principal = sprite_principal
        self.todos_inimigos = todos_inimigos

        # Defina a distância de spawn em relação ao sprite principal
        distancia_spawn = 1800  # Ajuste essa distância conforme necessário

        # Calcule a posição inicial com base na posição do sprite principal
        while True:
            # Gere posições iniciais aleatórias dentro da distância de spawn
            spawn_x = random.randint(self.sprite_principal.rect.x - distancia_spawn, self.sprite_principal.rect.x + distancia_spawn)
            spawn_y = random.randint(self.sprite_principal.rect.y - distancia_spawn, self.sprite_principal.rect.y + distancia_spawn)

            # Verifique se a posição gerada não colide com outros inimigos
            colide_com_outro_inimigo = False
            for outro_inimigo in self.todos_inimigos:
                if pygame.sprite.collide_rect(self, outro_inimigo):
                    colide_com_outro_inimigo = True
                    break

            # Se a posição não colidir com outros inimigos, defina-a como a posição inicial
            if not colide_com_outro_inimigo:
                self.rect.x = spawn_x
                self.rect.y = spawn_y
                break

    def update(self):
        # Movimento em direção ao sprite principal
        direcao_x = self.sprite_principal.rect.centerx - self.rect.centerx
        direcao_y = self.sprite_principal.rect.centery - self.rect.centery
        distancia = math.sqrt(direcao_x ** 2 + direcao_y ** 2)

        if distancia != 0:
            velocidade = 8  # Velocidade de movimento do inimigo
            self.rect.x += (direcao_x / distancia) * velocidade  # Velocidade horizontal
            self.rect.y += (direcao_y / distancia) * velocidade  # Velocidade Vertical

            # Verifique colisões com outros inimigos e ajuste a posição se houver uma colisão
            for outro_inimigo in self.todos_inimigos:
                if outro_inimigo != self and pygame.sprite.collide_rect(self, outro_inimigo):
                    direcao_x = outro_inimigo.rect.centerx - self.rect.centerx
                    direcao_y = outro_inimigo.rect.centery - self.rect.centery
                    distancia = math.sqrt(direcao_x ** 2 + direcao_y ** 2)

                    if distancia != 0:
                        # Mova-se na direção oposta
                        self.rect.x -= (direcao_x / distancia) * velocidade
                        self.rect.y -= (direcao_y / distancia) * velocidade

# Função da barra de vida
def desenhar_barra_de_vida(surface, x, y, largura, altura, vida):
    if vida < 0:
        vida = 0
    largura_barra = int(largura * (vida / 100.0))
    cor = VERDE if vida > 50 else VERMELHO if vida > 20 else VERMELHO
    pygame.draw.rect(surface, cor, (x, y, largura_barra, altura))
    pygame.draw.rect(surface, BRANCO, (x, y, largura, altura), 2)

# Função para mostrar a tela de "Game Over"
def tela_game_over(tempo_sobrevivido):
    tela_game_over = True
    fonte_game_over = pygame.font.Font(None, 72)
    
    while tela_game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # Define o fundo da tela de "Game Over"
        fundo_game_over = pygame.Surface((largura_janela, altura_janela))
        fundo_game_over.fill(PRETO)
        janela.blit(fundo_game_over, (0, 0))
        pygame.mixer.music.stop()

        # Exibe a mensagem de "Game Over" e o tempo sobrevivido
        mensagem_game_over = fonte_game_over.render("Game Over", True, BRANCO)
        retangulo_mensagem = mensagem_game_over.get_rect(center=(largura_janela // 2, altura_janela // 2 - 50))
        janela.blit(mensagem_game_over, retangulo_mensagem)

        mensagem_tempo = fonte_timer.render(f"Tempo sobrevivido: {tempo_sobrevivido}s", True, BRANCO)
        retangulo_tempo = mensagem_tempo.get_rect(center=(largura_janela // 2, altura_janela // 2 + 50))
        janela.blit(mensagem_tempo, retangulo_tempo)

        pygame.display.flip()

todos_sprites = pygame.sprite.Group()
sprites_inimigos = pygame.sprite.Group()
meu_sprite = player()
todos_sprites.add(meu_sprite)

# Inicializa uma variável de tempo no início do jogo
tempo_inicio = pygame.time.get_ticks()

# Posição do timer na tela
posicao_timer = (largura_janela // 2, 12)


# Tempo para controlar a criação de inimigos
tempo_criacao_inimigo = 0
intervalo_criacao_inimigo = 1000  # Crie um inimigo a cada 2 segundos (em milissegundos)

personagem_direita = pygame.image.load("Alucard_direita.png").convert_alpha()
personagem_esquerda = pygame.image.load("Alucard_esquerda.png").convert_alpha()

relogio = pygame.time.Clock()

running = True

# Posição inicial da câmera
camera_x = 0
camera_y = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    teclas = pygame.key.get_pressed()

    # Atualiza a posição do sprite com base nas teclas pressionadas
    if teclas[pygame.K_a]:
        meu_sprite.velocidade_x = - 4 # Move para a esquerda
        meu_sprite.image = personagem_esquerda
    elif teclas[pygame.K_d]:
        meu_sprite.velocidade_x = 4  # Move para a direita
        meu_sprite.image = personagem_direita
    else:
        meu_sprite.velocidade_x = 0

    if teclas[pygame.K_w]:
        meu_sprite.velocidade_y = - 4  # Move para cima
    elif teclas[pygame.K_s]:
        meu_sprite.velocidade_y = 4  # Move para baixo
    else:
        meu_sprite.velocidade_y = 0

    # Atualiza a posição do sprite
    meu_sprite.rect.x += meu_sprite.velocidade_x
    meu_sprite.rect.y += meu_sprite.velocidade_y

    # Verifique colisões entre o sprite principal e os inimigos
    colisoes = pygame.sprite.spritecollide(meu_sprite, sprites_inimigos, True)

    # Reduza a vida do sprite principal se houver colisões
    for inimigo in colisoes:
        meu_sprite.vida -= 10  # Reduza a vida do sprite principal em 10 pontos

    # Limite a vida do sprite principal entre 0 e 100
    meu_sprite.vida = max(0, min(meu_sprite.vida, 100))

    # Verifique se é hora de criar um novo inimigo
    tempo_atual = pygame.time.get_ticks()
    if tempo_atual - tempo_criacao_inimigo > intervalo_criacao_inimigo:
        novo_inimigo = enemy(meu_sprite, sprites_inimigos)
        todos_sprites.add(novo_inimigo)
        sprites_inimigos.add(novo_inimigo)
        tempo_criacao_inimigo = tempo_atual

    # Atualize o tempo decorrido desde o início do jogo
    tempo_atual = pygame.time.get_ticks()
    tempo_decorrido_milissegundos = tempo_atual - tempo_inicio  # Tempo decorrido em milissegundos

    # Converte o tempo decorrido para minutos e segundos
    segundos = (tempo_decorrido_milissegundos // 1000) % 60
    minutos = (tempo_decorrido_milissegundos // 1000) // 60

    # Define o fundo
    fundo = pygame.image.load("Floor.png").convert()
    fundo = pygame.transform.scale(fundo, (1280, 920))
    janela.blit(fundo, (0, 0))

    # Desenhe o timer no topo central da tela
    texto_timer = fonte_timer.render(f"Tempo sobrevivido: {minutos}m {segundos}s", True, BRANCO)
    retangulo_timer = texto_timer.get_rect(center=posicao_timer)
    janela.blit(texto_timer, retangulo_timer)

    # Verifique se o sprite saiu dos limites da tela
    if meu_sprite.rect.left < camera_x:
        camera_x = meu_sprite.rect.left
    elif meu_sprite.rect.right > camera_x + largura_janela:
        camera_x = meu_sprite.rect.right - largura_janela

    if meu_sprite.rect.top < camera_y:
        camera_y = meu_sprite.rect.top
    elif meu_sprite.rect.bottom > camera_y + altura_janela:
        camera_y = meu_sprite.rect.bottom - altura_janela

    # Desenhe todos os sprites na tela, ajustando a posição com base na câmera
    for sprite in todos_sprites:
        sprite.update()  # Atualize a posição do inimigo em direção ao sprite principal
        janela.blit(sprite.image, (sprite.rect.x - camera_x, sprite.rect.y - camera_y))

    # Desenhe a barra de vida
    desenhar_barra_de_vida(janela, 10, 10, 200, 20, meu_sprite.vida)

    # Atualize a tela
    pygame.display.flip()
    relogio.tick(60)

    # Tela de game over
    if meu_sprite.vida == 0:
        running = False
        tempo_fim = pygame.time.get_ticks()
        tempo_sobrevivido = (tempo_fim - tempo_inicio) // 1000  # Calcula o tempo sobrevivido em segundos
        tela_game_over(tempo_sobrevivido)