from typing import Protocol

from core.scenes_enum import ScenesEnum

"""
    Methods that are allowed to be called within a scene.
    Each scene may call set_scene. For now this is it
"""
class SceneManagerInterface(Protocol):
    
    def set_scene(self, scene: ScenesEnum):
        pass