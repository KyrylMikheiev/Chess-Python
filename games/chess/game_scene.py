import os

from games.chess.controller import Controller
from .move import Move
import pygame
from constants import *

class GameScene:
    
    def __init__(self, scene_manager, is_white):
        
        self.scene_manager = scene_manager
        self.screen = self.scene_manager.screen
        self.controller = Controller(is_white)
        self.load_images()
        
        self.selected_square = ()
        self.player_clicks = []
    
    def update(self):
        self.controller.update()
        
    def render(self):
        self.draw_board()
        self.highlight_move(self.controller.gs.move_log)
        self.highlight_squares(self.controller.gs, self.controller.valid_moves, self.selected_square)
        self.draw_pieces_and_chars(self.controller.gs.board, self.controller.gs.is_players_color_white)
        self.abrupt_game_button()
        self.handle_pop_up()

    def abrupt_game_button(self, screen):
        pass
    
    def handle_event(self, event: pygame.event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z:
                self.controller.undo_move()
            if event.key == pygame.K_r:
                self.reset_game()
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.controller.human_turn:
            self.handle_human_move()
            
    def handle_human_move(self):
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
                self.controller.handle_human_move()

    
    def reset_game(self):
        print("reset game")
        self.controller.terminate_thinking()
        self.scene_manager.change_scene(GameScene(self.scene_manager, self.controller.gs.is_players_color_white))

    '''
    drawings in render method:
    '''
    
    def draw_board(self):
        for i in range(8):
            for j in range(8):
                rect = pygame.Rect(j*SQUARE_SIZE + x_offset, i*SQUARE_SIZE + y_offset, SQUARE_SIZE, SQUARE_SIZE)
                pygame.draw.rect(self.screen, WHITE if (i + j) % 2 == 0 else BLACK, rect)

    def highlight_squares(self, gs, valid_moves, selected_square):
        if selected_square != ():
            r, c = selected_square
            if gs.board[r][c][0] == ("w" if gs.white_to_move else "b"):
                s = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE))
                s.set_alpha(100)
                s.fill(HIGHLIGHTED_SQUARE_COLOR)
                self.screen.blit(s, (c*SQUARE_SIZE + x_offset, r*SQUARE_SIZE + y_offset))
                s.fill(LEGAL_MOVES_COLOR)
                for move in valid_moves:
                    move: Move
                    if move.start_row == r and move.start_col == c:
                        self.screen.blit(s, (move.end_col*SQUARE_SIZE + x_offset, move.end_row*SQUARE_SIZE + y_offset))

    def draw_pieces_and_chars(self, board, is_players_color_white):
        CHAR_FONT = pygame.font.SysFont(None, 25)
        
        for r in range(8):
            for c in range(8):
                piece = board[r][c]
                if piece != "--":
                    self.screen.blit(IMAGES[piece], pygame.Rect(x_offset + c*SQUARE_SIZE - 3, y_offset + r*SQUARE_SIZE - 5, SQUARE_SIZE, SQUARE_SIZE))
                if c == 0:
                    char_text = CHAR_FONT.render(str(8-r) if is_players_color_white else str(r + 1), True, BLACK if r % 2 == 0 else WHITE)
                    self.screen.blit(char_text, (c*SQUARE_SIZE + x_offset + 5, r*SQUARE_SIZE + y_offset + 5))
                if r == 7:
                    char_text = CHAR_FONT.render(chr(97+c) if is_players_color_white else chr(104-c), True, BLACK if c % 2 != 0 else WHITE)
                    self.screen.blit(char_text, ((c+1)*SQUARE_SIZE + x_offset - 15, (r+1)*SQUARE_SIZE + y_offset - 20)) 

    def draw_text(self, text):
        title_font = pygame.font.SysFont(None, 70)
        textObject = title_font.render(text, 0, pygame.Color('Black'))
        textLocation = pygame.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH/2 - textObject.get_width()/2, HEIGHT/2 - textObject.get_height()/2)
        self.screen.blit(textObject, textLocation)
    
    def handle_pop_up(self):
        if self.controller.is_white_lost():
            self.draw_text(self.screen, "white in checkmate")
        else:
            self.draw_text(self.screen, "black in checkmate")
        if self.controller.is_stalemate():
            self.draw_text(self.screen, "stalemate")
        elif self.controller.is_check():
            self.draw_text(self.screen, "check") 
            
    def highlight_move(self, move_log):
        if move_log:
            moveID = move_log[-1].moveID
            x1, y1, x2, y2 = map(int, moveID)
            def draw_transparent_overlay(x, y, color):
                overlay = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
                overlay.fill((*color, 120))  # RGBA - last value is alpha (0-255)
                self.screen.blit(overlay, (y * SQUARE_SIZE + x_offset, x * SQUARE_SIZE + y_offset))

            draw_transparent_overlay(x1, y1, MOVE_HIGHLIGHT_COLOR)
            draw_transparent_overlay(x2, y2, MOVE_HIGHLIGHT_COLOR)
            
    """
    utils
    
    """
    def load_images(self):
        pieces = ["wp", "wr", "wn", "wb", "wq", "wk", "bp", "br", "bn", "bb", "bq", "bk"]
        for piece in pieces:
            IMAGES[piece] = pygame.image.load(os.path.join("assets", "images", f'{piece}.png'))
    