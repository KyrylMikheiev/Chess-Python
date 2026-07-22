"""Static position evaluation. Port from ai.py (scoreBoard + the piece tables).

Positive = good for White, negative = good for Black (keep the old convention).

Future note: evaluation can become variant-specific (King of the Hill values the
center more). If that happens, let a Variant supply an evaluator, or add a hook.
Not now -- keep one classical evaluator until a variant actually needs its own.
"""
from __future__ import annotations

from games.chess.domain.position import Position

# TODO: port pieceScore + knightScores/bishopScores/... piece-square tables,
# converted to absolute orientation / the (Color, PieceType) representation.


def score_board(position: Position) -> float:
    """Material + piece-square score for `position`. Port scoreBoard()."""
    # TODO
    raise NotImplementedError
