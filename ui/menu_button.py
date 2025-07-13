import pygame
from utils.utils import (
    BUTTON_FONT,
    BUTTON_FONT_COLOR,
    BUTTON_HEIGHT,
    BUTTON_WIDTH,
    BUTTON_BG_COLOR,
    BUTTON_BG_HOVER_COLOR,
)


class MenuButton:

    def __init__(self, label, action):
        self.label = label
        self.default_color = BUTTON_BG_COLOR
        self.hover_color = BUTTON_BG_HOVER_COLOR
        self.action = action
        self.font = BUTTON_FONT
        self.text = self.font.render(self.label, True, BUTTON_FONT_COLOR)

    def draw(self, x, y, screen):
        self.rect = pygame.Rect(x, y, BUTTON_WIDTH, BUTTON_HEIGHT)
        self.text_rect = self.text.get_rect(center=self.rect.center)
        color = (
            self.hover_color
            if self.is_hovered(pygame.mouse.get_pos())
            else self.default_color
        )
        pygame.draw.rect(screen, color, self.rect, border_radius=5)
        screen.blit(self.text, self.text_rect)

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

    def is_hovered(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)
