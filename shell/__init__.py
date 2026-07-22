"""Shell / platform layer.

Generic game-hosting framework: the app loop, scene switching, and the
Scene contract every game implements. Knows NOTHING about chess.

Dependency rule: shell/ must never import from games/.
"""
