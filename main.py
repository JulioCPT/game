from controller import MenuController, GameController
from model import HighscoreModel
from view import GameView

def main():
    model = HighscoreModel()
    view = GameView(1280, 920)
    menu_controller = MenuController(view, model)
    game_controller = GameController(view, model)

    while True:
        escolha = menu_controller.iniciar_menu()
        if escolha == "novo_jogo":
            game_controller.iniciar_jogo()
        elif escolha == "highscores":
            menu_controller.mostrar_highscores()

if __name__ == "__main__":
    main()
    