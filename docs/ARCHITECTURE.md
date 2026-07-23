# Architecture

A pygame app that hosts games. A thin **shell** (platform) hosts one **bounded
context per game**; each game is layered domain → app → ui. Chess variants
(Chess960, King of the Hill, …) are **strategies inside** the chess context, not
separate games.

## The layers and the one rule

Dependencies point **downward only**. Enforce it with pyright/mypy strict.

```
shell/            platform: app loop, scene manager, Scene contract   (no game knowledge)
ui_kit/           shared widgets + theme (leaf; imported by scenes/games)
scenes/           app-level non-game scenes (menus, variant select)

games/chess/
  domain/         PURE rules. No pygame, no players, no "turns alternate".
  app/            orchestration: Session (turns), Player, AI.  imports domain only.
  ui/             pygame: input→intents, draw snapshots.       imports app + ui_kit.
```

Litmus test: if a `domain/` file imports pygame or `app/`, it's in the wrong layer.

## Key design decisions (the *why*)

1. **Turns are an app concern, not a rule.** The domain answers "legal moves /
   apply / result" with no notion of alternation. `Session` (turn-based) owns the
   alternation; a future `RealtimeSession` (Kung Fu) reuses the same domain with
   a different flow. This is why real-time won't force a rewrite.
2. **Absolute coordinates.** Board is stored one way (row 0 = white). The UI
   flips for display. Kills the `is_players_color_white` branching everywhere.
3. **Pure move generation.** `movegen.apply(pos, move) -> new Position`; no
   in-place mutation, no `undo_move`. The AI just keeps old references.
4. **Pieces as data** (`SLIDERS`/`LEAPERS` tables), not methods on a god-object.
5. **`Variant` Strategy seam.** A new turn-based variant = one file in
   `domain/rules/` + register it. Touches nothing else.
6. **Value objects.** `Move`/`Position` are frozen dataclasses (free `==`,
   hashable, safe in the search). Enums replace `"w"/"b"/"wp"` magic strings.

## Migration order (do it in verifiable steps)

1. **Perft tests first** (`tests/chess/test_perft.py`) — your safety net.
2. Fill `domain/enums.py`, `move.py`, `position.py`, `pieces.py`.
3. Port move gen into `domain/movegen.py` (absolute coords, pure). Green perft 1–3.
4. Implement `rules/classical.py` (start position + result). Green perft 4.
5. `app/` — `Session` + `Player` (+ AI port). Get a runnable classical game.
6. `ui/` — `renderer.py` + `chess_scene.py` (scene builds a snapshot).
7. Point `shell/` + `scenes/` at the new scene; delete the old files.
8. Add `chess960.py` / `king_of_the_hill.py` — proof the seam works.

## Old → new mapping

| old | new |
| --- | --- |
| `core/app.py`, `core/scene_manager.py` | `shell/` |
| `constants.py`, `ui/*` | `ui_kit/` (+ `theme.py`) |
| `game_state.py` + `engine.py` + `pieces.py` | `games/chess/domain/*` |
| `controller.py` | `app/session.py` + `app/player.py` |
| `ai.py` | `app/ai/search.py` + `app/ai/evaluation.py` |
| `game_scene.py` + `ui.py` | `games/chess/ui/{chess_scene,renderer}.py` |

The old `Engine`/`GameState`/`Pieces` shared-`self` tangle has no home in this
layout — its concerns split across three `domain/` files behind a small facade,
so it can't reassemble.

> The new files are **skeletons**: contracts + docstrings + `TODO`s pointing at
> the source to port. The old code is untouched, so the branch still runs while
> you migrate file by file.
