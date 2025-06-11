import pygame
from utils import button_font

class MenuButton:
    WIDTH, HEIGHT = 400, 50

    def __init__(self, x, y, label, action):
        self.font = button_font
        self.rect = pygame.Rect(x, y, self.WIDTH, self.HEIGHT)
        self.label = label
        self.text = self.font.render(label, True, "black")
        self.text_rect = self.text.get_rect(center=self.rect.center)
        self.action = action 

    def draw(self, surface):
        pygame.draw.rect(surface, "white", self.rect, border_radius=5)
        surface.blit(self.text, self.text_rect)

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)