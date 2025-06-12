import pygame

WIDTH, HEIGHT = 1280, 1024
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess")
FPS = 60
clock = pygame.time.Clock()

title_font = pygame.font.SysFont(None, 70)
button_font = pygame.font.SysFont(None, 40)
char_font = pygame.font.SysFont(None, 25)

SQUARE_SIZE = 120
BOARD_SIZE = SQUARE_SIZE * 8
x_offset = (WIDTH - BOARD_SIZE) // 2
y_offset = (HEIGHT - BOARD_SIZE) // 2

BG_COLOR = (48, 46, 43)
WHITE = (237, 214, 176)
BLACK = (184, 135, 98)

IMAGES = {}
