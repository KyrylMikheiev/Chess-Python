class Move:
    
    def __init__(self, start_pos, end_pos, board, gs=None, is_en_passant_possible=False, is_castle_move=False):
        self.start_row = start_pos[0]
        self.start_col = start_pos[1]
        self.end_row = end_pos[0]
        self.end_col = end_pos[1]
        
        self.moved_piece = board[self.start_row][self.start_col]
        self.captured_piece_or_empty = board[self.end_row][self.end_col]
        
        #pawn promotion
        self.is_pawn_promoting = False
        if (
                (self.moved_piece == "wp" and self.end_row == 0 and gs.get_players_color()) or
                (self.moved_piece == "bp" and self.end_row == 7 and gs.get_players_color()) or
                (self.moved_piece == "bp" and self.end_row == 0 and not gs.get_players_color()) or
                (self.moved_piece == "wp" and self.end_row == 7 and not gs.get_players_color())
            ):
            self.is_pawn_promoting = True
        self.en_passant = is_en_passant_possible
        self.is_castle_move = is_castle_move
        
        
        # self.moveID = self.start_row * 1000 + self.start_col * 100 + self.end_row * 10 + self.end_col
        self.moveID = f'{self.start_row}{self.start_col}{self.end_row}{self.end_col}'
        
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        raise Exception("Not the same")
    