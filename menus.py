from ui import MenuButton
from utils import WIDTH, HEIGHT
from actions import ACTIONS

def create_menu(button_defs):
    buttons = []
    for i, (label, action_name) in enumerate(button_defs):
        x = WIDTH // 2 - MenuButton.WIDTH // 2
        y = HEIGHT // 2.5 + i * 70
        action = ACTIONS[action_name]
        buttons.append(MenuButton(x, y, label, action))
    return buttons

MENUS = {
    "main": [
        ("Play", "go_to_color_menu"),
        ("Statistics", "show_statistics"),
        ("Options", "show_options"),
        ("Quit", "quit_game")
    ],
    "color select": [
        ("Play as White", "start_game_white"),
        ("Play as Black", "start_game_black"),
        ("Back", "go_to_main_menu")
    ]
}

def get_menu(name):
    return create_menu(MENUS[name])
