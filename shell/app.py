"""Application entry object: owns the main loop and pygame lifecycle.

Port from: core/app.py

Responsibilities:
  - pygame.init() / teardown
  - construct the SceneManager and set the initial scene
  - run the loop until the manager stops
"""
from __future__ import annotations

from shell.scene_manager import SceneManager


class App:
    def __init__(self) -> None:
        # TODO: pygame.init(); build SceneManager; set initial scene (e.g. main menu)
        self.scene_manager = SceneManager()

    def run(self) -> None:
        # TODO: while self.scene_manager.running: self.scene_manager.run_frame()
        raise NotImplementedError
