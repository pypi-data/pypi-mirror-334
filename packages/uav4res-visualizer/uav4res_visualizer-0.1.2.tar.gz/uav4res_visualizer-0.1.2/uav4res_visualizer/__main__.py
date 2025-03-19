from .Game import Game


def main():
    game = Game(width=768, height=700, fps=120)
    while game.isRunning:
        game.update()
        game.handle_event()
        game.render()

    game.clean()


if __name__ == "__main__":
    main()
