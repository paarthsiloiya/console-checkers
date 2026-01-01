from copy import deepcopy
from constants import RED, BLACK, ROWS, COLS
import time
import random

def evaluate_board(board):
    if board.winner() == BLACK:
        return float('inf')
    if board.winner() == RED:
        return float('-inf')

    score = 0
    for row in range(ROWS):
        for col in range(COLS):
            piece = board.board[row][col]
            if piece != 0:
                piece_score = 10
                if piece.king:
                    piece_score = 20
                
                if 2 <= row <= 5 and 2 <= col <= 5:
                    piece_score += 2
                
                if not piece.king:
                    if piece.color == BLACK:
                        piece_score += row
                    else:
                        piece_score += (7 - row)
                
                if col == 0 or col == COLS - 1:
                    piece_score += 1
                
                if piece.color == BLACK:
                    score += piece_score
                else:
                    score -= piece_score
    
    return score

def minimax(position, depth, alpha, beta, max_player, start_time, time_limit):
    if time.time() - start_time > time_limit:
        raise TimeoutError

    if depth == 0 or position.winner() != None:
        return evaluate_board(position), position
    
    if max_player:
        maxEval = float('-inf')
        best_move = None
        moves = get_all_moves(position, BLACK)
        random.shuffle(moves)
        moves.sort(key=lambda x: len(x[1][2]), reverse=True)
        
        for move, move_details in moves:
            evaluation = minimax(move, depth-1, alpha, beta, False, start_time, time_limit)[0]
            maxEval = max(maxEval, evaluation)
            if maxEval == evaluation:
                best_move = move_details
            alpha = max(alpha, evaluation)
            if beta <= alpha:
                break
        
        return maxEval, best_move
    else:
        minEval = float('inf')
        best_move = None
        moves = get_all_moves(position, RED)
        random.shuffle(moves)
        moves.sort(key=lambda x: len(x[1][2]), reverse=True)
        
        for move, move_details in moves:
            evaluation = minimax(move, depth-1, alpha, beta, True, start_time, time_limit)[0]
            minEval = min(minEval, evaluation)
            if minEval == evaluation:
                best_move = move_details
            beta = min(beta, evaluation)
            if beta <= alpha:
                break
        
        return minEval, best_move

def iterative_deepening(position, max_player, time_limit=1.0):
    start_time = time.time()
    best_move = None
    depth = 1
    
    try:
        while True:
            if time.time() - start_time > time_limit:
                break
            
            val, move = minimax(position, depth, float('-inf'), float('inf'), max_player, start_time, time_limit)
            if move:
                best_move = move
            
            depth += 1
            
            if abs(val) == float('inf') or depth > 20:
                break
                
    except TimeoutError:
        pass
        
    return best_move

def simulate_move(piece, move, board, skip):
    board.move(piece, move[0], move[1], visual=False)
    if skip:
        board.remove(skip, visual=False)
    return board

def get_all_moves(board, color):
    moves = []
    for piece in board.get_all_pieces(color):
        valid_moves = board.get_valid_moves(piece)
        for move, skip in valid_moves.items():
            temp_board = deepcopy(board)
            temp_piece = temp_board.get_piece(piece.row, piece.col)
            new_board = simulate_move(temp_piece, move, temp_board, skip)
            skipped_coords = [(p.row, p.col) for p in skip]
            move_details = ((piece.row, piece.col), move, skipped_coords)
            moves.append((new_board, move_details))
    return moves
