"""Position -- the complete board state at one instant. A value, not a machine.

Design decisions vs the old GameState:
  - ABSOLUTE coordinates only. No WHITE_BOARD/BLACK_BOARD, no is_players_color.
    row 0 = white back rank, always. The UI flips for display, not the model.
  - Holds ONLY state, no move-generation or check logic (that's movegen.py).
  - Treat it as immutable: `apply(position, move)` in movegen returns a NEW
    Position. This kills undo_move entirely -- the AI just keeps old references.
    (If you ever profile and need in-place make/undo, hide it behind movegen's
    apply() so callers never see the difference.)

`board` is an 8x8 grid of Optional[(Color, PieceType)] -- None means empty.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from games.chess.domain.enums import Color, PieceType, Square

Piece = tuple[Color, PieceType]
Board = list[list[Piece | None]]


@dataclass(frozen=True)
class CastleRights:
    white_king_side: bool = True
    white_queen_side: bool = True
    black_king_side: bool = True
    black_queen_side: bool = True


@dataclass(frozen=True)
class Position:
    board: Board
    side_to_move: Color
    castle_rights: CastleRights = CastleRights()
    en_passant_target: Square | None = None
    # King squares cached for fast check detection (derive/update in apply()).
    white_king: Square = (0, 4)
    black_king: Square = (7, 4)

    def piece_at(self, square: Square) -> Piece | None:
        r, c = square
        return self.board[r][c]

    @staticmethod
    def in_bounds(square: Square) -> bool:
        r, c = square
        return 0 <= r <= 7 and 0 <= c <= 7

    # TODO: a copy helper for apply() (deep-copy the board rows) if you keep the
    # immutable model, or a classmethod to build the standard start position.
    # Note: standard start position belongs to the Variant (rules/classical.py),
    # not here -- Chess960 randomizes it.
