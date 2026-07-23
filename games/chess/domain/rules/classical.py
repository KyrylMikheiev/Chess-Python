"""Classical chess -- the default Variant and the baseline all others reuse.

Implements the Variant Protocol from variant.py.
Port the standard start position (from constants WHITE_BOARD, but in ABSOLUTE
orientation now) and the checkmate/stalemate logic (from engine.get_valid_moves'
end-of-game section) into here.
"""
from __future__ import annotations

from games.chess.domain.enums import GameResult
from games.chess.domain.move import Move
from games.chess.domain.position import Position


class ClassicalChess:
    name = "Classical"

    def initial_position(self) -> Position:
        # TODO: build the standard start position in absolute coords
        raise NotImplementedError

    def result(self, position: Position, legal_moves: list[Move]) -> GameResult:
        # TODO: no legal moves -> checkmate (loser = side_to_move) or stalemate
        raise NotImplementedError

    def adjust_moves(self, position: Position, moves: list[Move]) -> list[Move]:
        return moves
