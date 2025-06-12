import pygame
from utils import SQUARE_SIZE, WHITE, BLACK, x_offset, y_offset, char_font

class Board:
    
    def __init__(self, screen, white_pieces):
        self.font = char_font
        self.white_pieces = white_pieces
        self.screen = screen
        self.size = SQUARE_SIZE
        self.x_off = x_offset
        self.y_off = y_offset
        
    def draw_board(self):
            for i in range(8):
                for j in range(8):
                    if (i + j) % 2 == 0:
                        self.square_color = WHITE
                    else:
                        self.square_color = BLACK
                    self.rect = pygame.Rect(j*self.size + self.x_off, i*self.size + self.y_off, self.size, self.size)
                    pygame.draw.rect(self.screen, self.square_color, self.rect)
                    if j == 0:
                        self.char_text = self.font.render(str(8-i) if self.white_pieces else str(i + 1), True, BLACK if i % 2 == 0 else WHITE)
                        self.screen.blit(self.char_text, (j*self.size + self.x_off + 5, i*self.size + self.y_off + 5))
                    if i == 7:
                        self.char_text = self.font.render(chr(97+j) if self.white_pieces else chr(104-j), True, BLACK if j % 2 != 0 else WHITE)
                        self.screen.blit(self.char_text, ((j+1)*self.size + self.x_off - 15, (i+1)*self.size + self.y_off - 20))            

