"""AI subpackage: search + evaluation. Depends on domain/ only.

The AI is a Player (app layer), not part of the rules. It consumes pure domain
objects (Position, Move) and returns a Move. Keeping it here means the domain
never depends on the AI, and the AI can be tested with hand-built positions.
"""
