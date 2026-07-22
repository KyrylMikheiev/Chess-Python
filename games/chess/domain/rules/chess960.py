"""Chess960 (Fischer Random).

Only two things differ from Classical:
  - initial_position(): shuffled back rank (960 legal arrangements), mirrored
    for both colors. King between the rooks; bishops on opposite colors.
  - castling: generalized to the piece's start files (handle in movegen/apply
    once you generalize castling away from hard-coded columns).

Everything else -- delegate to / reuse ClassicalChess.
"""
from __future__ import annotations

from games.chess.domain.enums import GameResult
from games.chess.domain.move import Move
from games.chess.domain.position import Position
from games.chess.domain.rules.classical import ClassicalChess


class Chess960:
    name = "Chess960"

    def __init__(self) -> None:
        self._classical = ClassicalChess()

    def initial_position(self) -> Position:
        # TODO: generate a random legal 960 back-rank arrangement (absolute coords)
        raise NotImplementedError

    def result(self, position: Position, legal_moves: list[Move]) -> GameResult:
        return self._classical.result(position, legal_moves)

    def adjust_moves(self, position: Position, moves: list[Move]) -> list[Move]:
        return moves
