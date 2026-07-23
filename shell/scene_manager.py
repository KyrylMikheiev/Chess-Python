"""Owns the active scene and the switching between scenes.

Port from: core/scene_manager.py

Responsibilities:
  - hold the current Scene (see shell/scene.py)
  - own the pygame display surface
  - pump events -> current scene, then update -> render each frame

It must not know what a scene *is* internally -- only the Scene contract.
"""
from __future__ import annotations

import pygame

from shell.scene import Scene


class SceneManager:
    def __init__(self) -> None:
        self.current_scene: Scene | None = None
        self.running: bool = True
        # TODO: port display setup (set_mode, caption, fullscreen) from core/scene_manager.py
        self.screen: pygame.Surface | None = None

    def change_scene(self, scene: Scene) -> None:
        self.current_scene = scene

    def quit(self) -> None:
        self.running = False

    def run_frame(self) -> None:
        # TODO: port event pump + update + render from core/scene_manager.py
        # 1. handle global events (QUIT, F11) here
        # 2. forward the rest to current_scene.handle_event
        # 3. current_scene.update(dt); current_scene.render(self.screen)
        raise NotImplementedError
