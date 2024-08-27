import pygame
import sys
import pymongo
from game import iniciar_jogo  # Importa a função para iniciar o jogo

# Inicializa o Pygame
pygame.init()

# Conectar ao MongoDB
cliente = pymongo.MongoClient("mongodb://localhost:27017/")  # Altere para o URI correto se necessário
db = cliente["game_db"]
colecao_highscores = db["highscores"]

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)

# Tamanho da tela
largura_janela = 1280
altura_janela = 720
janela = pygame.display.set_mode((largura_janela, altura_janela))

# Fonte
fonte = pygame.font.Font(None, 74)

# Função para exibir o menu principal
def exibir_menu():
    while True:
        janela.fill(PRETO)

        titulo_texto = fonte.render("Jogão kkkkkkk", True, BRANCO)
        janela.blit(titulo_texto, (largura_janela // 2 - titulo_texto.get_width() // 2, 150))

        novo_jogo_texto = fonte.render("Novo Jogo", True, BRANCO)
        janela.blit(novo_jogo_texto, (largura_janela // 2 - novo_jogo_texto.get_width() // 2, 300))

        highscores_texto = fonte.render("Highscores", True, BRANCO)
        janela.blit(highscores_texto, (largura_janela // 2 - highscores_texto.get_width() // 2, 400))

        sair_texto = fonte.render("Sair", True, BRANCO)
        janela.blit(sair_texto, (largura_janela // 2 - sair_texto.get_width() // 2, 500))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if (largura_janela // 2 - novo_jogo_texto.get_width() // 2 <= x <= largura_janela // 2 + novo_jogo_texto.get_width() // 2):
                    if 300 <= y <= 300 + novo_jogo_texto.get_height():
                        iniciar_jogo()  # Inicia o jogo quando "Novo Jogo" for selecionado
                    elif 400 <= y <= 400 + highscores_texto.get_height():
                        mostrar_highscores()  # Exibe os highscores
                    elif 500 <= y <= 500 + sair_texto.get_height():
                        pygame.quit()
                        sys.exit()

# Função para mostrar os highscores
def mostrar_highscores():
    janela.fill(PRETO)

    titulo_texto = fonte.render("Highscores", True, BRANCO)
    janela.blit(titulo_texto, (largura_janela // 2 - titulo_texto.get_width() // 2, 50))

    # Pegar os 10 melhores tempos do banco de dados
    melhores_tempos = colecao_highscores.find().sort("tempo", pymongo.DESCENDING).limit(10)

    y = 150
    for i, highscore in enumerate(melhores_tempos):
        tempo_texto = fonte.render(f"{i + 1}. {highscore['tempo']}s", True, BRANCO)
        janela.blit(tempo_texto, (largura_janela // 2 - tempo_texto.get_width() // 2, y))
        y += 60

    pygame.display.flip()

    # Espera o jogador pressionar qualquer tecla para voltar ao menu
    esperando = True
    while esperando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                esperando = False
                exibir_menu()

# Executa o menu principal
exibir_menu()

