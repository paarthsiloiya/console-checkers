# Console Checkers

A console-based Checkers game written in Python, featuring a MinMax AI opponent with Alpha-Beta pruning and box-drawing character rendering.

## Features

- **Console Rendering**: Uses Unicode box-drawing characters for a clean board display.
- **Efficient Updates**: Uses `bext` to update only changed parts of the board, preventing flickering.
- **Game Modes**: Choose between Player vs Player or Player vs AI.
- **Smart AI**: Uses MinMax algorithm with Alpha-Beta pruning for efficient decision making.
- **Score Tracking**: Real-time display of remaining pieces for both players.
- **Input Handling**: Intuitive algebraic notation (e.g., "C3 D4").

## Installation

1.  Clone the repository.
2.  Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

## How to Play

Run the game using:
```bash
python main.py
```

1.  Select your game mode from the welcome screen.
2.  **RED** starts at the bottom, **BLACK** starts at the top.
3.  Enter moves in the format `Start End` (e.g., `C3 D4`).
4.  Press `q` to quit.

## Project Structure

- `main.py`: Entry point, game loop, and UI.
- `board.py`: Board representation, rendering logic, and move validation.
- `ai.py`: MinMax algorithm with Alpha-Beta pruning.
- `input_handler.py`: User input parsing.
- `constants.py`: Game constants and configuration.

## Improving the MinMax AI

The current AI uses MinMax with Alpha-Beta pruning. Here are further ways to improve its intelligence:

### 1. Enhanced Evaluation Function
The current evaluation only counts pieces. A better function would consider:
- **Positioning**: Pieces in the center and on the opponent's side are more valuable.
- **Kings**: Kings are worth more than regular pieces (e.g., 1.5x or 2x).
- **Mobility**: The number of legal moves available.
- **Safety**: Penalize pieces that are vulnerable to capture.
- **Structure**: Reward keeping pieces connected (defending each other).

### 2. Move Ordering
Evaluate "promising" moves first (e.g., captures or promotions). This maximizes the effectiveness of Alpha-Beta pruning.

### 3. Iterative Deepening
Instead of a fixed depth, start with depth 1, then 2, etc., until a time limit is reached. This ensures the AI always has a move ready.

### 4. Transposition Table
Store the results of previously evaluated board states to avoid re-calculating them if reached via a different move order.

### 5. Endgame Database
For positions with few pieces, use a pre-calculated database to play perfectly.
