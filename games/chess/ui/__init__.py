"""Chess PRESENTATION layer -- pygame rendering + input.

Dependency rule: ui/ imports app/ (and domain value types for reading), plus
ui_kit and shell.scene. It contains NO rules and NO orchestration logic --
it turns input into intents and draws snapshots.
"""
