"""Shared, game-agnostic UI widgets (buttons, menus) and the visual theme.

Dependency rule: ui_kit/ is a leaf. It must not import from games/ or shell/.
Games and scenes import ui_kit, never the other way around.
"""
