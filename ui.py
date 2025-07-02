import pygame
import utils

class MenuButton:
    WIDTH, HEIGHT = 400, 50

    def __init__(self, x, y, label, action):
        self.rect = pygame.Rect(x, y, self.WIDTH, self.HEIGHT)
        self.label = label
        self.default_color = pygame.Color("white")
        self.hover_color = pygame.Color("lightgray")
        self.action = action 

    def draw(self, surface):
        self.font = utils.button_font
        self.text = self.font.render(self.label, True, "black")
        self.text_rect = self.text.get_rect(center=self.rect.center)
        color = self.hover_color if self.is_hovered(pygame.mouse.get_pos()) else self.default_color
        pygame.draw.rect(surface, color, self.rect, border_radius=5)
        surface.blit(self.text, self.text_rect)

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)
    
    def is_hovered(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)