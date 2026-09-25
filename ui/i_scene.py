from typing import Protocol
import pygame

from core.scenes_enum import ScenesEnum

class SceneInterface(Protocol):
    
    def handle_event(self, event: pygame.event.EventType) -> ScenesEnum | None:
        pass
    
    def update(self):
        pass
    
    def render(self):
        pass