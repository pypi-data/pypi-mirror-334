from .engine.GameState import GameState
from .engine.GameStateManager import GameStateManager
from .engine.TextManager import TextManager
from .engine.TextureManager import TextureManager
from .engine.Button import Button
from .engine.Window import Window


class MenuState(GameState):
    def __init__(self):
        self.buttons = []
        from .MapBuildingState import MapBuildingState

        button = Button(x=230, y=300, width=300, height=100)
        button.set_title("Start Demo")
        button.set_border(2)
        button.set_font_size(40)
        button.on_click(lambda: GameStateManager().push_state(MapBuildingState()))
        self.buttons.append(button)

    def update(self):
        for button in self.buttons:
            button.update()

    def handle_events(self):
        pass

    def render(self, window: Window):
        window.fill("white")
        TextManager().print(
            window = window,
            text="UAV4Res",
            position=(50 + window.width / 2, 180),
            color="black",
            font_size=50,
        )

        TextureManager().draw_texture(
            name="uet_logo",
            window = window,
            position=(50, 130),
            scale=(120, 120),
        )

        for button in self.buttons:
            button.draw(window)

    def clean(self):
        pass
