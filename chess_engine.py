from utils import PIECE_DIRECTIONS, WHITE_BOARD, BLACK_BOARD

class GameState:
    
    def __init__(self, white_pieces):
        
        self.is_players_color_white = white_pieces
        self.white_to_move = True
        self.white_king_moved = False
        self.black_king_moved = False
        self.inCheck = False
        self.pins = []
        self.checks = []
        
        if self.is_players_color_white:
            self.player_to_move = True
            self.board = WHITE_BOARD
            self.white_king_location = (7, 4)
            self.black_king_location  = (0, 4)
        else:
            self.player_to_move = False
            self.board = BLACK_BOARD
            self.white_king_location = (0, 4)
            self.black_king_location = (7, 4)
        self.move_log = []
        self.move_functions = {
                                "p": self.get_pawn_moves, "r": self.get_rook_moves, 
                                "n": self.get_knight_moves, "b": self.get_bishop_moves, 
                                "q": self.get_queen_moves, "k": self.get_king_moves
                               }
        
    def make_move(self, move):
        self.board[move.start_row][move.start_col] = "--"
        self.board[move.end_row][move.end_col] = move.moved_piece
        self.move_log.append(move)
        self.player_to_move = not self.player_to_move
        self.white_to_move = not self.white_to_move
        if move.moved_piece == "wk":
            self.white_king_moved = True
            self.white_king_location = (move.end_row, move.end_col)
        elif move.moved_piece == "bk":
            self.black_king_moved = True
            self.black_king_location = (move.end_row, move.end_col)
        
    def undo_move(self):
        if len(self.move_log) != 0:
            move = self.move_log.pop()
            self.board[move.start_row][move.start_col] = move.moved_piece
            self.board[move.end_row][move.end_col] = move.captured_piece_or_empty
            self.player_to_move = not self.player_to_move
            self.white_to_move = not self.white_to_move
            if move.moved_piece == "wk": #check the move log and if no other king moves, then set to false.
                self.white_king_moved = False
                self.white_king_location = (move.start_row, move.start_col)
            elif move.moved_piece == "bk":
                self.black_king_moved = False
                self.black_king_location = (move.start_row, move.start_col)
            
        else: 
            print("Starting postion")
            
    # def check_for_pins_and_checks(self):
    #     pins = []
    #     checks = []
    #     inCheck = False
        
    #     if self.white_to_move:
    #         enemy_color = "b"
    #         ally_color = "w"
    #         start_row_king = self.white_king_location[0]
    #         start_col_king = self.white_king_location[1]
    #     else:
    #         enemy_color = "w"
    #         ally_color = "b"
    #         start_row_king = self.black_king_location[0]
    #         start_col_king = self.black_king_location[1]
        
    #     directions = PIECE_DIRECTIONS["k"] #"k": [(0, +1), (+1, 0), (-1, 0), (0, -1), (+1, +1), (-1, -1), (+1, -1), (-1, +1)]

    #     for direction in range(len(directions)):
    #         x_direction = direction[0]
    #         y_direction = direction[1]
    #         possible_pin = ()
    #         for  in range(1, 8):
    #             r = start_row_king + x_direction * i
    #             c = start_col_king + y_direction * i
    #             if 1 <= r <= 7 and 1 <= c <= 7:
    #                 piece = self.board[r][c]
    #                 piece_color = piece[0]
    #                 piece_type = piece[1]
    #                 if piece_color == ally_color:
    #                     if possible_pin == ():
    #                         possible_pin = (r, c, x_direction, y_direction)
    #                     else: 
    #                         break
    #                 elif piece_color == enemy_color:
    #                     if (0 <= direction <= 3 and piece_type == "r") or \
    #                         (4 <= direction <= 7 and piece_type == "b") or \
    #                         piece_type == "q" or \
    #                         (i )
    #                         if possible_pin != ():
    #                             inCheck = True
    #                             checks.append((r, c, x_direction, y_direction))
    #                         else:
    #                             pins.append((r, c, x_direction, y_direction))
    #             else:
    #                 break
            
    def get_valid_moves(self):
        return self.get_all_possible_moves()
    
    def get_all_possible_moves(self):
        moves = []
        for r in range(8):
            for c in range(8):
                color = self.board[r][c][0]
                if (color == "w" and self.white_to_move) or (color == "b" and not self.white_to_move):
                    piece = self.board[r][c][1]
                    self.move_functions[piece](r, c, moves)
        return moves

    def is_valid_move(self, x, y):
        return 0 <= x <= 7 and 0 <= y <= 7
    
    def single_step_moves(self, r, c, moves, piece):
        color = "w" if self.white_to_move else "b"
        for dx, dy in PIECE_DIRECTIONS[piece]:
            new_r, new_c = r + dx, c + dy
            if self.is_valid_move(new_r, new_c):
                target = self.board[new_r][new_c]
                if target == "--" or target[0] != color:
                    moves.append(Move((r, c), (new_r, new_c), self.board))
    
    def slidable_pieces(self, r, c, moves, piece):
        start_row = r
        start_col = c
        color = "w" if self.white_to_move else "b" 

        for dx, dy in PIECE_DIRECTIONS[piece]:
            r, c = start_row, start_col
            while True:
                r += dx
                c += dy
                if not self.is_valid_move(r, c):
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
        self.slidable_pieces(r, c, moves, "r")    

    def get_bishop_moves(self, r, c, moves):
        self.slidable_pieces(r, c, moves, "b")
            
    def get_queen_moves(self, r, c, moves):
        self.slidable_pieces(r, c, moves, "q")
        
    def get_knight_moves(self, r, c, moves):
        self.single_step_moves(r, c, moves, "n")
        
    def get_king_moves(self, r, c, moves):
        self.single_step_moves(r, c, moves, "k")
                    
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
                        # print("i can capture with a pawn on left")
                if c+1 <= 7:
                    if self.board[r-1][c+1][0] == "b" and i_am_white_and_to_move or self.board[r-1][c+1][0] == "w" and i_am_black_and_to_move:
                        moves.append(Move((r, c), (r-1, c + 1), self.board))
                        # print("i can capture with a pawn on right")
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
                        # print("enemy can capture with a pawn on his right")
                if c+1 <= 7:
                    if self.board[r+1][c+1][0] == "w" and i_am_white_and_to_wait or self.board[r+1][c+1][0] == "b" and i_am_black_and_to_wait :
                        moves.append(Move((r, c), (r + 1, c + 1), self.board)) 
                        # print("enemy can capture with a pawn on his left")
    
        
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
        raise Exception("Not the same")
    
    
        