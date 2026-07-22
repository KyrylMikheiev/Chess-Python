"""The Variant interface (Strategy pattern).

movegen and the app layer talk to a Variant through this Protocol only, so a
new variant is a new implementation -- no edits to shared code.

Keep the surface small: only the things variants actually differ on.
  - initial_position(): Chess960 randomizes the back rank; others are fixed.
  - result(): King of the Hill / Atomic change how the game ends.
  - adjust_moves(): hook for variants that add/remove moves (default = identity).
Piece movement is shared (movegen + pieces tables); expose a hook here only if a
variant genuinely changes how a piece moves.
"""
from __future__ import annotations

from typing import Protocol

from games.chess.domain.enums import GameResult
from games.chess.domain.move import Move
from games.chess.domain.position import Position


class Variant(Protocol):
    name: str

    def initial_position(self) -> Position:
        """The starting position for a new game of this variant."""
        ...

    def result(self, position: Position, legal_moves: list[Move]) -> GameResult:
        """Game over? Classical: checkmate/stalemate. Others override this."""
        ...

    def adjust_moves(self, position: Position, moves: list[Move]) -> list[Move]:
        """Optional hook to add/remove moves. Default impls just return `moves`."""
        ...
