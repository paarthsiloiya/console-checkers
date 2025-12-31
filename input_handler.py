from constants import ROWS, COLS

def parse_position(pos_str):
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
