from core.scenes_enum import ScenesEnum

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
        ("to color menu", ScenesEnum.COLOR_MENU)
    ]
}