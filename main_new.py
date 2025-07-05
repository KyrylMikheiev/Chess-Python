import pygame
from core.scene_manager import SceneManager
from scenes.menu_scene import MainMenuScene


def main():
    pygame.init()
    scene_manager = SceneManager()
    scene_manager.change_scene(MainMenuScene(scene_manager))  # First scene

    while scene_manager.running:
        scene_manager.run_frame()

    pygame.quit()

if __name__ == "__main__":
    main()
