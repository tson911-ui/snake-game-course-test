# 🐍 Python Snake Game

A clean, responsive, and easy-to-play **Snake Game** written in Python!

This project includes **two versions**:
1. **`snake.py` (Recommended)** — Full-featured arcade version built with **Pygame** featuring smooth graphics, modern retro color palette, eyes that look in the direction of movement, normal & golden bonus apples, adjustable difficulty, and persistent high scores.
2. **`snake_simple.py`** — Lightweight, **zero-install** version using Python's built-in `turtle` library (no external packages required).

---

## 🚀 Quick Start

### Option 1: Full Version (Pygame)

1. **Install requirements** (only needed once):
   ```bash
   pip install -r requirements.txt
   ```
   *(Or simply `pip install pygame`)*

2. **Run the game**:
   ```bash
   python snake.py
   ```

---

### Option 2: Zero-Install Version (Turtle)

If you cannot install external packages or just want to run immediately:

```bash
python snake_simple.py
```

*Works out of the box with standard Python!*

---

## 🎮 Controls

Both games support both **Arrow keys** and **WASD**:

| Action | Controls |
| :--- | :--- |
| **Move Up** | <kbd>↑</kbd> or <kbd>W</kbd> |
| **Move Down** | <kbd>↓</kbd> or <kbd>S</kbd> |
| **Move Left** | <kbd>←</kbd> or <kbd>A</kbd> |
| **Move Right** | <kbd>→</kbd> or <kbd>D</kbd> |
| **Pause / Resume** | <kbd>Space</kbd> |
| **Restart Game** | <kbd>R</kbd> (or <kbd>Space</kbd> / <kbd>Enter</kbd> on Game Over) |
| **Select Difficulty** *(Menu)* | <kbd>1</kbd> Easy, <kbd>2</kbd> Normal, <kbd>3</kbd> Hard |
| **Exit Game** | <kbd>Esc</kbd> |

---

## ✨ Features

- **Anti-Glitch Input Buffering**: Rapidly pressing two keys (e.g. `Right` then `Down`) won't cause accidental 180° self-collisions.
- **Persistent High Scores**: Best scores are automatically saved to `highscore.txt` so your achievements stay saved between sessions.
- **Difficulty Modes**:
  - `[1] Easy`: Relaxed, casual pace (8 FPS) — great for beginners!
  - `[2] Normal`: Classic arcade pace (12 FPS).
  - `[3] Hard`: Fast-paced challenge (18 FPS).
- **Golden Apples**: Every 5 apples, a golden bonus apple has a chance to appear for limited time, granting **+30 points**!
- **Visual Polish**: Animated snake eyes, soft grid lines, rounded body segments, and sleek Game Over overlay.

---

## 📁 Project Structure

```text
test vc/
├── snake.py              # Main game (Pygame, feature-rich)
├── snake_simple.py       # Standalone game (turtle, zero-dependency)
├── requirements.txt      # Dependencies (pygame)
├── highscore.txt         # Created automatically to store best score
├── project_snakegame.md  # Project Context & Guidelines
└── README.md             # Guide and documentation
```

---

## 🛠️ Easy Customization

You can easily tweak settings at the top of [`snake.py`](file:///C:/Users/hatha/Desktop/test%20vc/snake.py):

- **Change Grid or Window Size**:
  ```python
  CELL_SIZE = 25       # Pixel size of each cell
  GRID_WIDTH = 32      # 32 * 25 = 800 px width
  GRID_HEIGHT = 22     # 22 * 25 + 50 = 600 px height
  ```
- **Change Speeds / Difficulties**:
  ```python
  DIFFICULTIES = {
      "EASY": {"speed": 8, "name": "Easy (Casual)"},
      "NORMAL": {"speed": 12, "name": "Normal (Standard)"},
      "HARD": {"speed": 18, "name": "Hard (Fast)"}
  }
  ```
- **Change Colors**: Modify the RGB color tuples like `COLOR_SNAKE_HEAD`, `COLOR_BG_DARK`, etc.

Have fun playing! 🕹️
