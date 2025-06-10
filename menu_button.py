import pygame

class MenuButton:
    
    BUTTON_WIDTH, BUTTON_HEIGHT = 400, 50
    BUTTON_AMOUNT = 0
    
    def __init__(self, screen_width, screen_height, font, text):
        self.btn = pygame.Rect(
            screen_width/2 - self.BUTTON_WIDTH/2,
            screen_height/2.5 + self.BUTTON_AMOUNT*70,
            self.BUTTON_WIDTH,
            self.BUTTON_HEIGHT
        )
        self.text = font.render(text, True, "black")
        self.text_rect = self.text.get_rect(center=self.btn.center)
        MenuButton.BUTTON_AMOUNT += 1
        
    def draw(self, screen):
        pygame.draw.rect(screen, "white", self.btn, border_radius=5)
        screen.blit(self.text, self.text_rect)