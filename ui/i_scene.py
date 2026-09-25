from typing import Protocol
import pygame

from constants.menus import ScenesEnum

class SceneInterface(Protocol):
    
    def handle_event(self, event: pygame.event.EventType) -> ScenesEnum | None:
        pass
    
    def update(self):
        pass
    
    def render(self):
        pass