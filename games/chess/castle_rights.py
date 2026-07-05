from .move import Move

class CastleRights():
    
    def __init__(self, wks, wqs, bks, bqs):
        self.wks = wks
        self.wqs = wqs
        self.bks = bks
        self.bqs = bqs
        
    '''
    to castle:
    1. check if the king is in check
    2. Check castle rights (maybe king moved, or rook)
    3. check if the square between rook and king are in check
    
    we call method "get_castle_moves()" only in method "get_all_possible_moves()". 
    And get_all_possible_moves() is called if we have one check or no checks at all. 
    if there is a check, all castle moves are going to be eliminated anyway. 
    So it is going to be called in case of no checks. 
    That is the reason we dont need to check the first rule
    '''
    def get_castle_moves(self, location, moves):
        r = location[0]
        c = location[1]
        if self.is_players_color_white:
            if self.current_castle_rights.wks and self.white_to_move or self.current_castle_rights.bks and not self.white_to_move:
                self.get_kingside_moves(r, c, moves, "right")
            if self.current_castle_rights.wqs and self.white_to_move or self.current_castle_rights.bqs and not self.white_to_move:
                self.get_queenside_moves(r, c, moves, "left")
        else:
            if self.current_castle_rights.wks and self.white_to_move or self.current_castle_rights.bks and not self.white_to_move:
                self.get_kingside_moves(r, c, moves, "left")
            if self.current_castle_rights.wqs and self.white_to_move or self.current_castle_rights.bqs and not self.white_to_move:
                self.get_queenside_moves(r, c, moves, "right")
                
    def get_kingside_moves(self, r, c, moves, dir):
        if dir == "right":
            if self.board[r][5] == "--" and self.board[r][6] == "--":
                if not self.square_under_attack(r, 5) and not self.square_under_attack(r, 6):
                    moves.append(Move((r, c), (r, 6), self.board, is_castle_move=True))
        elif dir == "left":
            if self.board[r][1] == "--" and self.board[r][2] == "--":
                if not self.square_under_attack(r, 1) and not self.square_under_attack(r, 2):
                    moves.append(Move((r, c), (r, 1), self.board, is_castle_move=True))
    
    def get_queenside_moves(self, r, c, moves, color):
        if color == "left":
            if self.board[r][1] == "--" and self.board[r][2] == "--" and self.board[r][3] == "--":
                if not self.square_under_attack(r, 1) and not self.square_under_attack(r, 2) and not self.square_under_attack(r, 3):
                    moves.append(Move((r, c), (r, 2), self.board, is_castle_move=True))
        elif color == "right":
            if self.board[r][4] == "--" and self.board[r][5] == "--" and self.board[r][6] == "--":
                if not self.square_under_attack(r, 4) and not self.square_under_attack(r, 5) and not self.square_under_attack(r, 6):
                    moves.append(Move((r, c), (r, 5), self.board, is_castle_move=True))
                    
    def update_castle_rights(self, move: Move):
        if move.moved_piece == "wk":
            self.current_castle_rights.wks = False
            self.current_castle_rights.wqs = False
        if move.moved_piece == "bk":
            self.current_castle_rights.bks = False
            self.current_castle_rights.bqs = False
        if move.moved_piece[1] == "r":
            if self.player_to_move:
                if self.is_players_color_white:
                    if move.start_row == 7 and move.start_col == 0:
                        self.current_castle_rights.wqs = False
                    if move.start_row == 7 and move.start_col == 7:
                        self.current_castle_rights.wks = False
                else:
                    if move.start_row == 7 and move.start_col == 0:
                        self.current_castle_rights.bks = False
                    if move.start_row == 7 and move.start_col == 7:
                        self.current_castle_rights.bqs = False
            else:
                if self.is_players_color_white:
                    if move.start_row == 0 and move.start_col == 0:
                        self.current_castle_rights.bqs = False
                    if move.start_row == 0 and move.start_col == 7:
                        self.current_castle_rights.bks = False
                else:
                    if move.start_row == 0 and move.start_col == 0:
                        self.current_castle_rights.wks = False
                    if move.start_row == 0 and move.start_col == 7:
                        self.current_castle_rights.wqs = False
                        
    def square_under_attack(self, r, c):
        self.white_to_move = not self.white_to_move
        opp_moves = self.get_all_possible_moves()
        self.white_to_move = not self.white_to_move
        for move in opp_moves:
            if move.end_row == r and move.end_col == c:
                return True
        return False
    