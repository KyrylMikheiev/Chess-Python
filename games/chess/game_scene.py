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
        
        self.selected_square = ()
        self.player_clicks = []
    
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

