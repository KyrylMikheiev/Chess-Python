from ui.menu import Menu
from ui.menu_button import MenuButton
from utils.utils import MENUS

class MainMenu:
    
    def __init__(self, scene_manager):
        self.scene_manager = scene_manager
        
    def handle_event(self, event):
        pass
    
    def update(self, dt):
        pass
    
    def render(self, screen):
        menu = Menu("main", screen)
        menu.draw()