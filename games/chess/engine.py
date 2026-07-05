from constants import PIECE_DIRECTIONS
from .move import Move

class Engine:
    
    def check_for_pins_and_checks(self):
        pins = [] #list of tuples, each tuple has length of 4 with 1:row 2:col 3:x_direction, 4:y_direction
        checks = [] #list of tuples, each tuple has length of 4 with 1:row 2:col 3:x_direction, 4:y_direction
        in_check = False
        
        if self.white_to_move:
            enemy_color = "b"
            ally_color = "w"
            start_row_king, start_col_king = self.white_king_location
        else:
            enemy_color = "w"
            ally_color = "b"
            start_row_king, start_col_king = self.black_king_location
                    
        directions = PIECE_DIRECTIONS["k"] #"k": [(0, +1), (+1, 0), (-1, 0), (0, -1), (+1, +1), (+1, -1), (-1, -1), (-1, +1)]
        for direction in range(len(directions)):
            x_direction = directions[direction][0]
            y_direction = directions[direction][1]
            possible_pin = ()
            for amount_of_squares in range(1, 8):
                r = start_row_king + x_direction * amount_of_squares
                c = start_col_king + y_direction * amount_of_squares
                #we need to stay on the board
                
                if 0 <= r <= 7 and 0 <= c <= 7:
                    piece = self.board[r][c]
                    piece_color = piece[0]
                    piece_type = piece[1]
                    # Explanation why we check if this not a king: 
                    # we call this function (check_for_pins_and_checks) as we generate moves for king, 
                    # so that moved king is not staying at check. 
                    # Basically, to generate moves for king, we imitate the king move to the possible square and then check 
                    # if he gets checked (because this should be allowed). 
                    # And, as we check it, the real king position stays. 
                    # So there is a kind of phantom king on the board which blocks the moved king from check                        
                    if piece_color == ally_color and piece_type != "k":
                        if possible_pin == ():
                            possible_pin = (r, c, x_direction, y_direction)
                        else: 
                            break #two pieces on the same line direction meaning no pin is possible
                                    #UPDATE: what if en-passent?
                    elif piece_color == enemy_color:
                        if (0 <= direction <= 3 and piece_type == "r") or \
                            (4 <= direction <= 7 and piece_type == "b") or \
                            piece_type == "q" or \
                            (amount_of_squares == 1 and piece_type == "k") or \
                            (amount_of_squares == 1 and piece_type == "p" and self.validate_pawn_check(directions[direction], enemy_color)):
                            #if there no piece protecting from check 
                            if possible_pin == (): 
                                # print(r,c,"possible check from", piece_color, " piece_type:", piece_type)
                                in_check = True
                                checks.append((r, c, x_direction, y_direction))
                                #then this is check and we stop checking for pins and checks from this direction
                                break 
                            else:
                                pins.append(possible_pin)
                                #there is an enemy piece applying pressure on a possible pinned piece so it is a pinned piece now
                                #and it doesnt matter what else is behind this piece, it is 100% pin, that is why we break
                                break 
                        else: 
                            #if there is a enemy piece and it is not applying any check (if statement above) 
                            # then any piece behind this piece wont apply any pressure 
                            # (except for knight whcih going to be checked later)
                            #that is why we break
                            break 
                else:
                    #off the board
                    break 
        
        #knight check
        for m in PIECE_DIRECTIONS["n"]:
            possible_knight_x = start_row_king + m[0]   
            possible_knight_y = start_col_king + m[1]
            if 0 <= possible_knight_x <= 7 and 0 <= possible_knight_y <= 7:
                piece = self.board[possible_knight_x][possible_knight_y]
                if enemy_color == piece[0] and piece[1] == "n":
                    in_check = True
                    checks.append((possible_knight_x, possible_knight_y, m[0], m[1]))
            
        #print(in_check, checks, pins, sep="\n")
        return in_check, pins, checks

    #find squares that block from check or capture the piece
    def get_valid_moves(self):
        moves = []
        self.in_check, self.pins, self.checks = self.check_for_pins_and_checks()
        
        if self.white_to_move:
            king_row, king_col = self.white_king_location
        else:
            king_row, king_col = self.black_king_location
        
        if self.in_check:
            if len(self.checks) == 1: #only one means we can either move king, block with another piece, take the attacking piece
                moves = self.get_all_possible_moves()
                check_info = self.checks[0]
                piece_checks_row = check_info[0]
                piece_checks_col = check_info[1]
                piece_checking = self.board[piece_checks_row][piece_checks_col]
                valid_squares = [] #in other words blocking_from_check_or_capturing_squares
                #if the moving piece is knight, the only valid squares for all our pieces (except for king) is capturing the knight
                #(checking if the moved piece was king or not follows later in the code)
                #(firstly we just search for squares that would block the check or capture the piece)
                if piece_checking[1] == "n":
                    valid_squares = [(piece_checks_row, piece_checks_col)]
                else:
                    for i in range(1, 8):
                        #squares that would block the check
                        valid_square = (king_row + check_info[2] * i, king_col + check_info[3] * i)
                        valid_squares.append(valid_square)
                        #as we get to the enemy piece position that checks our king 
                        # (we have already added move capturing the piece 
                        #   (in other words moving our piece to the postion of piece that checks), 
                        # because we do it beforehand)
                        #we can stop, because blocking means placing a piece between the king and attacking piece (or on attacking piece)
                        if valid_square[0] == piece_checks_row and valid_square[1] == piece_checks_col:
                            break
                for i in range(len(moves) - 1, -1, -1):
                    #if we move the piece and it is not a king (when it is check)
                    if moves[i].moved_piece[1] != "k":
                        #then it is suppoused to be the square that is blocking the check or capturing the piece 
                        #(that is why for knight valid square is a square where khingt is)
                        #which are stored in valid squares
                        if (moves[i].end_row, moves[i].end_col) not in valid_squares:
                            moves.remove(moves[i])
            else: 
                #if there is a double check, only way to get out is to move king
                # print("this is a double check, only move is to move king")
                self.get_king_moves(king_row, king_col, moves)
        else: 
            #no check, all moves are valid except for pins
            moves = self.get_all_possible_moves()
            if self.white_to_move:
                self.get_castle_moves(self.white_king_location, moves)
            else:
                self.get_castle_moves(self.black_king_location, moves)
            
        #what about king move, that ends up in check?
        if len(moves) == 0:
            if self.in_check:
                self.checkmate = True
                # if self.white_to_move:
                #     print("white in checkmate")
                # else:
                #     print("black in checkmate")
            else:
                self.stalemate = True
                print("stalemate")
        else:
            self.checkmate = False
            self.stalemate = False
    
        return moves                
    
    def get_all_possible_moves(self):
        moves = []
        for r in range(8):
            for c in range(8):
                color = self.board[r][c][0]
                if (color == "w" and self.white_to_move) or (color == "b" and not self.white_to_move):
                    piece = self.board[r][c][1]
                    self.move_functions[piece](r, c, moves)
        return moves
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