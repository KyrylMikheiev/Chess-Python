"""The contract between the shell and every game/scene.

This is the ONLY thing the shell knows about a game. A chess scene, a menu,
a settings screen -- all implement this. The shell drives them uniformly.

Keep this tiny and game-agnostic: no chess concepts allowed here.
"""
from __future__ import annotations

from typing import Protocol

import pygame


class Scene(Protocol):
    """Anything the SceneManager can drive for one frame."""

    def handle_event(self, event: pygame.event.Event) -> None:
        """React to a single input event (mouse, key, ...)."""
        ...

    def update(self, dt: float) -> None:
        """Advance the scene by one tick. `dt` = seconds since last frame."""
        ...

    def render(self, surface: pygame.Surface) -> None:
        """Draw the current state onto `surface`. No game logic here."""
        ...
