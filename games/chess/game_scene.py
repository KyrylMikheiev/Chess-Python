from games.chess.controller import Controller
from games.chess.ui import ChessUi
from .move import Move
import pygame
from constants import *

class GameScene:
    
    def __init__(self, scene_manager, is_white):
        
        self.scene_manager = scene_manager
        self.screen = self.scene_manager.screen
        self.controller = Controller(is_white)
        self.ui = ChessUi(self.screen)
        
        self.start_square: tuple[int, int] | None = None
        self.end_square: tuple[int, int] | None = None
        self.move: Move
    
    def update(self):
        self.controller.update()
        
    def render(self):
        self.ui.render()
        
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
            given_col = (mouse_pos[0] - x_offset)//SQUARE_SIZE #from 0 to 7
            given_row = (mouse_pos[1] - y_offset)//SQUARE_SIZE #from 0 to 7
            next_square = (given_row, given_col)
            if not self.start_square:
                self.start_square = next_square
            #if user clicked same square twice
            elif self.start_square == next_square:
                self.start_square = None
            else:
                self.end_square = next_square
                self.move = Move(self.start_square, self.end_square)
                self.start_square = None
                self.end_square = None
                
    def get_human_move(self):
        self.handle_human_move()
        if not self.move:
            print("there is no move from game scene to see")
            raise RuntimeError
        return self.move

    def reset_game(self):
        print("reset game")
        self.controller.terminate_thinking()
        self.scene_manager.change_scene(GameScene(self.scene_manager, self.controller.gs.is_players_color_white))

