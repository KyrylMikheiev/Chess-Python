import pygame

WINDOW = None
title_font = None
button_font = None
char_font = None
clock = None
WIDTH, HEIGHT = 1280, 1024

MENUS = {
    "main": [
        ("Play", "go_to_color_menu"),
        ("Statistics", "show_statistics"),
        ("Options", "show_options"),
        ("Quit", "quit_game")
    ],
    "color select": [
        ("Play as White", "start_game_white"),
        ("Play as Black", "start_game_black"),
        ("Back", "go_to_main_menu")
    ]
}

def init_utils():
    global WINDOW, clock, title_font, button_font, char_font
    # WIDTH, HEIGHT = 1920, 1080 #fullscreen on my laptop
    WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Chess")
    clock = pygame.time.Clock()

    title_font = pygame.font.SysFont(None, 70)
    button_font = pygame.font.SysFont(None, 40)
    char_font = pygame.font.SysFont(None, 25)

SQUARE_SIZE = 120
BOARD_SIZE = SQUARE_SIZE * 8
x_offset = (WIDTH - BOARD_SIZE) // 2
y_offset = (HEIGHT - BOARD_SIZE) // 2

BUTTON_WIDTH = 400
BUTTON_HEIGHT = 50
X_OFFSET_BUTTON = (WIDTH - BUTTON_WIDTH) // 2
Y_OFFSET_BUTTON = (HEIGHT - BUTTON_WIDTH) // 2

BG_COLOR = (48, 46, 43)
WHITE = (237, 214, 176)
BLACK = (184, 135, 98)
HIGHLIGHTED_SQUARE_COLOR = "blue"
LEGAL_MOVES_COLOR = "yellow"

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


PIECES_SCORES = {"p": 1, "r": 5, "n": 3, "b": 3, "q": 10, "k": 0}
CHECKMATE_SCORE = 1000
STALEMATE_SCORE = 0