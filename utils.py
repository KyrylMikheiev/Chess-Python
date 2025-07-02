import pygame

WIDTH, HEIGHT = 1280, 1024
# WIDTH, HEIGHT = 1920, 1080 #fullscreen on my laptop
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

PIECE_DIRECTIONS = {
    "r": [(+1, 0), (0, +1), (-1, 0), (0, -1)],
    "b": [(+1, +1), (+1, -1), (-1, -1), (-1, +1)],
    "n": [(-2, +1), (-1, +2), (+1, +2), (+2, +1), (-2, -1), (-1, -2), (+1, -2), (+2, -1)],
    "q": [(+1, +1), (+1, -1), (-1, -1), (-1, +1), (+1, 0), (0, +1), (-1, 0), (0, -1)],
    "k": [(0, +1), (+1, 0), (-1, 0), (0, -1), (+1, +1), (+1, -1), (-1, -1), (-1, +1)]
}

WHITE_BOARD = [
                ["br", "bn", "bb", "bq", "bk", "bb", "bn", "br"], 
                ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
                ["--", "--", "--", "--", "--", "--", "--", "--"],
                ["--", "--", "--", "--", "--", "--", "--", "--"],
                ["--", "--", "--", "--", "--", "--", "--", "--"],
                ["--", "--", "--", "--", "--", "--", "--", "--"],
                ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
                ["wr", "wn", "wb", "wq", "wk", "wb", "wn", "wr"]
               ]
BLACK_BOARD = [
                ["wr", "wn", "wb", "wk", "wq", "wb", "wn", "wr"], 
                ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
                ["--", "--", "--", "--", "--", "--", "--", "--"],
                ["--", "--", "--", "--", "--", "--", "--", "--"],
                ["--", "--", "--", "--", "--", "--", "--", "--"],
                ["--", "--", "--", "--", "--", "--", "--", "--"],
                ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
                ["br", "bn", "bb", "bk", "bq", "bb", "bn", "br"]
               ]
