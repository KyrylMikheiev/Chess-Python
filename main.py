import pygame

pygame.init()

from utils import WIDTH, WINDOW, FPS, clock, title_font, BG_COLOR, IMAGES, x_offset, y_offset, SQUARE_SIZE
from menus import get_menu
from app_state import AppState

def draw_pieces(board):
     for r in range(8):
        for c in range(8):
            piece = board.get_pieces_array()[r][c]
            if piece != "--":
                WINDOW.blit(IMAGES[piece], pygame.Rect(x_offset + c*SQUARE_SIZE - 3, y_offset + r*SQUARE_SIZE - 5, SQUARE_SIZE, SQUARE_SIZE))

def main(): 
    state = AppState()

    # Get initial menu
    current_buttons = get_menu(state.get_current_menu())

    while state.get_running_state():
        mouse_pos = pygame.mouse.get_pos()
        WINDOW.fill(BG_COLOR)
        
        if state.get_current_menu() == "game":
            current_buttons = []
            board = state.get_board()
            if board:
                board.draw_board()
                draw_pieces(board)
               
        else:
            if not current_buttons:  # only repopulate if empty
                current_buttons = get_menu(state.get_current_menu())
        
            title = state.get_current_menu().capitalize()
            title_text = title_font.render(title, True, "white")
            WINDOW.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 150))

            for button in current_buttons:
                button.draw(WINDOW)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                state.set_running_state(False)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if state.get_current_menu() != "game":
                    for button in current_buttons:
                        if button.is_clicked(mouse_pos):
                            next_menu = button.action(state)
                            if next_menu:
                                state.set_current_menu(next_menu)
                                current_buttons = get_menu(next_menu)

        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
