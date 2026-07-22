"""Core domain vocabulary as real types instead of magic strings.

This replaces the stringly-typed "w"/"b"/"wp" scattered through the old code.
Enums make illegal states unrepresentable and give you the strict typing you
wanted -- pyright/mypy can now catch a swapped color at author time.

Coordinates are ABSOLUTE: row 0 is always white's back rank, row 7 black's.
Board orientation for display is a UI concern (renderer flips), never stored here.
"""
from __future__ import annotations

from enum import Enum


class Color(Enum):
    WHITE = "w"
    BLACK = "b"

    @property
    def opponent(self) -> "Color":
        return Color.BLACK if self is Color.WHITE else Color.WHITE


class PieceType(Enum):
    PAWN = "p"
    KNIGHT = "n"
    BISHOP = "b"
    ROOK = "r"
    QUEEN = "q"
    KING = "k"


# A square is (row, col), both 0..7, absolute coordinates.
Square = tuple[int, int]


class GameResult(Enum):
    ONGOING = "ongoing"
    WHITE_WINS = "white_wins"
    BLACK_WINS = "black_wins"
    DRAW = "draw"
