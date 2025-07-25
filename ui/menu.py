import pygame
from utils.utils import BUTTON_HEIGHT, BUTTON_WIDTH, MENU_NAME_COLOR, MENU_NAME_FONT, MENUS
from .menu_button import MenuButton

class Menu:
    
    def __init__(self, menu_name):
        self.menu = menu_name
        self.buttons = []
        self.create_buttons()
        font = MENU_NAME_FONT
        self.title_text = font.render(self.menu, True, MENU_NAME_COLOR)
    
    def create_buttons(self):
        for (label, action_name) in MENUS[self.menu]:
            button = MenuButton(label, action_name)
            self.buttons.append(button)

    def draw(self, screen: pygame.surface.Surface):
        dis_info = pygame.display.get_window_size()
        screen.blit(self.title_text, (dis_info[0] // 2 - self.title_text.get_width() // 2, 150))
        for i, button in enumerate(self.buttons):
            x = (screen.get_size()[0] - BUTTON_WIDTH) // 2
            y = (screen.get_size()[1] - BUTTON_HEIGHT) // 2.5 + i * 70
            button: MenuButton
            button.draw(x, y, screen)