from constants import PIECE_DIRECTIONS
from .move import Move


class Pieces:
    
    def __init__(self):
        self.move_functions = {
                "p": self.get_pawn_moves, "r": self.get_rook_moves, 
                "n": self.get_knight_moves, "b": self.get_bishop_moves, 
                "q": self.get_queen_moves, "k": self.get_king_moves
                }
    
    def get_is_piece_pinned_and_pin_direction(self, r, c):
        is_pinned = False
        pin_direction = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c: 
                is_pinned = True
                if self.board[r][c][0] != "n":
                    pin_direction = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                return is_pinned, pin_direction
        return is_pinned, pin_direction
        
    def is_valid_move(self, x, y):
        return 0 <= x <= 7 and 0 <= y <= 7

    def slidable_pieces(self, r, c, moves, piece, is_pinned, pin_direction):
        start_row = r #to store the start value
        start_col = c #to store the start value
        color = "w" if self.white_to_move else "b" 

        for dx, dy in PIECE_DIRECTIONS[piece]:
            r, c = start_row, start_col #set start value
            while True:
                r += dx
                c += dy
                if not self.is_valid_move(r, c): 
                    break
                if is_pinned:
                    if pin_direction != (dx, dy) and pin_direction != (-dx, -dy):
                        break

                target_square = self.board[r][c]
                if target_square == "--":
                    moves.append(Move((start_row, start_col), (r, c), self.board))
                elif target_square[0] != color:
                    moves.append(Move((start_row, start_col), (r, c), self.board))  # capture
                    break
                else:
                    break  # blocked by same color
    
    def get_rook_moves(self, r, c, moves):
        is_pinned, pin_direction = self.get_is_piece_pinned_and_pin_direction(r, c)   
        self.slidable_pieces(r, c, moves, "r", is_pinned, pin_direction)

    def get_bishop_moves(self, r, c, moves):
        is_pinned, pin_direction = self.get_is_piece_pinned_and_pin_direction(r, c)   
        self.slidable_pieces(r, c, moves, "b", is_pinned, pin_direction)
            
    def get_queen_moves(self, r, c, moves):
        is_pinned, pin_direction = self.get_is_piece_pinned_and_pin_direction(r, c)   
        self.slidable_pieces(r, c, moves, "q", is_pinned, pin_direction)
        
    def get_knight_moves(self, r, c, moves):
        is_pinned, pin_direction = self.get_is_piece_pinned_and_pin_direction(r, c)   
        color = "w" if self.white_to_move else "b"
        for dx, dy in PIECE_DIRECTIONS["n"]:
            new_r, new_c = r + dx, c + dy
            if self.is_valid_move(new_r, new_c) and (not is_pinned or pin_direction == (dx, dy) or pin_direction == (-dx, -dy)):
                target = self.board[new_r][new_c]
                if target == "--" or target[0] != color:
                    moves.append(Move((r, c), (new_r, new_c), self.board))
                    
    def get_king_moves(self, r, c, moves):
        direction = PIECE_DIRECTIONS["k"]
        ally_color = 'w' if self.white_to_move else 'b'
        for i in range(8):
            end_row = r + direction[i][0]
            end_col = c + direction[i][1]
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                end_piece = self.board[end_row][end_col]
                if end_piece[0] != ally_color: #not ally piece (empty or enemy piece
                    # place king on end square and check for checks
                    if ally_color == 'w':
                        self.white_king_location = (end_row, end_col)
                    else:
                        self.black_king_location = (end_row, end_col)
                    in_check, pins, checks = self.check_for_pins_and_checks()
                    if not in_check:
                        moves.append(Move((r, c), (end_row, end_col), self.board))
                    # place king back on original location
                    if ally_color == 'w':
                        self.white_king_location = (r, c)
                    else:
                        self.black_king_location = (r, c)
                        
    def get_pawn_moves(self, r, c, moves):
        is_pinned, pin_direction = self.get_is_piece_pinned_and_pin_direction(r, c)   
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
                    if not is_pinned or pin_direction == (-1, 0):
                        moves.append(Move((r, c), (r-1, c), self.board, gs=self))
                        if r == 6 and self.board[r-2][c] == "--":
                            moves.append(Move((r, c), (r-2, c), self.board, gs=self))
                if c-1 >= 0:
                    if not is_pinned or pin_direction == (-1, -1):
                        if self.board[r-1][c-1][0] == "b" and i_am_white_and_to_move or (self.board[r-1][c-1][0] == "w" and i_am_black_and_to_move):
                            moves.append(Move((r, c), (r-1, c - 1), self.board, gs=self)) 
                            # #print("i can capture with a pawn on left")
                        elif self.possible_en_passant_end_square == (r-1, c-1):
                            if self.board[r][c-1][0] == "w" and i_am_black_and_to_move or self.board[r][c-1][0] == "b" and i_am_white_and_to_move:
                                moves.append(Move((r, c), (r-1, c - 1), self.board, gs=self, is_en_passant_possible=True)) 
                if c+1 <= 7:
                    if not is_pinned or pin_direction == (-1, +1):
                        if self.board[r-1][c+1][0] == "b" and i_am_white_and_to_move or self.board[r-1][c+1][0] == "w" and i_am_black_and_to_move:
                            moves.append(Move((r, c), (r-1, c + 1), self.board, gs=self))
                            # #print("i can capture with a pawn on right")
                        elif self.possible_en_passant_end_square == (r-1, c+1):
                            if self.board[r][c+1][0] == "w" and i_am_black_and_to_move or self.board[r][c+1][0] == "b" and i_am_white_and_to_move:
                                moves.append(Move((r, c), (r-1, c + 1), self.board, gs=self, is_en_passant_possible=True)) 
        #handels enemy/computer moves 
        else:
            if r + 1 <= 7:
                if self.board[r+1][c] == "--":
                    if not is_pinned or pin_direction == (+1, 0):
                        moves.append(Move((r, c), (r+1, c), self.board, gs=self))
                        if r == 1 and self.board[r+2][c] == "--":
                            moves.append(Move((r, c), (r+2, c), self.board, gs=self))
                if c-1 >= 0:
                    if not is_pinned or pin_direction == (+1, -1):
                        if self.board[r+1][c-1][0] == "w" and i_am_white_and_to_wait or self.board[r+1][c-1][0] == "b" and i_am_black_and_to_wait:
                            moves.append(Move((r, c), (r + 1, c - 1), self.board, gs=self))
                            # #print("enemy can capture with a pawn on his right")
                        elif self.possible_en_passant_end_square == (r+1, c-1):
                            if self.board[r][c-1][0] == "w" and i_am_white_and_to_wait or self.board[r][c-1][0] == "b" and i_am_black_and_to_wait:
                                moves.append(Move((r, c), (r+1, c - 1), self.board, gs=self, is_en_passant_possible=True)) 
                if c+1 <= 7:
                    if not is_pinned or pin_direction == (+1, +1):
                        if self.board[r+1][c+1][0] == "w" and i_am_white_and_to_wait or self.board[r+1][c+1][0] == "b" and i_am_black_and_to_wait :
                            moves.append(Move((r, c), (r + 1, c + 1), self.board, gs=self)) 
                            # #print("enemy can capture with a pawn", r,c, "on his left")
                        elif self.possible_en_passant_end_square == (r+1, c+1):
                            if self.board[r][c+1][0] == "w" and i_am_white_and_to_wait or self.board[r][c+1][0] == "b" and i_am_black_and_to_wait:
                                moves.append(Move((r, c), (r+1, c + 1), self.board, gs=self, is_en_passant_possible=True))