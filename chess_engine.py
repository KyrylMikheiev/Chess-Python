class GameState:
    
    def __init__(self, white_pieces):
        
        self.is_players_color_white = white_pieces
        self.white_to_move = True
        
        if self.is_players_color_white:
            self.player_to_move = True
            self.board = [["br", "bn", "bb", "bq", "bk", "bb", "bn", "br"], ["bp"] * 8, ["--"] * 8, ["--"] * 8, ["--"] * 8, ["--"] * 8, ["wp"] * 8, ["wr", "wn", "wb", "wq", "wk", "wb", "wn", "wr"]]
        else:
            self.player_to_move = False
            self.board = [["wr", "wn", "wb", "wq", "wk", "wb", "wn", "wr"], ["wp"] * 8, ["--"] * 8, ["--"] * 8, ["--"] * 8, ["--"] * 8, ["bp"] * 8, ["br", "bn", "bb", "bq", "bk", "bb", "bn", "br"]]
        self.move_log = []

    def make_move(self, move):
        self.board[move.start_row][move.start_col] = "--"
        self.board[move.end_row][move.end_col] = move.moved_piece
        self.move_log.append(move)
        self.player_to_move = not self.player_to_move
        self.white_to_move = not self.white_to_move
        
    def undo_move(self):
        if len(self.move_log) != 0:
            move = self.move_log.pop()
            self.board[move.start_row][move.start_col] = move.moved_piece
            self.board[move.end_row][move.end_col] = move.captured_piece_or_empty
            self.player_to_move = not self.player_to_move
            self.white_to_move = not self.white_to_move
            
        else: 
            print("Starting postion")
            
    def get_valid_moves(self):
        return self.get_all_possible_moves()
    
    def get_all_possible_moves(self):
        moves = []
        for r in range(8):
            for c in range(8):
                color = self.board[r][c][0]
                if (color == "w" and self.white_to_move) or (color == "b" and not self.white_to_move):
                    piece = self.board[r][c][1]
                    if piece == "p":
                        self.get_pawn_moves(r, c, moves)
                    # elif piece == "r":
                    #     self.get_rook_moves(r, c, moves)
                    # elif piece == "n":
                    #     self.get_knight_moves(r, c, moves)
                    # elif piece == "b":
                    #     self.get_bishop_moves(r, c, moves)
                    # elif piece == "queen":
                    #     self.get_queen_moves(r, c, moves)
                    # elif piece == "k":
                    #     self.get_king_moves(r, c, moves)
        return moves
        
    
    def get_pawn_moves(self, r, c, moves):
        # independetly if we play for white or black, moveID stays the same as we would read from the top to the bottom, 
        # even though when we play for white the pawns are on the second rank (board indixation) and not on 6th (from the top to bottom)
        i_am_white_and_to_move = self.is_players_color_white and self.white_to_move
        i_am_white_and_to_wait = self.is_players_color_white and not self.white_to_move
        
        i_am_black_and_to_move = not self.is_players_color_white and not self.white_to_move
        i_am_black_and_to_wait = not self.is_players_color_white and self.white_to_move
        
        #handels user moves
        if self.player_to_move:
            if r - 1 >= 0:
                if self.board[r-1][c] == "--":
                    moves.append(Move((r, c), (r-1, c), self.board))
                    if r == 6 and self.board[r-2][c] == "--":
                        moves.append(Move((r, c), (r-2, c), self.board))
                if c-1 >= 0:
                    if self.board[r-1][c-1][0] == "b" and i_am_white_and_to_move or (self.board[r-1][c-1][0] == "w" and i_am_black_and_to_move):
                        moves.append(Move((r, c), (r-1, c - 1), self.board)) 
                        print("capture left my turn")
                if c+1 <= 7:
                    if self.board[r-1][c+1][0] == "b" and i_am_white_and_to_move or self.board[r-1][c+1][0] == "w" and i_am_black_and_to_move:
                        moves.append(Move((r, c), (r-1, c + 1), self.board))
                        print("capture right my turn")
        #handels enemy/computer moves 
        else:
            if r + 1 <= 7:
                if self.board[r+1][c] == "--":
                    moves.append(Move((r, c), (r+1, c), self.board))
                    if r == 1 and self.board[r+2][c] == "--":
                        moves.append(Move((r, c), (r+2, c), self.board))
                if c-1 >= 0:
                    if self.board[r+1][c-1][0] == "w" and i_am_white_and_to_wait or self.board[r+1][c-1][0] == "b" and i_am_black_and_to_wait:
                        moves.append(Move((r, c), (r + 1, c - 1), self.board))
                        print("capture right enemy move")
                if c+1 <= 7:
                    if self.board[r+1][c+1][0] == "w" and i_am_white_and_to_wait or self.board[r+1][c+1][0] == "b" and i_am_black_and_to_wait :
                        moves.append(Move((r, c), (r + 1, c + 1), self.board)) 
                        print("capture left enemy move")
        # i_am_to_move = self.white_to_move == self.is_players_color_white
        # direction = -1 if i_am_to_move else 1
        # start_row = 6 if i_am_to_move else 1
        # enemy_color = 'b' if self.is_players_color_white else 'w'
        # r_new = r + direction

        # if 0 <= r_new <= 7:
        #     # Forward move
        #     if self.board[r_new][c] == "--":
        #         moves.append(Move((r, c), (r_new, c), self.board))
        #         r_double = r + 2 * direction
        #         if r == start_row and self.board[r_double][c] == "--":
        #             moves.append(Move((r, c), (r_double, c), self.board))
            
        #     # Captures
        #     for dc, direction_label in [(-1, "left"), (1, "right")]:
        #         c_new = c + dc
        #         if 0 <= c_new <= 7:
        #             target = self.board[r_new][c_new]
        #             if target[0] == enemy_color:
        #                 moves.append(Move((r, c), (r_new, c_new), self.board))
        #                 print(f"capture {direction_label} {'my turn' if i_am_to_move else 'enemy move'}")

    def get_rook_moves(self):
        pass
    def get_knight_moves(self):
        pass
    def get_bishop_moves(self):
        pass
    def get_queen_moves(self):
        pass
    def get_king_moves(self):
        pass
    
        
class Move:
    
    def __init__(self, start_pos, end_pos, board):
        self.start_row = start_pos[0]
        self.start_col = start_pos[1]
        self.end_row = end_pos[0]
        self.end_col = end_pos[1]
        
        self.moved_piece = board[self.start_row][self.start_col]
        self.captured_piece_or_empty = board[self.end_row][self.end_col]
        
        self.moveID = self.start_row * 1000 + self.start_col * 100 + self.end_row * 10 + self.end_col
        # print(self.moveID)
        
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        
    
    
        