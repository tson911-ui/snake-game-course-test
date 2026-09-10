# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A classic Snake game written in Python, shipped as two independent, self-contained implementations that serve different purposes:

1. **`snake.py`** (recommended/full version) — Pygame-based arcade game with input buffering, difficulty levels, golden bonus apples, and persistent high scores.
2. **`snake_simple.py`** (zero-install version) — Uses only Python's built-in `turtle` module, no external dependencies.

There is no build system, package manifest, or test suite — this is a pair of standalone scripts.

## Commands

Run the full version (requires pygame):
```bash
pip install -r requirements.txt   # or: pip install pygame
python snake.py
```

Run the zero-dependency version (no install needed):
```bash
python snake_simple.py
```

There are no lint or test commands configured in this repo.

## Architecture

### `snake.py`
- All tunable config (grid size, colors, difficulty FPS) lives in constants at the top of the file — this is the intended place to adjust gameplay/visuals, not scattered through the class.
- `SnakeGame` is a single class driving the whole game loop (`run()` → `handle_input()` → `update()` → `render()` each tick) with an explicit state machine: `MENU`, `PLAYING`, `PAUSED`, `GAMEOVER`.
- **Input buffering**: keypresses go into `self.input_queue` (max length 2) rather than mutating direction immediately; `queue_direction()` rejects a queued direction that is the exact reverse of the current one. This is what prevents accidental 180° self-collision on rapid key taps — preserve this indirection when touching movement/input code.
- **Persistence**: `load_high_score()` / `save_high_score()` read/write `highscore.txt` (path resolved relative to the script via `os.path.dirname(__file__)`), each wrapped in `try/except` since the file may not exist or be writable.
- Food spawning avoids the snake body via list-comprehension over empty cells (`spawn_food`, `maybe_spawn_golden_apple`); golden apples appear on a timer (`golden_timer`) every 5th apple eaten with a 60% chance.
- Grid coordinates are always integers within `0 <= x < GRID_WIDTH`, `0 <= y < GRID_HEIGHT`; pixel positions are derived from grid coordinates only at draw time (`draw_*` methods), offset by `TOP_BAR_HEIGHT` for the header bar.

### `snake_simple.py`
- Procedural script (no classes) using module-level globals and turtle's manual screen-refresh mode (`wn.tracer(0)` + explicit `wn.update()`), typical of turtle-based games.
- Deliberately kept minimal and dependency-free — do not add pygame or other third-party imports here.

## Conventions

- PEP 8 naming: `snake_case` for functions/variables, `CamelCase` for classes, `UPPER_SNAKE_CASE` for constants.
- Keep the two game versions independent: advanced features (sound, particle effects, new themes) belong in `snake.py`; `snake_simple.py` must stay pip-install-free.
- Any file I/O (high scores or new save data) must be wrapped in `try/except` to tolerate missing files or lack of write permission.
- Both versions must support Arrow keys and WASD in parallel, with Space for pause/resume and R for quick restart.
