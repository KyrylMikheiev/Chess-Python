from games.chess.ai import Ai
from games.chess.engine import Engine
from games.chess.game_scene import GameScene
from games.chess.game_state import GameState


class ChessGameController:
    
    """
    1.  Engine generates allowed moves for a user
    2.  User moves a mouse
    3.  User clicks a tile with a piece
    4.  User clicks a tile where the piece should go
    5.  Engine validates if the move is allowed
    6.  Gamestate makes a move 
    7.  Gamestate updates the state (check-/stalemate ? stop, the ai lost : keep going)
    8.  Ai gets allowed moves from the engine
    9.  Ai finds a combination of moves which brings the most score
    10. The first move of combination is given to controller 
    11. Chess controller gives the move to a gamestate
    12. Gamestae makes a move
    13. Gamestate updates the state (check-/stalemate ? stop, the user lost : keep going)
    14. Repeat from the first step till checkmate or stalemate
    15. Show stalemate or checkmate message
    16. Let user play again or navigate to the main menu
    """

    def __init__(self, human_white: bool):
        self.game_scene = GameScene(human_white)
        self.gs = GameState(human_white)
        self.engine = Engine()
        self.ai = Ai()
        self.start_game()
        
    def start_game(self):
        if not self.gs.is_players_color_white:
            self.handle_ai_move()
        self.game_loop()
        
            
    def game_loop(self):
        while not self.gs.checkmate and not self.gs.stalemate:
            self.handle_human_move()
            self.handle_ai_move()
        else:
            self.game_scene.handle_pop_up()
            
    def handle_human_move(self):
        user_valid_moves = self.engine.get_valid_moves()
        user_move = self.game_scene.get_human_move()
        if user_move in user_valid_moves:
            self.gs.make_move(user_move)
        else:
            print("move is not allowed bud")
            raise RuntimeError
        
    def handle_ai_move(self):
        ai_valid_moves = self.engine.get_valid_moves()
        ai_move = self.ai.find_move(self.gs, ai_valid_moves)
        self.gs.make_move(ai_move)