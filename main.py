import bext
import colorama
from constants import *
from board import Board
from input_handler import get_player_move
from ai import iterative_deepening

def draw_welcome_screen():
    bext.clear()
    print(f"{COLOR_RED}" + "="*55)
    print(f"{COLOR_RED}   _____ _               _                 ")
    print(f"{COLOR_RED}  / ____| |             | |                ")
    print(f"{COLOR_RED} | |    | |__   ___  ___| | _____ _ __ ___ ")
    print(f"{COLOR_RED} | |    | '_ \ / _ \/ __| |/ / _ \ '__/ __|")
    print(f"{COLOR_RED} | |____| | | |  __/ (__|   <  __/ |  \__ \\")
    print(f"{COLOR_RED}  \_____|_| |_|\___|\___|_|\_\___|_|  |___/")
    print(f"{COLOR_RED}" + "="*55 + f"{COLOR_RESET}")
    print("\nWelcome to Console Checkers!")
    print("1. Player vs Player")
    print("2. Player vs AI")
    print("\nSelect mode (1 or 2): ", end='')

def draw_score(board):
    bext.goto(BOARD_OFFSET_X, 0)
    print(f"{COLOR_RED}RED: {board.red_left} {KING_SYMBOL if board.red_kings > 0 else ''}   {COLOR_BLACK}BLACK: {board.black_left} {KING_SYMBOL if board.black_kings > 0 else ''}{COLOR_RESET}   ")

def main():
    bext.title('Console Checkers')
    draw_welcome_screen()
    
    mode = ''
    while mode not in ['1', '2']:
        mode = input().strip()
        if mode not in ['1', '2']:
            print("Invalid selection. Please enter 1 or 2: ", end='')
    
    bext.clear()
    board = Board()
    board.draw()
    draw_score(board)
    
    turn = RED
    input_line = BOARD_OFFSET_Y + ROWS * 2 + 2
    
    while True:
        winner = board.winner()
        if winner is not None:
            bext.goto(0, input_line)
            if winner == RED:
                print(f"{COLOR_RED}RED WINS!{COLOR_RESET}")
            else:
                print(f"{COLOR_BLACK}BLACK WINS!{COLOR_RESET}")
            break
        
        draw_score(board)
        
        if mode == '1' or turn == RED:
            valid_move = False
            while not valid_move:
                bext.goto(0, input_line)
                print(' ' * 80) 
                bext.goto(0, input_line)
                
                move = get_player_move(turn)
                
                bext.goto(0, input_line)
                print(' ' * 80)
                bext.goto(0, input_line + 1)
                print(' ' * 80)
                
                if move == 'QUIT':
                    return
                
                if move is None:
                    bext.goto(0, input_line + 1)
                    print("Invalid format. Use 'A3 B4'.")
                    continue

                start, end = move
                piece = board.get_piece(start[0], start[1])
                
                if piece != 0 and piece.color == turn:
                    valid_moves = board.get_valid_moves(piece)
                    if end in valid_moves:
                        skipped = valid_moves[end]
                        board.move(piece, end[0], end[1])
                        if skipped:
                            board.remove(skipped)
                        valid_move = True
                        turn = BLACK if turn == RED else RED
                    else:
                        bext.goto(0, input_line + 1)
                        print("Invalid move for this piece.")
                else:
                    bext.goto(0, input_line + 1)
                    color_str = "RED" if turn == RED else "BLACK"
                    print(f"No {color_str} piece at that location.")
        else:
            bext.goto(0, input_line)
            print("AI is thinking...")
            
            move_details = iterative_deepening(board, True, time_limit=1.0)
            
            if move_details is None:
                bext.goto(0, input_line)
                print("AI has no moves. RED wins!")
                break
            
            start_coords, end_coords, skipped_coords = move_details
            
            piece = board.get_piece(start_coords[0], start_coords[1])
            board.move(piece, end_coords[0], end_coords[1])
            
            if skipped_coords:
                pieces_to_remove = []
                for r, c in skipped_coords:
                    p = board.get_piece(r, c)
                    if p != 0:
                        pieces_to_remove.append(p)
                board.remove(pieces_to_remove)
            
            turn = RED
            
            bext.goto(0, input_line)
            print(' ' * 80)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        print(COLOR_RESET)
