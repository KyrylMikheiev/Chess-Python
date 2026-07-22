"""Piece movement described as DATA, not as methods on a god-object.

The old code had get_rook_moves/get_bishop_moves/... as methods sharing `self`
with the board. Here, movement is a table that movegen.py reads. A Variant can
swap this table to add fairy pieces or change behavior -- a data change, not a
new subclass.

Two movement archetypes cover the standard pieces:
  - SLIDERS: repeat a direction until blocked (rook, bishop, queen)
  - LEAPERS: single jump to fixed offsets (knight, king one-step)
Pawns and castling are special-cased in movegen (they depend on state/rules).
"""
from __future__ import annotations

from games.chess.domain.enums import PieceType

# Direction/offset vectors as (d_row, d_col).
_ORTHOGONAL = [(0, 1), (0, -1), (1, 0), (-1, 0)]
_DIAGONAL = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

# Pieces that slide along directions until blocked.
SLIDERS: dict[PieceType, list[tuple[int, int]]] = {
    PieceType.ROOK: _ORTHOGONAL,
    PieceType.BISHOP: _DIAGONAL,
    PieceType.QUEEN: _ORTHOGONAL + _DIAGONAL,
}

# Pieces that leap to fixed offsets (single step).
LEAPERS: dict[PieceType, list[tuple[int, int]]] = {
    PieceType.KNIGHT: [(2, 1), (2, -1), (-2, 1), (-2, -1),
                       (1, 2), (1, -2), (-1, 2), (-1, -2)],
    PieceType.KING: _ORTHOGONAL + _DIAGONAL,
}

# TODO: port your PIECE_DIRECTIONS values into the tables above and delete the
# constant from constants.py once movegen reads from here.
