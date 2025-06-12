class GameState:
    
    def __init__(self, white_pieces):
        
        self.is_players_color_white = white_pieces
        self.move_log = []
        
        if self.is_players_color_white:
            self.player_to_move = True
            self.board = [["br", "bn", "bb", "bq", "bk", "bb", "bn", "br"], ["bp"] * 8, ["--"] * 8, ["--"] * 8, ["--"] * 8, ["--"] * 8, ["wp"] * 8, ["wr", "wn", "wb", "wq", "wk", "wb", "wn", "wr"]]
        else:
            self.player_to_move = False
            self.board = [["wr", "wn", "wb", "wq", "wk", "wb", "wn", "wr"], ["wp"] * 8, ["--"] * 8, ["--"] * 8, ["--"] * 8, ["--"] * 8, ["bp"] * 8, ["br", "bn", "bb", "bq", "bk", "bb", "bn", "br"]]
   
    def make_move(self, move):
        self.board[move.start_row][move.start_col] = "--"
        self.board[move.end_row][move.end_col] = move.moved_piece
        self.move_log.append(move)
        self.player_to_move = not self.player_to_move
        
        
class Move:
    
    def __init__(self, start_pos, end_pos, board):
        self.start_row = start_pos[0]
        self.start_col = start_pos[1]
        self.end_row = end_pos[0]
        self.end_col = end_pos[1]
        
        self.moved_piece = board[self.start_row][self.start_col]
        self.captured_piece_or_empty = board[self.end_row][self.end_col]
    
        