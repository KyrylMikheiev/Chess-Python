import pygame
import sys

ACTIONS = {}

def start_game_white():
    print("Starting as white")
    return None  # stays on same menu or exits loop

def start_game_black():
    print("Starting as black")
    return None

def go_to_color_menu():
    return "color select"

def go_to_main_menu():
    return "main"

def quit_game():
    pygame.quit()
    sys.exit()

def show_statistics():
    print("Statistics clicked")

def show_options():
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
