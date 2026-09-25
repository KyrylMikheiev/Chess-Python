from enum import Enum
from constants.window import HEIGHT, WIDTH

class ScenesEnum(Enum):
    MAIN_MENU = "Main"
    COLOR_MENU = "Color Menu"
    GAME_SCENE = "Game Scene"

MENUS_WITH_BUTTONS_AND_LINKS = {
    ScenesEnum.MAIN_MENU: [
        ("Play", ScenesEnum.COLOR_MENU),
    ],
    ScenesEnum.COLOR_MENU: [
        ("Play as White", ScenesEnum.GAME_SCENE),
        ("Play as Black", ScenesEnum.GAME_SCENE),
        ("Back", ScenesEnum.MAIN_MENU),
    ],
    ScenesEnum.GAME_SCENE: [
        ("To Color Menu", ScenesEnum.COLOR_MENU)
    ]
}

MENU_NAME_COLOR = "white"

BUTTON_WIDTH = 400
BUTTON_HEIGHT = 50
X_OFFSET_BUTTON = (WIDTH - BUTTON_WIDTH) // 2
Y_OFFSET_BUTTON = (HEIGHT - BUTTON_WIDTH) // 2
BUTTON_BG_COLOR = "white"
BUTTON_BG_HOVER_COLOR = "lightgray"
BUTTON_FONT_COLOR = "black"