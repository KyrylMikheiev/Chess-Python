from multiprocessing import Process, Queue

from games.chess import ai
from games.chess.engine import Engine
from games.chess.game_state import GameState
from games.chess.move import Move


class Controller:
    def __init__(self, is_white):
        self.engine = Engine()
        self.gs = GameState()
        self.valid_moves = self.engine.get_valid_moves()
        self.game_over = False
        self.ai_thinking = False
        self.move_undone = False 
        
        self.move_made = False
        
        self.ai_move = None
        self.move_finder_process = None
        
        self.return_queue = None
        
        self.human_turn = is_white
        
    def handle_ai_move(self):
        if self.game_over or self.human_turn or self.move_undone:
            return
        if not self.ai_thinking:
            self.ai_thinking = True
            # print("thinking....")
            self.return_queue = Queue() # used to pass data between processes/ threads
            self.move_finder_process = Process(target=ai.find_best_move, args=(self.gs, self.valid_moves, self.return_queue))
            self.move_finder_process.start() # starting the process
            
        if not self.move_finder_process.is_alive():
            # print('Done thinking!!!') 
            if not self.return_queue.empty():
                self.ai_move = self.return_queue.get()
            else:
                print("AI process terminated before returning a move.")
                self.ai_move =  ai.find_random_move(self.valid_moves)  
            self.gs.make_move(self.ai_move)
            self.move_made = True
            self.ai_thinking = False
    
    def handle_human_move(self): 
        move =  Move(self.player_clicks[0], self.player_clicks[1], self.gs.board, gs=self.gs)
        # print(move.moveID)
        for i in range(len(self.valid_moves)):
            if move == self.valid_moves[i]:
                self.engine.gs.make_move(self.valid_moves[i])
                self.move_made = True
                self.selected_square = ()
                self.player_clicks = []
                break
        if not self.move_made:
            self.player_clicks = [self.selected_square]
            
    def update(self):
        if self.human_turn:
            self.handle_human_move()
        else:
            self.handle_ai_move()  
        # ------------------------------
        # TODO: Move to game state
        # ------------------------------
        if self.move_made:
            self.valid_moves = self.engine.get_valid_moves()
            self.move_made = False
            if not self.human_turn:
                self.move_undone = False

        self.human_turn = self.gs.player_to_move
    
    def terminate_thinking(self):
        if self.ai_thinking:
            self.move_finder_process.terminate()
            self.ai_thinking = False
    
    def undo_move(self):
        self.gs.undo_move()
        self.move_made = True
        self.game_over = False
        self.terminate_thinking()
        self.move_undone = True 
    
    def is_white_lost(self):
        return self.is_checkmate() and self.gs.white_to_move
    
    def handle_checkmate(self): 
        pass
    def handle_stalemate(self):
        pass
    
    def is_checkmate(self):
        return self.gs.checkmate
    
    def is_stalemate(self):
        return self.gs.stalemate
    
    def is_check(self):
        return self.gs.in_check
