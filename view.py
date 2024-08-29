import pygame

class GameView:
    def __init__(self, largura, altura):
        pygame.init()
        self.janela = pygame.display.set_mode((largura, altura), pygame.RESIZABLE)
        self.fonte_principal = pygame.font.Font(None, 74)
        self.fonte_timer = pygame.font.Font(None, 36)
        self.cores = {
            "branco": (255, 255, 255),
            "preto": (0, 0, 0),
            "vermelho": (255, 0, 0),
            "verde": (0, 255, 0),
        }

    def desenhar_texto(self, texto, posicao, tamanho_fonte=74, cor="branco"):
        fonte = pygame.font.Font(None, tamanho_fonte)
        texto_renderizado = fonte.render(texto, True, self.cores[cor])
        self.janela.blit(texto_renderizado, posicao)

    def exibir_menu(self, opcoes):
        self.janela.fill(self.cores["preto"])
        for i, (texto, posicao) in enumerate(opcoes.items()):
            self.desenhar_texto(texto, posicao)
        pygame.display.flip()

    def mostrar_highscores(self, highscores):
        self.janela.fill(self.cores["preto"])
        y = 250
        for i, highscore in enumerate(highscores):
            texto = f"{i + 1}: {highscore['nome']} - {highscore['tempo']}s"
            self.desenhar_texto(texto, (580, y), tamanho_fonte=50)
            y += 60
        pygame.display.flip()

    def desenhar_barra_de_vida(self, vida, x=10, y=10, largura=200, altura=20):
        if vida < 0:
            vida = 0
        largura_barra = int(largura * (vida / 100.0))
        cor = self.cores["verde"] if vida > 50 else self.cores["vermelho"]
        pygame.draw.rect(self.janela, cor, (x, y, largura_barra, altura))
        pygame.draw.rect(self.janela, self.cores["branco"], (x, y, largura, altura), 2)
        pygame.display.flip()

    def desenhar_game_over(self, tempo_sobrevivido):
        self.janela.fill(self.cores["preto"])
        self.desenhar_texto("Game Over", (640, 360), tamanho_fonte=72)
        self.desenhar_texto(f"Tempo sobrevivido: {tempo_sobrevivido}s", (640, 460), tamanho_fonte=50)
