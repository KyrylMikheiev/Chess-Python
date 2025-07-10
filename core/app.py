from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame
from core.scene_manager import SceneManager
from scenes.menus.main_menu import MainMenu


def app():
    pygame.init()
    scene_manager = SceneManager()
    scene_manager.change_scene(MainMenu(scene_manager))  # First scene

    while scene_manager.running:
        scene_manager.run_frame()

    pygame.quit()

