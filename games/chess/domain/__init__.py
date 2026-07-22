"""Chess DOMAIN layer -- pure rules.

Absolutely no pygame, no "players", no "turns-alternate" assumption, no I/O.
Everything here is deterministic and unit-testable without a screen.

Dependency rule: domain/ imports only the standard library and its own package.
If a file in here imports pygame or from app/ or ui/, it is in the wrong layer.

The four questions this layer answers (see movegen.py + rules/):
  1. legal_moves(position, variant)  -> what moves are legal?
  2. is_legal(position, move, variant) -> is this move legal?
  3. apply(position, move)            -> what position results? (no mutation)
  4. variant.result(position)         -> is the game over, and how?
"""
