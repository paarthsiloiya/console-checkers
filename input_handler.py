"""
Input Handler Module for Console Checkers.

This module is responsible for parsing and validating user input, converting
algebraic notation (e.g., "A3") into board coordinates.
"""

from constants import ROWS, COLS

def parse_position(pos_str):
    """
    Parses a position string (e.g., "A3") into row and column indices.

    Args:
        pos_str (str): The position string to parse.

    Returns:
        tuple or None: (row, col) if valid, None otherwise.
    """
    if len(pos_str) < 2:
        return None
    
    col_char = pos_str[0].upper()
    row_char = pos_str[1:]
    
    if not col_char.isalpha() or not row_char.isdigit():
        return None
    
    col = ord(col_char) - ord('A')
    row = int(row_char) - 1
    
    if 0 <= row < ROWS and 0 <= col < COLS:
        return (row, col)
    return None

def get_player_move(turn_color):
    """
    Prompts the player for a move and parses the input.

    Args:
        turn_color (int): The color of the current player (RED or BLACK).

    Returns:
        tuple or str or None: 
            - (start_pos, end_pos) tuple if input is valid.
            - 'QUIT' if the user wants to quit.
            - None if the input format is invalid.
    """
    color_name = "RED" if turn_color == 1 else "BLACK"
    
    try:
        move_str = input(f"{color_name}'s turn. Enter move (e.g., C3 D4) or 'q' to quit: ").strip()
        if move_str.lower() == 'q':
            return 'QUIT'
        
        parts = move_str.split()
        if len(parts) != 2:
            return None
        
        start_pos = parse_position(parts[0])
        end_pos = parse_position(parts[1])
        
        if start_pos and end_pos:
            return (start_pos, end_pos)
        else:
            return None
    except KeyboardInterrupt:
        return 'QUIT'
