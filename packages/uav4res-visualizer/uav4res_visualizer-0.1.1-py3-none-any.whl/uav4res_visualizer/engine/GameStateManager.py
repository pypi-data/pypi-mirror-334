from .Singleton import Singleton
from .Window import Window


@Singleton
class GameStateManager:
    def __init__(self):
        self.states = []  # Stack of states

    def push_state(self, state):
        """Push a new state onto the stack."""
        self.states.append(state)

    def pop_state(self):
        """Remove the current state from the stack."""
        if self.states:
            self.states.pop()

    def switch_state(self, state):
        """Replace the current state with a new one."""
        if self.states:
            self.pop_state()
        self.push_state(state)

    def handle_events(self):
        """Forward events to the current state."""
        if self.states:
            self.states[-1].handle_events()

    def update(self):
        """Update the current state."""
        if self.states:
            self.states[-1].update()

    def render(self, window: Window):
        """Render the current state."""
        if self.states:
            self.states[-1].render(window)

    def clean(self):
        if self.states:
            self.states[-1].clean()
