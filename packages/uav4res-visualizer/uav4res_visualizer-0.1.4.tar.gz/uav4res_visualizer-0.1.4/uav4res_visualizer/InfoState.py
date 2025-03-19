import pygame
from .engine.GameState import GameState
from .engine.GameStateManager import GameStateManager
from .engine.InputManager import InputManager
from .engine.TextManager import TextManager
from .engine.TextureManager import TextureManager
from .engine.Button import Button
from .engine.Window import Window


class InfoState(GameState):
    def __init__(self):
        self.buttons = []

        from .MenuState import MenuState

        button = Button(x=280, y=500, width=200, height=65)
        button.set_title("Back")
        button.set_border(2)
        button.on_click(lambda: GameStateManager().switch_state(MenuState()))
        self.buttons.append(button)

    def update(self):
        for button in self.buttons:
            button.update()

    def handle_events(self):
        from PlayState import PlayState

        if InputManager().is_key_down(pygame.K_RETURN):
            GameStateManager().switch_state(PlayState())

    def render(self, window: Window):
        window.fill("white")
        TextManager().print(
            text="Fluffy (UET-VNU): UAV4Res",
            position=(50 + window.width / 2, 80),
            color="black",
            font_size=50,
        )

        TextureManager().draw_texture(
            name="uet_logo",
            position=(40, 30),
            scale=(100, 100),
        )

        TextManager().print(
            text="Project from team Fluffy UET-VNU, Project from team Fluffy UET-VNU, Project from team Fluffy UET-VNU",
            position=(window.width / 2, 300),
            color="black",
            font_size=30,
            max_width=500,
        )

        for button in self.buttons:
            button.draw(window)

    def clean(self):
        pass
