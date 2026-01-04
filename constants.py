import pygame

#default window size
WIDTH, HEIGHT = 1280, 1024

#chess board -------------------------------------------------------------------------------------
SQUARE_SIZE = 120
BOARD_SIZE = SQUARE_SIZE * 8
x_offset = (WIDTH - BOARD_SIZE) // 2
y_offset = (HEIGHT - BOARD_SIZE) // 2
BG_COLOR = (48, 46, 43)
WHITE = (237, 214, 176)
BLACK = (184, 135, 98)
HIGHLIGHTED_SQUARE_COLOR = "blue"
LEGAL_MOVES_COLOR = "yellow"
MOVE_HIGHLIGHT_COLOR = (50, 255, 60)  # must be rgb

CHAR_FONT = pygame.font.SysFont(None, 25)


#menu ui settings -------------------------------------------------------------------------------------
MENU_NAME_COLOR = "white"
MENU_NAME_FONT = pygame.font.SysFont(None, 70)

BUTTON_WIDTH = 400
BUTTON_HEIGHT = 50
X_OFFSET_BUTTON = (WIDTH - BUTTON_WIDTH) // 2
Y_OFFSET_BUTTON = (HEIGHT - BUTTON_WIDTH) // 2
BUTTON_BG_COLOR = "white"
BUTTON_BG_HOVER_COLOR = "lightgray"
BUTTON_FONT_COLOR = "black"
BUTTON_FONT = pygame.font.SysFont(None, 40)

#menus -------------------------------------------------------------------------------------
MENUS = {
    "main": [
        ("Play", "go_to_color_menu"),
        ("Statistics", "show_statistics"),
        ("Options", "show_options"),
        ("Quit", "quit_game"),
    ],
    "color select": [
        ("Play as White", "start_game_white"),
        ("Play as Black", "start_game_black"),
        ("Back", "go_to_main_menu"),
    ],
    "in game": [
        ("End the game", "abrupt_game")
    ]
}

#engine-------------------------------------------------------------------------------------
IMAGES = {}

PIECE_DIRECTIONS = {
    "r": [(+1, 0), (0, +1), (-1, 0), (0, -1)],
    "b": [(+1, +1), (+1, -1), (-1, -1), (-1, +1)],
    "n": [(-2, +1), (-1, +2), (+1, +2), (+2, +1), (-2, -1), (-1, -2), (+1, -2), (+2, -1)],
    "q": [(+1, +1), (+1, -1), (-1, -1), (-1, +1), (+1, 0), (0, +1), (-1, 0), (0, -1)],
    "k": [(0, +1), (+1, 0), (-1, 0), (0, -1), (+1, +1), (+1, -1), (-1, -1), (-1, +1)],
}

WHITE_BOARD = [
    ["br", "bn", "bb", "bq", "bk", "bb", "bn", "br"],
    ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
    ["--", "--", "--", "--", "--", "--", "--", "--"],
    ["--", "--", "--", "--", "--", "--", "--", "--"],
    ["--", "--", "--", "--", "--", "--", "--", "--"],
    ["--", "--", "--", "--", "--", "--", "--", "--"],
    ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
    ["wr", "wn", "wb", "wq", "wk", "wb", "wn", "wr"],
]

BLACK_BOARD = [
    ["wr", "wn", "wb", "wk", "wq", "wb", "wn", "wr"],
    ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
    ["--", "--", "--", "--", "--", "--", "--", "--"],
    ["--", "--", "--", "--", "--", "--", "--", "--"],
    ["--", "--", "--", "--", "--", "--", "--", "--"],
    ["--", "--", "--", "--", "--", "--", "--", "--"],
    ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
    ["br", "bn", "bb", "bk", "bq", "bb", "bn", "br"],
]

#ai-------------------------------------------------------------------------------------
PIECES_SCORES = {"p": 1, "r": 5, "n": 3, "b": 3, "q": 10, "k": 0}
CHECKMATE_SCORE = 1000
STALEMATE_SCORE = 0
