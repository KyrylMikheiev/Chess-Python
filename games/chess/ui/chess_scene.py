"""ChessScene -- the game's entry point into the shell. The reborn GameScene.

Implements shell.scene.Scene. Responsibilities:
  - own a Session (app layer) and a Renderer (ui layer)
  - translate pygame input into intents:
      * click board -> select square / build a Move -> HumanPlayer.submit(move)
      * 'z' -> session.undo(), 'r' -> reset
  - build a render snapshot from the Session and hand it to the Renderer
It holds the transient UI-only state (selected square, click list) that used to
be smeared across GameScene / Controller / ChessUi.

Port from: game_scene.py (input handling + wiring).
"""
from __future__ import annotations

import pygame

from games.chess.app.player import AIPlayer, HumanPlayer
from games.chess.app.session import Session
from games.chess.domain.enums import Color
from games.chess.domain.rules.variant import Variant
from games.chess.ui.renderer import Renderer
from shell.scene_manager import SceneManager


class ChessScene:
    def __init__(self, scene_manager: SceneManager, variant: Variant,
                 human_color: Color = Color.WHITE) -> None:
        self.scene_manager = scene_manager
        self.human_color = human_color
        self.human = HumanPlayer()
        ai = AIPlayer()
        white = self.human if human_color is Color.WHITE else ai
        black = ai if human_color is Color.WHITE else self.human
        self.session = Session(variant, white, black)
        self.renderer = Renderer(scene_manager.screen)

        # transient UI-only state
        self.selected_square: tuple[int, int] | None = None
        self.click_buffer: list[tuple[int, int]] = []

    def handle_event(self, event: pygame.event.Event) -> None:
        # TODO: keydown z/r; mousebutton -> map pixel to (row,col) [flip if black],
        #       select square, and on 2nd click build a Move + self.human.submit(move)
        raise NotImplementedError

    def update(self, dt: float) -> None:
        self.session.step()

    def render(self, surface: pygame.Surface) -> None:
        # TODO: build a snapshot from self.session + selection, then
        #       self.renderer.draw(surface, snapshot)
        raise NotImplementedError
