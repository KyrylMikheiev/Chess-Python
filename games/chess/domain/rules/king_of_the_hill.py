"""King of the Hill -- same board & pieces as classical, different win condition.

Demonstrates a variant that changes ONLY result(): you also win by getting your
king to one of the four center squares (3,3)/(3,4)/(4,3)/(4,4). Start position
and movement are identical to classical, so delegate those.

This is the cleanest proof that the Variant seam works: one method overridden.
"""
from __future__ import annotations

from games.chess.domain.enums import GameResult
from games.chess.domain.move import Move
from games.chess.domain.position import Position
from games.chess.domain.rules.classical import ClassicalChess

_CENTER = {(3, 3), (3, 4), (4, 3), (4, 4)}


class KingOfTheHill:
    name = "King of the Hill"

    def __init__(self) -> None:
        self._classical = ClassicalChess()

    def initial_position(self) -> Position:
        return self._classical.initial_position()

    def result(self, position: Position, legal_moves: list[Move]) -> GameResult:
        # TODO: if a king already reached a center square -> that side wins;
        #       otherwise fall back to classical checkmate/stalemate.
        return self._classical.result(position, legal_moves)

    def adjust_moves(self, position: Position, moves: list[Move]) -> list[Move]:
        return moves
