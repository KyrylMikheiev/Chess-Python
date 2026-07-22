"""Session -- the turn-based game driver. The reborn Controller.

Owns the mutable "current game" state that the domain (pure values) does not:
the current Position, the move history, which Player is on turn. Each step it
asks the current player for a move, applies it via the domain, recomputes legal
moves, and checks the variant's result.

This is the ONE place that assumes players alternate. A future
realtime_session.py (Kung Fu) reuses the same domain calls without this
alternation -- that's why the turn logic is here and not in the domain.

Port from: controller.py (update/handle_*_move/undo_move/game-over flags).
"""
from __future__ import annotations

from games.chess.app.player import Player
from games.chess.domain import movegen
from games.chess.domain.enums import Color, GameResult
from games.chess.domain.move import Move
from games.chess.domain.position import Position
from games.chess.domain.rules.variant import Variant


class Session:
    def __init__(self, variant: Variant, white: Player, black: Player) -> None:
        self.variant = variant
        self.players: dict[Color, Player] = {Color.WHITE: white, Color.BLACK: black}
        self.position: Position = variant.initial_position()
        self.history: list[Position] = [self.position]
        self.legal_moves: list[Move] = movegen.legal_moves(self.position, variant)
        self.result: GameResult = GameResult.ONGOING

    def current_player(self) -> Player:
        return self.players[self.position.side_to_move]

    def step(self) -> None:
        """Advance one tick: ask the player on turn; apply if a move is ready."""
        if self.result is not GameResult.ONGOING:
            return
        move = self.current_player().request_move(self.position, self.legal_moves)
        if move is None:
            return  # human hasn't clicked / AI still thinking
        self._apply(move)

    def _apply(self, move: Move) -> None:
        # TODO: validate move is in self.legal_moves, then:
        self.position = movegen.apply(self.position, move)
        self.history.append(self.position)
        self.legal_moves = movegen.legal_moves(self.position, self.variant)
        self.result = self.variant.result(self.position, self.legal_moves)

    def undo(self) -> None:
        # TODO: pop history back one (or two, to skip the AI reply) and recompute
        # legal_moves. Immutable history makes this trivial -- no inverse logic.
        raise NotImplementedError
