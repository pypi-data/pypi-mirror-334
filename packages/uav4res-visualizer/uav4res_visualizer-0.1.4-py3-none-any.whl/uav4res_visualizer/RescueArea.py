from TextureManager import TextureManager
from TextManager import TextManager


class RescueArea():
    def __init__(self, position,  number_of_victim: int, important_score: int):
        self.important_score = important_score
        self.position = position
        self.number_of_victim = number_of_victim

    def update(self):
        pass

    def handle_events(self):
        pass

    def draw(self):
        TextureManager().draw_texture(
            name="boat", position=self.position, scale=(30, 30)
        )
        TextManager().print(
            text=f"important_score: {self.important_score},victims: {self.number_of_victim}",
            position=self.position,
            color="black",
            font_size=20,
        )

    def clean(self):
        pass
