import pygame

from constants.fonts import MENU_NAME_FONT
from ui.menu_button import MenuButton
from constants.menus import (
    BUTTON_HEIGHT, 
    BUTTON_WIDTH, 
    MENU_NAME_COLOR, 
    MENUS_WITH_BUTTONS_AND_LINKS, 
    ScenesEnum
)

class Menu:
    
    def __init__(self, menu_name: ScenesEnum):
        self.menu_name = menu_name
        self.menu = MENUS_WITH_BUTTONS_AND_LINKS[self.menu_name]
        self.buttons: list[MenuButton] = []
        self.create_buttons()
        font = MENU_NAME_FONT
        self.title_text = font.render(self.menu_name.value, True, MENU_NAME_COLOR)
    
    def create_buttons(self):
        for (label, action_name) in self.menu:
            button = MenuButton(label, action_name)
            self.buttons.append(button)

    def draw(self, screen: pygame.surface.Surface):
        dis_info = pygame.display.get_window_size()
        screen.blit(self.title_text, (dis_info[0] // 2 - self.title_text.get_width() // 2, 150))
        for i, button in enumerate(self.buttons):
            x = (screen.get_size()[0] - BUTTON_WIDTH) // 2
            y = (screen.get_size()[1] - BUTTON_HEIGHT) // 2.5 + i * 70
            button.draw(x, y, screen)