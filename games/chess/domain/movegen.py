"""Move generation and application -- PURE. No mutation, no side effects.

This is the untangling of the old Engine + Pieces + GameState `self`-sharing
mess. Instead of methods that mutate the board to test king safety, these are
functions that take a Position and return data / a new Position.

Port the logic from:
  - engine.py  : check_for_pins_and_checks, get_valid_moves, get_all_possible_moves
  - pieces.py  : the per-piece generation (now driven by pieces.SLIDERS/LEAPERS)
  - game_state.py: make_move body -> apply() below (as a pure transform)

Key change from the old design: king-safety is tested by generating the
resulting Position and asking `is_square_attacked(king)` on it -- NOT by
temporarily mutating king_location in place.
"""
from __future__ import annotations

from games.chess.domain.enums import Color, Square
from games.chess.domain.move import Move
from games.chess.domain.position import Position


def pseudo_legal_moves(position: Position, color: Color) -> list[Move]:
    """All moves ignoring king-safety (pins/checks). Reads pieces.* tables."""
    # TODO: port sliders/leapers/pawn generation from pieces.py, using
    # absolute coords (no is_players_color branching).
    raise NotImplementedError


def is_square_attacked(position: Position, square: Square, by: Color) -> bool:
    """Is `square` attacked by any `by`-colored piece? Basis of check logic."""
    # TODO: derive from check_for_pins_and_checks in engine.py, made stateless.
    raise NotImplementedError


def apply(position: Position, move: Move) -> Position:
    """Return the NEW position after `move`. Never mutates `position`.

    Handles capture, promotion, en passant, castling rook move, castle-rights
    update, en-passant target, king-square cache, and flipping side_to_move.
    Port the body of game_state.make_move here as a pure transform.
    """
    # TODO
    raise NotImplementedError


def legal_moves(position: Position, variant) -> list[Move]:
    """Pseudo-legal moves filtered so the mover's king is not left in check,
    plus variant-specific special moves (castling, etc.).

    `variant` is a rules.variant.Variant; it may add/remove/adjust moves.
    Port get_valid_moves from engine.py here.
    """
    # TODO
    raise NotImplementedError
