import pygame

pygame.init()

import chess_engine
from utils import *
from menus import get_menu
from app_state import AppState

state = AppState()
    
def main(): 

    # Get initial menu
    current_buttons = get_menu(state.get_current_menu())
    selected_square = ()
    player_clicks = [] #two tuples
    gs = None
    move = None
    valid_moves = None
    move_made = False
    
    while state.get_running_state():
        mouse_pos = pygame.mouse.get_pos()
        WINDOW.fill(BG_COLOR)
        
        if state.get_current_menu() == "game":
            # current_buttons = []
            if not gs:
                gs = chess_engine.GameState(state.is_players_color_white)
                valid_moves = gs.get_valid_moves()
            
            draw_game_state(WINDOW, gs)
        else:
            if not current_buttons:  # only repopulate if empty (after chessgame)
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
                elif state.get_current_menu() == "game" and mouse_pos[0] in range (x_offset, x_offset + BOARD_SIZE) and mouse_pos[1] in range (y_offset, y_offset + BOARD_SIZE):
                    col = (mouse_pos[0] - x_offset)//SQUARE_SIZE #from 0 to 7
                    row = (mouse_pos[1] - y_offset)//SQUARE_SIZE #from 0 to 7
                    if selected_square == (row, col):
                        selected_square = ()
                        player_clicks = []
                    else:
                        selected_square = (row, col)
                        player_clicks.append(selected_square)

                    if len(player_clicks) == 2:
                        move = chess_engine.Move(player_clicks[0], player_clicks[1], gs.board)
                        # print(move.moveID)
                        if move in valid_moves:
                            gs.make_move(move)
                            move_made = True
                        selected_square = ()
                        player_clicks = []
                        
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z and event.mod & pygame.KMOD_CTRL:
                    gs.undo_move()
                    move_made = True
                    
        if move_made:
            
            valid_moves = gs.get_valid_moves()
            move_made = False
                    

        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()
    
def draw_game_state(screen, gs):
    draw_board(screen, gs.is_players_color_white)
    draw_pieces(screen, gs.board)
    
def draw_board(screen, is_players_color_white):
    for i in range(8):
        for j in range(8):
            rect = pygame.Rect(j*SQUARE_SIZE + x_offset, i*SQUARE_SIZE + y_offset, SQUARE_SIZE, SQUARE_SIZE)
            pygame.draw.rect(screen, WHITE if (i + j) % 2 == 0 else BLACK, rect)
            if j == 0:
                char_text = char_font.render(str(8-i) if is_players_color_white else str(i + 1), True, BLACK if i % 2 == 0 else WHITE)
                screen.blit(char_text, (j*SQUARE_SIZE + x_offset + 5, i*SQUARE_SIZE + y_offset + 5))
            if i == 7:
                char_text = char_font.render(chr(97+j) if is_players_color_white else chr(104-j), True, BLACK if j % 2 != 0 else WHITE)
                screen.blit(char_text, ((j+1)*SQUARE_SIZE + x_offset - 15, (i+1)*SQUARE_SIZE + y_offset - 20))            

def draw_pieces(screen, board):
    for r in range(8):
        for c in range(8):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], pygame.Rect(x_offset + c*SQUARE_SIZE - 3, y_offset + r*SQUARE_SIZE - 5, SQUARE_SIZE, SQUARE_SIZE))

                        
if __name__ == "__main__":
    main()
