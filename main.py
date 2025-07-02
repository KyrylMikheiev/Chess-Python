import pygame

import chess_engine
from utils import *
from menus import get_menu
from app_state import AppState
import smart_move_finder  
import time
from multiprocessing import Process, Queue

state = AppState()
    
def main(): 
    
    pygame.init()
    init_utils()
    from utils import WINDOW, clock, title_font
    # Get initial menu
    current_buttons = get_menu(state.get_current_menu())
    selected_square = ()
    player_clicks = [] #two tuples
    gs = None
    move = None
    valid_moves = None
    move_made = False
    
    human_turn = None
    game_over = False
    ai_thinking = False
    move_finder_process = None
    move_undone = False
    
    while state.get_running_state():
        mouse_pos = pygame.mouse.get_pos()
        WINDOW.fill(BG_COLOR)
        
        if state.get_current_menu() == "game":
            # current_buttons = []
            if not gs:
                gs = chess_engine.GameState(state.is_players_color_white)
                valid_moves = gs.get_valid_moves()            
                    
            draw_game_state(WINDOW, gs, selected_square, valid_moves)
            human_turn = (gs.is_players_color_white and gs.white_to_move) or (not gs.is_players_color_white and not gs.white_to_move)

                            
        else:
            if not current_buttons:  # only repopulate if empty (after chessgame)
                current_buttons = get_menu(state.get_current_menu())
        
            title = state.get_current_menu().capitalize()
            title_text = title_font.render(title, True, "white")
            WINDOW.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 150))

            for button in current_buttons:
                button.draw(WINDOW)
                
        #click events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                state.set_running_state(False)
            #mouse events
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if state.get_current_menu() != "game":
                    for button in current_buttons:
                        if button.is_clicked(mouse_pos):
                            next_menu = button.action(state)
                            if next_menu:
                                state.set_current_menu(next_menu)
                                current_buttons = get_menu(next_menu)
                elif state.get_current_menu() == "game" and mouse_pos[0] in range (x_offset, x_offset + BOARD_SIZE) and mouse_pos[1] in range (y_offset, y_offset + BOARD_SIZE) and not game_over:
                    human_turn = (gs.is_players_color_white and gs.white_to_move) or (not gs.is_players_color_white and not gs.white_to_move)
                    if human_turn:  
                        col = (mouse_pos[0] - x_offset)//SQUARE_SIZE #from 0 to 7
                        row = (mouse_pos[1] - y_offset)//SQUARE_SIZE #from 0 to 7
                        if selected_square == (row, col):
                            selected_square = ()
                            player_clicks = []
                        else:
                            selected_square = (row, col)
                            player_clicks.append(selected_square)

                        if len(player_clicks) == 2:
                            move = chess_engine.Move(player_clicks[0], player_clicks[1], gs.board, gs=gs)
                            # print(move.moveID)
                            for i in range(len(valid_moves)):
                                if move == valid_moves[i]:
                                    gs.make_move(valid_moves[i])
                                    move_made = True
                                    selected_square = ()
                                    player_clicks = []
                            if not move_made:
                                player_clicks = [selected_square]
                            # if move in valid_moves:
                            #     gs.make_move(move)
                            #     move_made = True
                            # selected_square = ()
                            # player_clicks = []

                            
            #key events
            elif event.type == pygame.KEYDOWN and state.get_current_menu() == "game":
                if event.key == pygame.K_z:
                    gs.undo_move()
                    move_made = True
                    game_over = False
                    if ai_thinking:
                        move_finder_process.terminate()
                        ai_thinking = False
                    move_undone = True  
                if event.key == pygame.K_r:
                    gs = chess_engine.GameState()
                    valid_moves = gs.get_valid_moves()
                    selected_square = ()
                    player_clicks = []
                    move_made = False
                    game_over = False #Reset gameFlag
                    if ai_thinking:
                        move_finder_process.terminate()
                        ai_thinking = False
                    move_undone = True    
              
        if state.get_current_menu() == "game" and gs:      
            if not game_over and not human_turn and not move_undone:
                if not ai_thinking:
                    ai_thinking = True
                    print("thinking....")
                    return_queue = Queue() # used to pass data between processes/ threads
                    move_finder_process = Process(target=smart_move_finder.find_best_move, args=(gs, valid_moves, return_queue))
                    move_finder_process.start() # starting the process
                    
                if not move_finder_process.is_alive():
                    print('Done thinking!!!') 
                    if not return_queue.empty():
                        ai_move = return_queue.get()
                    else:
                        print("AI process terminated before returning a move.")
                        ai_move = smart_move_finder.find_random_move(valid_moves)  
                    # print(ai_move.moveID, "here")
                    gs.make_move(ai_move)
                    move_made = True
                    ai_thinking = False
                                
            if move_made:
                print("MOVE WAS MADE")
                if move:
                    print(move.moveID, "your move")
                if ai_move:
                    print(ai_move.moveID, "ai move")
                valid_moves = gs.get_valid_moves()
                move_made = False
                if not human_turn:
                    move_undone = False
                    
            if gs.checkmate:
                game_over = True
                draw_text(WINDOW, "checkmate")
            elif gs.stalemate:
                game_over = True
                draw_text(WINDOW, "stalemate")
            elif gs.in_check:
                draw_text(WINDOW, "check")            

        pygame.display.flip()
        FPS = 60
        clock.tick(FPS)


    pygame.quit()
    
def draw_game_state(screen, gs, selected_square, valid_moves):
    draw_board(screen, gs.is_players_color_white)
    highlight_squares(screen, gs, valid_moves, selected_square)
    draw_pieces(screen, gs.board)

    
def draw_board(screen, is_players_color_white):
    from utils import char_font 
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

def highlight_squares(screen, gs: chess_engine.GameState, valid_moves, selected_square):
    if selected_square != ():
        r, c = selected_square
        if gs.board[r][c][0] == ("w" if gs.white_to_move else "b"):
            s = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE))
            s.set_alpha(100)
            s.fill(HIGHLIGHTED_SQUARE_COLOR)
            screen.blit(s, (c*SQUARE_SIZE + x_offset, r*SQUARE_SIZE + y_offset))
            s.fill(LEGAL_MOVES_COLOR)
            for move in valid_moves:
                if move.start_row == r and move.start_col == c:
                    screen.blit(s, (move.end_col*SQUARE_SIZE + x_offset, move.end_row*SQUARE_SIZE + y_offset))


def draw_pieces(screen, board):
    for r in range(8):
        for c in range(8):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], pygame.Rect(x_offset + c*SQUARE_SIZE - 3, y_offset + r*SQUARE_SIZE - 5, SQUARE_SIZE, SQUARE_SIZE))


def draw_text(screen, text):
    from utils import title_font
    textObject = title_font.render(text, 0, pygame.Color('Black'))
    textLocation = pygame.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH/2 - textObject.get_width()/2, HEIGHT/2 - textObject.get_height()/2)
    screen.blit(textObject, textLocation)
                        
if __name__ == "__main__":
    main()
