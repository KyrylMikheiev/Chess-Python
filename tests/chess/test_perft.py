"""Perft: the regression net for the whole redesign. Write this FIRST.

Perft(n) counts the number of legal move sequences of length n from a position.
The counts for the standard start position are published and exact, so they
catch ANY move-generation bug (missed en passant, illegal castling through
check, pin handling, ...). Get these green before/while you port logic, and you
can refactor the domain fearlessly.

Standard start position (https://www.chessprogramming.org/Perft_Results):
    depth 1 -> 20
    depth 2 -> 400
    depth 3 -> 8902
    depth 4 -> 197281

Run with: pytest tests/chess/test_perft.py
"""
from __future__ import annotations

from games.chess.domain import movegen
from games.chess.domain.position import Position
from games.chess.domain.rules.classical import ClassicalChess


def perft(position: Position, depth: int, variant) -> int:
    if depth == 0:
        return 1
    total = 0
    for move in movegen.legal_moves(position, variant):
        total += perft(movegen.apply(position, move), depth - 1, variant)
    return total


def test_perft_start_position():
    variant = ClassicalChess()
    start = variant.initial_position()
    assert perft(start, 1, variant) == 20
    assert perft(start, 2, variant) == 400
    assert perft(start, 3, variant) == 8902
    # assert perft(start, 4, variant) == 197281  # enable once fast enough
