from copy import deepcopy
from constants import RED, BLACK

def minimax(position, depth, alpha, beta, max_player):
    if depth == 0 or position.winner() != None:
        return position.evaluate(), position
    
    if max_player:
        maxEval = float('-inf')
        best_move = None
        for move, move_details in get_all_moves(position, BLACK):
            evaluation = minimax(move, depth-1, alpha, beta, False)[0]
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
        for move, move_details in get_all_moves(position, RED):
            evaluation = minimax(move, depth-1, alpha, beta, True)[0]
            minEval = min(minEval, evaluation)
            if minEval == evaluation:
                best_move = move_details
            beta = min(beta, evaluation)
            if beta <= alpha:
                break
        
        return minEval, best_move

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
