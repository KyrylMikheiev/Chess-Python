from .castle_rights import CastleRights
from constants import WHITE_BOARD, BLACK_BOARD

class GameState:
    
    def __init__(self, white_pieces):
        
        self.is_players_color_white = white_pieces
        self.white_to_move = True
        self.in_check = False
        self.pins = []
        self.checks = []
        self.checkmate = False
        self.stalemate = False
                
        if self.is_players_color_white:
            self.player_to_move = True
            self.board = [row[:] for row in WHITE_BOARD]
            self.white_king_location = (7, 4)
            self.black_king_location  = (0, 4)
        else:
            self.player_to_move = False
            self.board = [row[:] for row in BLACK_BOARD]
            self.white_king_location = (0, 4)
            self.black_king_location = (7, 4)
        self.move_log = []
        self.move_functions = {
                                "p": self.get_pawn_moves, "r": self.get_rook_moves, 
                                "n": self.get_knight_moves, "b": self.get_bishop_moves, 
                                "q": self.get_queen_moves, "k": self.get_king_moves
                                }
        self.possible_en_passant_end_square = () #cordinates of where piece ends up landing after en passant
        self.current_castle_rights = CastleRights(True, True, True, True)
        self.castle_rights_log = [CastleRights(self.current_castle_rights.wks, self.current_castle_rights.wqs, 
                                                self.current_castle_rights.bks, self.current_castle_rights.bqs)]
        

    def get_players_color(self):
        return self.is_players_color_white

    def make_move(self, move: "Move"):
        self.board[move.start_row][move.start_col] = "--"
        if move.is_pawn_promoting:
            # # if you want to take the piece u want, uncomment this section
            # if self.player_to_move:
            #     print("Type a letter of a piece you want to choose")
            #     piece = input()
            #     piece = piece.lower().strip() 
            #     if piece in ["r", "n", "b", "q"]:
            #         self.board[move.end_row][move.end_col] = move.moved_piece[0] + piece
            #     else:
            #         print("This piece is not allowed to be chosen")
            #         self.make_move(move)
            # #engine always takes queen for now
            # else: 
            #     self.board[move.end_row][move.end_col] = move.moved_piece[0] + "q"
            self.board[move.end_row][move.end_col] = move.moved_piece[0] + "q"
        else:
            self.board[move.end_row][move.end_col] = move.moved_piece
        self.move_log.append(move)
        
        # king positions
        if move.moved_piece == "wk":
            self.white_king_location = (move.end_row, move.end_col)
        elif move.moved_piece == "bk":
            self.black_king_location = (move.end_row, move.end_col)
        
        #en passant
        if move.en_passant:
            self.board[move.start_row][move.end_col] = "--" #capturing the pawn
        if move.moved_piece[1] == "p" and abs(move.start_row - move.end_row) == 2:
            self.possible_en_passant_end_square = ((move.start_row + move.end_row)//2, move.end_col)
        else:
            self.possible_en_passant_end_square = ()     
            
        #castle moves
        if move.is_castle_move:
            if self.is_players_color_white:
                if move.end_col - move.start_col == 2:
                    self.board[move.end_row][move.end_col - 1] = self.board[move.end_row][move.end_col + 1]
                    self.board[move.end_row][move.end_col + 1] = "--"
                elif move.end_col - move.start_col == -2:    
                    self.board[move.end_row][move.end_col + 1] = self.board[move.end_row][move.end_col - 2]
                    self.board[move.end_row][move.end_col - 2] = "--"
            else: #i play with black
                if move.end_col - move.start_col == -2:
                    self.board[move.end_row][move.end_col + 1] = self.board[move.end_row][move.end_col - 1]
                    self.board[move.end_row][move.end_col - 1] = "--"
                elif move.end_col - move.start_col == 2:    
                    self.board[move.end_row][move.end_col - 1] = self.board[move.end_row][move.end_col + 2]
                    self.board[move.end_row][move.end_col + 2] = "--"
                
        self.castle_rights_log.append(CastleRights(self.current_castle_rights.wks, self.current_castle_rights.wqs, self.current_castle_rights.bks, self.current_castle_rights.bqs))
        self.update_castle_rights(move)  

        self.player_to_move = not self.player_to_move
        self.white_to_move = not self.white_to_move
        
    def undo_move(self):
        if len(self.move_log) != 0:
            move = self.move_log.pop()
            self.board[move.start_row][move.start_col] = move.moved_piece
            self.board[move.end_row][move.end_col] = move.captured_piece_or_empty
            self.player_to_move = not self.player_to_move
            self.white_to_move = not self.white_to_move
            if move.moved_piece == "wk": #check the move log and if no other king moves, then set to false.
                self.white_king_location = (move.start_row, move.start_col)
            elif move.moved_piece == "bk":
                self.black_king_location = (move.start_row, move.start_col)
            if move.en_passant:
                self.board[move.end_row][move.end_col] = "--"
                self.board[move.start_row][move.end_col] = "bp" if self.white_to_move else "wp"
                self.possible_en_passant_end_square = (move.end_row, move.end_col)
            if move.moved_piece[1] == "p" and abs(move.start_row - move.end_row) == 2:   #sure start row and end row?
                self.possible_en_passant_end_square = ()
                
            if move.is_castle_move:
                if self.is_players_color_white:
                    if move.end_col - move.start_col == 2:
                        self.board[move.end_row][move.end_col + 1] = self.board[move.end_row][move.end_col - 1]
                        self.board[move.end_row][move.end_col - 1] = "--"
                    elif move.end_col - move.start_col == -2:    
                        self.board[move.end_row][move.end_col - 2] = self.board[move.end_row][move.end_col + 1]
                        self.board[move.end_row][move.end_col + 1] = "--"
                else: #i play with black
                    if move.end_col - move.start_col == -2:
                        self.board[move.end_row][move.end_col - 1] = self.board[move.end_row][move.end_col + 1]
                        self.board[move.end_row][move.end_col + 1] = "--"
                    elif move.end_col - move.start_col == 2:    
                        self.board[move.end_row][move.end_col + 2] = self.board[move.end_row][move.end_col - 1]
                        self.board[move.end_row][move.end_col - 1] = "--"
            
            self.castle_rights_log.pop()
            self.current_castle_rights = self.castle_rights_log[-1]
            self.checkmate = False
            self.stalemate = False
        else: 
            print("Starting postion")
