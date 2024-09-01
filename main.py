import pygame
from controller import MenuController, GameController
from model import HighscoreModel
from view import GameView

def main():
    pygame.mixer.init()
    pygame.mixer.music.load("TRILHA_FODA.mp3")
    pygame.mixer.music.set_volume(0.1)
    model = HighscoreModel()
    view = GameView(1280, 720)
    menu_controller = MenuController(view, model)
    game_controller = GameController(view, model)

    while True:
        escolha = menu_controller.iniciar_menu()
        if escolha == "novo_jogo":
            game_controller.iniciar_jogo()
        elif escolha == "highscores":
            menu_controller.mostrar_highscores()
        elif escolha == "creditos":
            menu_controller.mostrar_creditos()
            

if __name__ == "__main__":
    main()