"""Renderer -- draws a snapshot. Knows nothing about controllers or rules.

Design change vs the old ChessUi: it must NOT reach back into
controller.gs.board (the old code did, and referenced self.controller /
self.selected_square that were never set -- that's why it was broken). Instead
the scene hands it exactly what to draw each frame.

Board FLIPPING for display happens HERE (bottom = the human's color), so the
domain can stay in absolute coordinates.

Port the drawing bodies from ui.py: draw_board, highlight_move,
highlight_squares, draw_pieces_and_chars, draw_text, load_images.
"""
from __future__ import annotations

import pygame


class Renderer:
    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        # TODO: load_images() into an images dict keyed by (Color, PieceType)

    def draw(self, surface: pygame.Surface, snapshot) -> None:
        """Draw everything for one frame from `snapshot` (see ChessScene).

        snapshot carries: board, side_to_move, selected square, legal targets
        for the selected piece, last move, result/status text, and the human's
        color (for orientation). The renderer only reads it.
        """
        # TODO: board -> highlights -> pieces/coords -> status popup
        raise NotImplementedError
