from utils import PIECE_DIRECTIONS, WHITE_BOARD, BLACK_BOARD

class GameState:
    
    def __init__(self, white_pieces):
        
        self.is_players_color_white = white_pieces
        self.white_to_move = True
        self.white_king_moved = False
        self.black_king_moved = False
        self.in_check = False
        self.pins = []
        self.checks = []
        self.checkmate = False
        self.stalemate = False
        
        
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
    
    def validate_pawn_check(self, direction, enemy_color):
        players_pawns_directions = ((-1, -1), (-1, +1))
        enemys_pawns_directions = ((+1, -1), (+1, +1))
        if self.is_players_color_white and enemy_color == "w" or not self.is_players_color_white and enemy_color == "b":
            return direction in enemys_pawns_directions
        else:
            return direction in players_pawns_directions
            
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
                    if piece_color == ally_color and piece_type != "k": # Explanation why we check if this not a king: we call this function (check_for_pins_and_checks) as we generate moves for king, so that moved king is not staying at check. Basically, to generate moves for king, we imitate the king move to the possible square and then check if he gets checked (because this should be allowed). And, as we check it, the real king position stays. So there is a kind of phantom king on the board which blocks the moved king from check
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
                print("check")
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
                print("this is a double check, only move is to move king")
                self.get_king_moves(king_row, king_col, moves)
        else: 
            #no check, all moves are valid except for pins
            moves = self.get_all_possible_moves()
            
        #what about king move, that ends up in check?
        if len(moves) == 0:
            if self.in_check:
                self.checkmate = True
                print("checkmate")
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
                        moves.append(Move((r, c), (r-1, c), self.board))
                        if r == 6 and self.board[r-2][c] == "--":
                            moves.append(Move((r, c), (r-2, c), self.board))
                if c-1 >= 0:
                    if not is_pinned or pin_direction == (-1, -1):
                        if self.board[r-1][c-1][0] == "b" and i_am_white_and_to_move or (self.board[r-1][c-1][0] == "w" and i_am_black_and_to_move):
                            moves.append(Move((r, c), (r-1, c - 1), self.board)) 
                            # #print("i can capture with a pawn on left")
                if c+1 <= 7:
                    if not is_pinned or pin_direction == (-1, +1):
                        if self.board[r-1][c+1][0] == "b" and i_am_white_and_to_move or self.board[r-1][c+1][0] == "w" and i_am_black_and_to_move:
                            moves.append(Move((r, c), (r-1, c + 1), self.board))
                            # #print("i can capture with a pawn on right")
        #handels enemy/computer moves 
        else:
            if r + 1 <= 7:
                if self.board[r+1][c] == "--":
                    if not is_pinned or pin_direction == (+1, 0):
                        moves.append(Move((r, c), (r+1, c), self.board))
                        if r == 1 and self.board[r+2][c] == "--":
                            moves.append(Move((r, c), (r+2, c), self.board))
                if c-1 >= 0:
                    if not is_pinned or pin_direction == (+1, -1):
                        if self.board[r+1][c-1][0] == "w" and i_am_white_and_to_wait or self.board[r+1][c-1][0] == "b" and i_am_black_and_to_wait:
                            moves.append(Move((r, c), (r + 1, c - 1), self.board))
                            # #print("enemy can capture with a pawn on his right")
                if c+1 <= 7:
                    if not is_pinned or pin_direction == (+1, +1):
                        if self.board[r+1][c+1][0] == "w" and i_am_white_and_to_wait or self.board[r+1][c+1][0] == "b" and i_am_black_and_to_wait :
                            moves.append(Move((r, c), (r + 1, c + 1), self.board)) 
                            # #print("enemy can capture with a pawn on his left")
        
class Move:
    
    def __init__(self, start_pos, end_pos, board):
        self.start_row = start_pos[0]
        self.start_col = start_pos[1]
        self.end_row = end_pos[0]
        self.end_col = end_pos[1]
        
        self.moved_piece = board[self.start_row][self.start_col]
        self.captured_piece_or_empty = board[self.end_row][self.end_col]
        
        self.moveID = self.start_row * 1000 + self.start_col * 100 + self.end_row * 10 + self.end_col
        
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        raise Exception("Not the same")
    
    
        