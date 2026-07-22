"""Variant rules -- the Strategy seam that makes new game modes cheap.

Each Variant defines what differs from classical chess: starting position,
any special move rules, and the end/win condition. Everything shared (piece
movement, check detection) stays in movegen.py and is reused by all variants.

Adding a turn-based variant = add one file here + register it. It does NOT
touch the domain core, the app layer, or the UI.
"""
