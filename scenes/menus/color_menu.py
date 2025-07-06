import pygame
from core.scene_manager import SceneManager
from scenes.game_scene import GameScene
from ui.menu import Menu
from utils.utils import MENUS

class ColorMenu:
    
    def __init__(self, scene_manager: SceneManager):
        self.scene_manager = scene_manager
        self.menu = Menu("color select")
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            for button in self.menu.buttons:
                if button.is_clicked(mouse_pos):
                    # print(f"Button '{button.label}' clicked! Action: {button.action}")
                    self.handle_action(button.action)
    
        """
            "color select": [
        ("Play as White", "start_game_white"),
        ("Play as Black", "start_game_black"),
        ("Back", "go_to_main_menu")
    ]
        """
    def handle_action(self, action):
        if action == "start_game_white":
            self.scene_manager.change_scene(GameScene(self.scene_manager, True))
            print("Start game as white!")  # Placeholder
        elif action == "start_game_black":
            self.scene_manager.change_scene(GameScene(self.scene_manager, False))
            print("Start game as black!")  # Placeholder
        elif action == "go_to_main_menu":
            from scenes.menus.main_menu import MainMenu
            self.scene_manager.change_scene(MainMenu(self.scene_manager))
            print("Back to main menu!")  # Placeholder
        else:
            print(f"No action bound for: {action}")
    
    def update(self, dt):
        pass
    
    def render(self, screen):
        self.menu.draw(screen)