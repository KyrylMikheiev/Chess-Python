import pygame
import sys
from game import Board
from app_state import AppState
from utils import WINDOW as screen

ACTIONS = {}

def start_game_white(state):
    print("Starting as white")
    state.set_current_menu("game")
    board = Board(screen, True)
    state.set_board(board)
    return None

def start_game_black(state):
    print("Starting as black")
    state.set_current_menu("game")
    board = Board(screen, False)
    state.set_board(board)
    return None

def go_to_color_menu(state):
    return "color select"

def go_to_main_menu(state):
    return "main"

def quit_game(state):
    pygame.quit()
    sys.exit()

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
