from abc import ABC, abstractmethod
from .Window import Window 


# Abstract class for a game state
class GameState(ABC):
    @abstractmethod
    def handle_events(self):
        """Handle user input."""
        pass

    @abstractmethod
    def update(self):
        """Update the game logic."""
        pass

    @abstractmethod
    def render(self, window: Window):
        """Render the game state."""
        pass

    @abstractmethod
    def clean(self):
        """Clean the game state."""
        pass

