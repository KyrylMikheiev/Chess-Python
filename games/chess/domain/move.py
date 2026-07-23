"""Move -- a dumb, immutable value object.

Design decisions vs the old Move:
  - No reference to GameState/Position. A move is just data: from, to, flags.
    (Promotion detection is a RULE -> it belongs in movegen/variant, and the
    chosen promotion piece is stored here as a plain field once decided.)
  - Frozen dataclass -> free __eq__/__hash__, safe to put in sets/dicts, and
    it can never mutate underneath the AI search.
  - __eq__ comes from the dataclass and returns False for non-Move objects
    (the old __eq__ raised an exception -- that was a bug for `in`/tests).
"""
from __future__ import annotations

from dataclasses import dataclass

from games.chess.domain.enums import PieceType, Square


@dataclass(frozen=True)
class Move:
    frm: Square
    to: Square
    is_en_passant: bool = False
    is_castle: bool = False
    promotion: PieceType | None = None  # set when the move is a pawn promotion

    # TODO (optional): a human-readable / uci-style id for logging & highlight,
    # e.g. derived from frm/to. Keep it derived, don't let callers set state.
