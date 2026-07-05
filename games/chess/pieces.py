class Pieces:
    
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