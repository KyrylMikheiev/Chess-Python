from constants.window import WIDTH, HEIGHT

#chess board -------------------------------------------------------------------------------------
SQUARE_SIZE = 120
BOARD_SIZE = SQUARE_SIZE * 8
x_offset = (WIDTH - BOARD_SIZE) // 2
y_offset = (HEIGHT - BOARD_SIZE) // 2
WHITE = (237, 214, 176)
BLACK = (184, 135, 98)
HIGHLIGHTED_SQUARE_COLOR = "blue"
LEGAL_MOVES_COLOR = "yellow"
MOVE_HIGHLIGHT_COLOR = (50, 255, 60)  # must be rgb


