import pygame
from core import scene_manager
from core.scene_manager import SceneManager
from ui.menu import Menu
from utils.utils import MENUS

class MainMenu:
    
    def __init__(self, scene_manager: SceneManager):
        self.scene_manager = scene_manager
        self.menu = Menu("main")
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            for button in self.menu.buttons:
                if button.is_clicked(mouse_pos):
                    # print(f"Button '{button.label}' clicked! Action: {button.action}")
                    self.handle_action(button.action)
                    
    def handle_action(self, action):
        if action == "go_to_color_menu":
            from scenes.menus.color_menu import ColorMenu
            self.scene_manager.change_scene(ColorMenu(self.scene_manager))
        elif action == "show_statistics":
            print("show statistics")
        elif action == "show_options":
            print("show options")
        elif action == "quit_game":
            self.scene_manager.quit()
        else:
            print(f"No action bound for: {action}")
    
    def update(self, dt):
        pass
    
    def render(self, screen):
        self.menu.draw(screen)