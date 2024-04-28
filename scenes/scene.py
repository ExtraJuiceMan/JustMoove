from abc import abstractmethod
from game_state import GameVideoConfiguration
from game_state import GameState
import pygame


class SceneBase:
    def __init__(self):
        pass

    @abstractmethod
    def handle_event(self, event: pygame.event.Event):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def render(self, screen: pygame.Surface):
        pass
    