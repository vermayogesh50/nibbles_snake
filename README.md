# Nibbles (Snake)

A small, asset-free Snake game for Windows, written in Python with Pygame. The snake and square food use shaded, beveled shapes for a 3D-style look. Choose Easy, Medium, or Hard, then use the arrow keys to play. You have three lives; each collision uses one, and your score is kept between attempts.

## Project structure

```text
nibbles/
├── game.py             # Pygame window, drawing, input, and game loop
├── game_logic.py       # Small game-rule functions
├── test_game_logic.py  # Tests for the rules
├── requirements.txt    # Python package dependencies
└── README.md
```

## Prerequisites

- Windows 10 or later
- Python 3.9 through 3.13
- An internet connection for the one-time Pygame installation

During Python setup, select **Add Python to PATH**. The commands below use the Windows `py` launcher; if it is unavailable, replace `py` with `python`.

## Install and run

Open Command Prompt or PowerShell in this project folder, then run:

```powershell
py -m venv .venv
.\.venv\Scripts\activate
py -m pip install -r requirements.txt
py game.py
```

At the start screen, press **1** for Easy, **2** for Medium, or **3** for Hard. Higher difficulty makes the snake move faster. Use the **arrow keys** to steer. Eat the red food to grow and earn one point. Avoid the edges and your own body; a collision uses one of your three lives and starts a fresh attempt while keeping your score. After game over (or winning by filling the board), press **R** or **Enter** to play again at the same difficulty, or **M** to choose a difficulty. Close the window to quit.

## Run the tests

The game-rule tests use Python's built-in `unittest` and do not open a game window:

```powershell
py -m unittest -v
```

## How the code works

- **`game_logic.py`** contains functions that work with grid coordinates. `move_snake` calculates a step and reports food or a collision; `place_food` selects a free cell; `is_opposite_direction` prevents an immediate turn back into the snake. Keeping these rules separate makes them straightforward to test.
- **`draw_difficulty_selection`** displays the start screen, where the player chooses a speed.
- **`create_new_game`** in `game.py` sets up the starting snake, direction, food, score, lives, and chosen difficulty. Calling it again resets the game.
- **`handle_direction_key`** turns arrow-key presses into a queued direction. The game ignores a direct reversal.
- **`update_game`** advances the snake one cell, increments the score when food is eaten, places replacement food, and uses a life on collision. It ends the game after the third collision.
- **`draw_game`** draws the grid, shaded snake segments, square food, score, and game-over screen using Pygame shapes and text—no image files are needed. The 3D-style appearance is drawn in 2D; the game rules remain on a simple grid.
- **`main`** starts Pygame and repeatedly reads input, updates the game at a steady pace, and draws each frame.
