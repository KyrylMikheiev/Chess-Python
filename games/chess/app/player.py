"""Player abstraction -- collapses the old handle_human_move / handle_ai_move
split into one uniform concept: "when asked, produce a move (eventually)".

The Session asks the current player for a move each step. A HumanPlayer is fed
by clicks from the UI; an AIPlayer runs the search (in a process) and reports
when ready. Both look the same to the Session.

Port from: controller.py (the two move-handling paths + the multiprocessing).
"""
from __future__ import annotations

from typing import Protocol

from games.chess.domain.move import Move
from games.chess.domain.position import Position


class Player(Protocol):
    def request_move(self, position: Position, legal_moves: list[Move]) -> Move | None:
        """Return a chosen move, or None if not ready yet (async AI / awaiting
        human input). The Session polls until a move is returned."""
        ...


class HumanPlayer:
    """Move comes from UI input. The scene calls submit() with the clicked move."""

    def __init__(self) -> None:
        self._pending: Move | None = None

    def submit(self, move: Move) -> None:
        self._pending = move

    def request_move(self, position: Position, legal_moves: list[Move]) -> Move | None:
        move, self._pending = self._pending, None
        return move


class AIPlayer:
    """Wraps the negamax search in a background process (from controller.py)."""

    def __init__(self) -> None:
        # TODO: hold the Process/Queue state that Controller.handle_ai_move had
        self._thinking = False

    def request_move(self, position: Position, legal_moves: list[Move]) -> Move | None:
        # TODO: start ai.search in a Process if idle; when it finishes, return
        # the move; otherwise return None (still thinking). Encapsulate ALL the
        # multiprocessing here so the Session stays simple.
        raise NotImplementedError
