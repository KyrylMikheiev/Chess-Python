import pygame

from core.i_scene import SceneInterface
from core.i_scene_manager import SceneManagerInterface
from core.scenes_enum import ScenesEnum
from ui.menu import Menu

class Scene(SceneInterface):
    
    def __init__(self, scene_manager: SceneManagerInterface, name: ScenesEnum):
        self.name = name
        self.scene_manager = scene_manager
        self.menu = Menu(self.name)
    
    def handle_event(self, event: pygame.event.EventType):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            for button in self.menu.buttons:
                if button.is_clicked(mouse_pos):
                    self.scene_manager.set_scene(button.action)
    
    def update(self):
        pass
    
    def render(self):
        self.menu.draw(self.scene_manager.screen)