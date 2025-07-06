from multiprocessing import Process, Queue
import os
from games.chess import ai
from games.chess.engine import GameState, Move
import pygame
from utils.utils import *

class GameScene:
    
    def __init__(self, scene_manager, is_white):
        self.scene_manager = scene_manager
        self.gs = GameState(is_white)
        self.valid_moves = self.gs.get_valid_moves()
        self.load_images()
        
        self.selected_square = ()
        self.player_clicks = []
        self.move_made = False
        
        self.human_turn = is_white

        self.game_over = False
        self.ai_thinking = False
        self.move_undone = False 
        
        self.move = None
        self.ai_move = None
        self.move_finder_process = None
        
        self.return_queue = None
        
    def load_images(self):
        pieces = ["wp", "wr", "wn", "wb", "wq", "wk", "bp", "br", "bn", "bb", "bq", "bk"]
        for piece in pieces:
            IMAGES[piece] = pygame.image.load(os.path.join("assets", "images", f'{piece}.png'))
        
    def render(self, screen):
        self.human_turn = (self.gs.is_players_color_white and self.gs.white_to_move) or (not self.gs.is_players_color_white and not self.gs.white_to_move)
        self.draw_board(screen, self.gs.is_players_color_white)
        self.highlight_squares(screen, self.gs, self.valid_moves, self.selected_square)
        self.draw_pieces(screen, self.gs.board)
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            if mouse_pos[0] in range (x_offset, x_offset + BOARD_SIZE) and mouse_pos[1] in range (y_offset, y_offset + BOARD_SIZE):
                col = (mouse_pos[0] - x_offset)//SQUARE_SIZE #from 0 to 7
                row = (mouse_pos[1] - y_offset)//SQUARE_SIZE #from 0 to 7
                if self.selected_square == (row, col):
                    self.selected_square = ()
                    self.player_clicks = []
                else:
                    self.selected_square = (row, col)
                    self.player_clicks.append(self.selected_square)

                if len(self.player_clicks) == 2:
                    move =  Move(self.player_clicks[0], self.player_clicks[1], self.gs.board, gs=self.gs)
                    # print(move.moveID)
                    for i in range(len(self.valid_moves)):
                        if move == self.valid_moves[i]:
                            self.gs.make_move(self.valid_moves[i])
                            self.move_made = True
                            self.selected_square = ()
                            self.player_clicks = []
                    if not self.move_made:
                        self.player_clicks = [self.selected_square]
                        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z:
                self.gs.undo_move()
                self.move_made = True
                self.game_over = False
                if self.ai_thinking:
                    self.move_finder_process.terminate()
                    self.ai_thinking = False
                self.move_undone = True  
            if event.key == pygame.K_r:
                self.gs =  GameState()
                self.valid_moves = self.gs.get_valid_moves()
                self.selected_square = ()
                self.player_clicks = []
                self.move_made = False
                self.game_over = False #Reset gameFlag
                if self.ai_thinking:
                    self.move_finder_process.terminate()
                    self.ai_thinking = False
                self.move_undone = True
                    
    def update(self, screen):
        if not self.game_over and not self.human_turn and not self.move_undone:
            if not self.ai_thinking:
                self.ai_thinking = True
                print("thinking....")
                self.return_queue = Queue() # used to pass data between processes/ threads
                self.move_finder_process = Process(target=ai.find_best_move, args=(self.gs, self.valid_moves, self.return_queue))
                self.move_finder_process.start() # starting the process
                
            if not self.move_finder_process.is_alive():
                print('Done thinking!!!') 
                if not self.return_queue.empty():
                    self.ai_move = self.return_queue.get()
                else:
                    print("AI process terminated before returning a move.")
                    self.ai_move =  ai.find_random_move(self.valid_moves)  
                # print(ai_move.moveID, "here")
                self.gs.make_move(self.ai_move)
                self.move_made = True
                self.ai_thinking = False
                                
        if self.move_made:
            print("MOVE WAS MADE")
            if self.move:
                print(self.move.moveID, "your move")
            if self.ai_move:
                print(self.ai_move.moveID, "ai move")
            self.valid_moves = self.gs.get_valid_moves()
            self.move_made = False
            if not self.human_turn:
                self.move_undone = False
                
        if self.gs.checkmate:
            self.game_over = True
            self.draw_text(screen, "checkmate")
        elif self.gs.stalemate:
            self.game_over = True
            self.draw_text(screen, "stalemate")
        elif self.gs.in_check:
            self.draw_text(screen, "check")     
        
    def draw_board(self, screen, is_players_color_white):
        char_font = pygame.font.SysFont(None, 25)
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

    def highlight_squares(self, screen, gs:  GameState, valid_moves, selected_square):
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


    def draw_pieces(self, screen, board):
        for r in range(8):
            for c in range(8):
                piece = board[r][c]
                if piece != "--":
                    screen.blit(IMAGES[piece], pygame.Rect(x_offset + c*SQUARE_SIZE - 3, y_offset + r*SQUARE_SIZE - 5, SQUARE_SIZE, SQUARE_SIZE))

    def draw_text(self, screen, text):
        title_font = pygame.font.SysFont(None, 70)
        textObject = title_font.render(text, 0, pygame.Color('Black'))
        textLocation = pygame.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH/2 - textObject.get_width()/2, HEIGHT/2 - textObject.get_height()/2)
        screen.blit(textObject, textLocation)