import pygame
from .engine.GameState import GameState
from .engine.GameStateManager import GameStateManager
from .engine.InputManager import InputManager
from .engine.Window import Window


class PlayState(GameState):
    def update(self):
        pass

    def handle_events(self):
        from .MenuState import MenuState

        if InputManager().is_key_down(pygame.K_ESCAPE):
            GameStateManager().switch_state(MenuState())

    def render(self, window: Window):
        window.fill((0, 255, 0))

    def clean(self):
        pass
