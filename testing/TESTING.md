# Testing Documentation

## Overview
This document details the testing methodology used to benchmark the performance of the new AI against the old AI.

## Environment
- **Directory**: `testing/`
- **Files**:
    - `old_ai.py`: Baseline AI implementation (MinMax with Alpha-Beta).
    - `new_ai.py`: Enhanced AI implementation (Iterative Deepening, Move Ordering, Enhanced Evaluation).
    - `benchmark.py`: Script to run the simulation.
    - `analysis.ipynb`: Notebook to analyze the results.

## Methodology
1.  **Simulation**: 100 games are played between the two AIs.
    -   **Phase 1**: 50 games with Old AI as RED (Player 1) and New AI as BLACK (Player 2).
    -   **Phase 2**: 50 games with New AI as RED (Player 1) and Old AI as BLACK (Player 2).
2.  **Time Limit**: The New AI uses a time limit of 0.5 seconds per move for the benchmark. The Old AI uses a fixed depth of 3.
3.  **Data Collection**: For each game, we record:
    -   Winner
    -   Total moves
    -   Total time
    -   Per-move duration
    -   AI used for each turn

## Analysis
The `analysis.ipynb` notebook processes the `benchmark_results.json` file to generate:
-   **Win Rates**: Overall and per-phase win percentages.
-   **Time Analysis**: Average time per move, distribution of move times.
-   **Game Length**: Histogram of total moves per game.
-   **Progression**: Average time per move as the game progresses.

## Running the Benchmark
To run the benchmark:
```bash
python testing/benchmark.py
```
This will generate `benchmark_results.json`. Then open `testing/analysis.ipynb` to view the analysis.
