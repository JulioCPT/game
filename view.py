import pygame

class GameView:
    def __init__(self, largura, altura):
        pygame.init()
        self.largura = largura
        self.altura = altura
        self.janela = pygame.display.set_mode((largura, altura), pygame.RESIZABLE)
        self.fundo = pygame.image.load("Floor.png").convert()  # Carregue sua imagem de fundo
        self.fundo = pygame.transform.scale(self.fundo, (largura, altura))  # Escale para o tamanho inicial da tela
        self.fonte_principal = pygame.font.Font(None, 74)
        self.fonte_timer = pygame.font.Font(None, 36)
        self.cores = {
            "branco": (255, 255, 255),
            "preto": (0, 0, 0),
            "vermelho": (255, 0, 0),
            "verde": (0, 255, 0),
        }

    def desenhar_fundo(self):
        fundo = pygame.transform.scale(self.fundo, (self.largura, self.altura))  # Ajusta o fundo ao tamanho atual da tela
        self.janela.blit(fundo, (0, 0))

    def atualizar_tamanho(self, largura, altura):
        self.largura = largura
        self.altura = altura
        self.janela = pygame.display.set_mode((largura, altura), pygame.RESIZABLE)
        self.fundo = pygame.transform.scale(pygame.image.load("Floor.png").convert(), (largura, altura))  # Redimensiona o fundo novamente

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
            if 'nome' not in highscore or 'tempo' not in highscore:
                print(f"Documento inválido encontrado: {highscore}")
                continue  # Pule esse documento se for inválido

            texto = f"{i + 1}: {highscore['nome']} - {highscore['tempo']}s"
            self.desenhar_texto(texto, (820, y), tamanho_fonte=50)
            y += 60
        pygame.display.flip()
    
    def mostrar_creditos(self):
        running = True
        while running:
            self.view.janela.fill(self.view.cores["preto"])
            self.view.desenhar_texto("Créditos", (590, 300))
            self.view.desenhar_texto("teste", (640, 400))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    running = False  # Sai do loop e volta ao menu

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
        self.desenhar_texto("Game Over", (810, 360), tamanho_fonte=72)
        self.desenhar_texto(f"Tempo sobrevivido: {tempo_sobrevivido}s", (750, 460), tamanho_fonte=50)
        