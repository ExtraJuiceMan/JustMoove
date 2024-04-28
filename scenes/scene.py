from __future__ import annotations

from abc import abstractmethod
from typing import Optional
from game_state import GameVideoConfiguration
from game_state import GameState
import pygame


class SceneBase:
    def __init__(self):
        pass
        self.next_scene = None

    def set_next_scene(self, scene: SceneBase):
        self.next_scene = scene

    def pop_next_scene(self) -> Optional[SceneBase]:
        if not self.next_scene:
            return None
        
        next_scene = self.next_scene
        self.next_scene = None

        return next_scene

    @abstractmethod
    def handle_event(self, event: pygame.event.Event):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def render(self, screen: pygame.Surface):
        pass
    