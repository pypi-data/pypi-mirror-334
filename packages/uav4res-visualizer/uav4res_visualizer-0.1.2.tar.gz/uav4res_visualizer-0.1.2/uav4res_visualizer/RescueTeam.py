from .engine.TextureManager import TextureManager
from .engine.TextManager import TextManager


class RescueTeam:
    def __init__(self, position, number_of_seats: int):
        self.position = position
        self.number_of_seats = number_of_seats
        self.speed = 2

    def update(self):
        pass

    def handle_events(self):
        pass

    def draw(self):
        TextureManager().draw_texture(
            name="boat", position=self.position, scale=(30, 30)
        )
        TextManager().print(
            text=f"seats: {self.number_of_seats}",
            position=self.position,
            color="black",
            font_size=20,
        )

    def clean(self):
        pass
