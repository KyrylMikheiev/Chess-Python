"""Negamax + alpha-beta search. Port from ai.py (findMoveNegaMaxAlphaBeta).

Changes from the old version:
  - Works against the pure domain: use movegen.legal_moves(position, variant)
    and movegen.apply(position, move) instead of gs.get_valid_moves/make_move/
    undo_move. With an immutable Position there is NO undo -- recursion just
    passes the new position down. This removes a whole class of undo bugs.
  - scoreBoard moves to evaluation.py and is imported here.
  - The transposition cache keys on a hashable Position (frozen dataclass) or a
    derived key -- not str(board) as before.
"""
from __future__ import annotations

from games.chess.domain.move import Move
from games.chess.domain.position import Position

DEPTH = 4
CHECKMATE = 1000
STALEMATE = 0


def find_best_move(position: Position, variant, return_queue=None) -> Move | None:
    """Entry point run in the AIPlayer's process. Port find_best_move here."""
    # TODO: negamax alpha-beta over movegen.legal_moves / movegen.apply
    raise NotImplementedError


def find_random_move(legal_moves: list[Move]) -> Move:
    # TODO: random.choice fallback (as in ai.find_random_move)
    raise NotImplementedError
