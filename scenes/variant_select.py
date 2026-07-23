"""Variant selection scene: pick Classical / Chess960 / King of the Hill / ...

Follows the same shape as scenes/main_menu.py. This is the seam where a
Variant is chosen and handed into the chess game: on selection it builds the
chess scene with the chosen Variant and switches to it.
"""
import pygame

from core.scene_manager import SceneManager


class VariantSelect:

    def __init__(self, scene_manager: SceneManager):
        self.scene_manager = scene_manager
        # TODO: build one button per available Variant
        #       (see games/chess/domain/rules/). Reuse ui.menu.Menu like MainMenu.

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # TODO: on click -> resolve chosen Variant, then
            #   from games.chess.ui.chess_scene import ChessScene
            #   self.scene_manager.change_scene(ChessScene(self.scene_manager, variant))
            pass

    def update(self):
        pass

    def render(self, screen):
        # TODO: draw the variant buttons
        pass
