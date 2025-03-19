import os
from .config import IMAGE_DIR
import pygame
from .engine.Singleton import Singleton
from .engine.GameStateManager import GameStateManager
from .engine.InputManager import InputManager
from .engine.Window import Window
from .MenuState import MenuState
from .engine.TextureManager import TextureManager


@Singleton
class Game:
    def __init__(self, width, height, fps):
        pygame.init()
        self.isRunning = True
        self.FPS = fps
        self.window = Window(width, height, self.FPS)
        GameStateManager().push_state(MenuState())
        self.loadTexture()

    def loadTexture(self):
        TextureManager().load_texture("boat", os.path.join(IMAGE_DIR, "boat.png"))
        TextureManager().load_texture(
            "uet_logo", os.path.join(IMAGE_DIR, "uet_logo.png")
        )
        TextureManager().load_texture("arrow", os.path.join(IMAGE_DIR, "arrow.png"))
        TextureManager().load_texture("map1", os.path.join(IMAGE_DIR, "map1.jpeg"))

    def update(self):
        GameStateManager().update()

    def handle_event(self):
        if InputManager().is_quit():
            self.quit()

        self.window.handle_FPS()
        InputManager().update()

        GameStateManager().handle_events()

    def render(self):
        self.window.fill("white")
        GameStateManager().render(self.window)
        pygame.display.flip()

    def quit(self):
        self.isRunning = False

    def clean(self):
        GameStateManager().clean()
        pygame.quit()
