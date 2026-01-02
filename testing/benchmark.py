"""
Benchmark Module for Console Checkers AI.

This module provides tools to benchmark the performance of the AI algorithms.
It runs games between different AI versions or configurations and records
metrics such as win rates, move times, and game lengths.
"""

import sys
import os
import time
import json
import random

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from board import Board
from constants import RED, BLACK
from testing import old_ai
from testing import new_ai

def play_game(red_ai_func, black_ai_func, game_id):
    """
    Simulates a single game between two AI functions.

    Args:
        red_ai_func (function): The AI function for the RED player.
        black_ai_func (function): The AI function for the BLACK player.
        game_id (int): A unique identifier for the game.

    Returns:
        dict: A dictionary containing game statistics:
            - game_id: The game identifier.
            - winner: The color of the winner ('RED', 'BLACK', or 'DRAW').
            - moves: A list of dictionaries detailing each move (turn, duration, move_count).
            - red_ai: Name of the RED AI function.
            - black_ai: Name of the BLACK AI function.
    """
    board = Board()
    turn = RED
    move_count = 0
    game_data = {
        "game_id": game_id,
        "winner": None,
        "moves": [],
        "red_ai": red_ai_func.__name__,
        "black_ai": black_ai_func.__name__
    }
    
    while True:
        start_time = time.time()
        
        if turn == RED:
            if red_ai_func == old_ai.minimax:
                _, move_details = old_ai.minimax(board, 3, float('-inf'), float('inf'), False)
            else:
                move_details = new_ai.iterative_deepening(board, False, time_limit=0.5)
        else:
            if black_ai_func == old_ai.minimax:
                _, move_details = old_ai.minimax(board, 3, float('-inf'), float('inf'), True)
            else:
                move_details = new_ai.iterative_deepening(board, True, time_limit=0.5)
        
        end_time = time.time()
        duration = end_time - start_time
        
        if move_details is None:
            winner = BLACK if turn == RED else RED
            game_data["winner"] = "BLACK" if winner == BLACK else "RED"
            break
            
        start_coords, end_coords, skipped_coords = move_details
        
        game_data["moves"].append({
            "turn": "RED" if turn == RED else "BLACK",
            "duration": duration,
            "move_count": move_count
        })
        
        piece = board.get_piece(start_coords[0], start_coords[1])
        board.move(piece, end_coords[0], end_coords[1], visual=False)
        
        if skipped_coords:
            pieces_to_remove = []
            for r, c in skipped_coords:
                p = board.get_piece(r, c)
                if p != 0:
                    pieces_to_remove.append(p)
            board.remove(pieces_to_remove, visual=False)
        
        winner = board.winner()
        if winner is not None:
            game_data["winner"] = "BLACK" if winner == BLACK else "RED"
            break
            
        turn = BLACK if turn == RED else RED
        move_count += 1
        
        if move_count > 200:
            game_data["winner"] = "DRAW"
            break
            
    return game_data

def print_progress_bar(iteration, total, prefix='', suffix='', decimals=1, length=50, fill='█', printEnd="\r"):
    """
    Call in a loop to create terminal progress bar.

    Args:
        iteration (int): Current iteration.
        total (int): Total iterations.
        prefix (str, optional): Prefix string. Defaults to ''.
        suffix (str, optional): Suffix string. Defaults to ''.
        decimals (int, optional): Positive number of decimals in percent complete. Defaults to 1.
        length (int, optional): Character length of bar. Defaults to 50.
        fill (str, optional): Bar fill character. Defaults to '█'.
        printEnd (str, optional): End character (e.g. "\\r", "\\r\\n"). Defaults to "\\r".

    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()

def main():
    results = []
    total_games_per_phase = 50
    
    print("Starting Phase 1: Old AI (RED) vs New AI (BLACK)")
    print_progress_bar(0, total_games_per_phase, prefix='Progress:', suffix='Complete', length=50)
    for i in range(total_games_per_phase):
        data = play_game(old_ai.minimax, new_ai.iterative_deepening, i+1)
        results.append(data)
        print_progress_bar(i + 1, total_games_per_phase, prefix='Progress:', suffix='Complete', length=50)
        
    print("Starting Phase 2: New AI (RED) vs Old AI (BLACK)")
    print_progress_bar(0, total_games_per_phase, prefix='Progress:', suffix='Complete', length=50)
    for i in range(total_games_per_phase):
        data = play_game(new_ai.iterative_deepening, old_ai.minimax, i+51)
        results.append(data)
        print_progress_bar(i + 1, total_games_per_phase, prefix='Progress:', suffix='Complete', length=50)
        
    with open('benchmark_results.json', 'w') as f:
        json.dump(results, f, indent=4)
        
    print("Benchmark complete. Results saved to benchmark_results.json")

if __name__ == "__main__":
    main()
