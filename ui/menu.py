import pygame
from utils.utils import BUTTON_HEIGHT, BUTTON_WIDTH, MENUS, WIDTH, HEIGHT, X_OFFSET_BUTTON
from .menu_button import MenuButton

class Menu:
    
    def __init__(self, menu_name, screen: pygame.surface.Surface):
        self.menu = menu_name
        self.buttons = []
        self.screen = screen
    
    def draw(self):
        for i, (label, action_name) in enumerate(MENUS[self.menu]):
            x = (self.screen.get_size()[0] - BUTTON_WIDTH) // 2
            y = (self.screen.get_size()[1] - BUTTON_HEIGHT) // 2.5 + i * 70
            button = MenuButton(x, y, label, "hz")
            self.buttons.append(button)
            button.draw(self.screen)
            
    