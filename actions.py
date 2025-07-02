import pygame
import sys
from app_state import AppState
from utils import IMAGES, SQUARE_SIZE, WIDTH, HEIGHT, x_offset, y_offset, WINDOW as screen
import os

ACTIONS = {}

def load_images():
    pieces = ["wp", "wr", "wn", "wb", "wq", "wk", "bp", "br", "bn", "bb", "bq", "bk"]
    for piece in pieces:
        IMAGES[piece] = pygame.image.load(os.path.join("Assets", f'{piece}.png'))

def start_game_white(state: AppState):
    print("Starting as white")
    load_images()
    state.set_current_menu("game")
    state.is_players_color_white = True
    return None

def start_game_black(state: AppState):
    print("Starting as black")
    load_images()
    state.set_current_menu("game")
    state.is_players_color_white = False
    return None

def go_to_color_menu(state):
    return "color select"

def go_to_main_menu(state):
    return "main"

def quit_game(state):
    pygame.quit()
    sys.exit() #do i need it?

def show_statistics(state):
    print("Statistics clicked")

def show_options(state):
    print("Options clicked")

# Register actions
ACTIONS.update({
    "start_game_white": start_game_white,
    "start_game_black": start_game_black,
    "go_to_color_menu": go_to_color_menu,
    "go_to_main_menu": go_to_main_menu,
    "quit_game": quit_game,
    "show_statistics": show_statistics,
    "show_options": show_options
})
