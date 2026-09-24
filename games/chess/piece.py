from typing import Protocol

from games.chess.move import Move

class Piece(Protocol):
    
    def get_moves(self) -> list[Move]:
        pass
    
    #get bitboard 
    def get_positions(self):
        pass
    