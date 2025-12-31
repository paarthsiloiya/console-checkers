import bext
import colorama
from constants import *

class Piece:
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.king = False

    def make_king(self):
        self.king = True

    def draw(self, x, y):
        try:
            bext.goto(x, y)
            symbol = KING_SYMBOL if self.king else PIECE_SYMBOL
            color = COLOR_RED if self.color == RED else COLOR_BLACK
            print(f"{color}{symbol}{COLOR_RESET}", end='')
        except:
            pass

class Board:
    def __init__(self):
        self.board = []
        self.red_left = self.black_left = 12
        self.red_kings = self.black_kings = 0
        self.create_board()

    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if col % 2 == ((row +  1) % 2):
                    if row < 3:
                        self.board[row].append(Piece(row, col, BLACK))
                    elif row > 4:
                        self.board[row].append(Piece(row, col, RED))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)

    def draw(self):
        bext.clear()
        
        bext.goto(BOARD_OFFSET_X + 2, BOARD_OFFSET_Y - 1)
        print("   ".join(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']))

        for row in range(ROWS):
            bext.goto(BOARD_OFFSET_X, BOARD_OFFSET_Y + row * 2)
            if row == 0:
                print(BOX_TL + (BOX_H * 3 + BOX_TM) * (COLS - 1) + BOX_H * 3 + BOX_TR)
            else:
                print(BOX_LM + (BOX_H * 3 + BOX_CROSS) * (COLS - 1) + BOX_H * 3 + BOX_RM)
            
            print(f" {row + 1}")

            bext.goto(BOARD_OFFSET_X, BOARD_OFFSET_Y + row * 2 + 1)
            print(BOX_V, end='')
            for col in range(COLS):
                bg_color = COLOR_BOARD_LIGHT if (row + col) % 2 == 0 else COLOR_BOARD_DARK
                
                print(f"{bg_color}   {COLOR_RESET}", end='')
                
                piece = self.board[row][col]
                if piece != 0:
                    pass
                
                print(BOX_V, end='')
            
        bext.goto(BOARD_OFFSET_X, BOARD_OFFSET_Y + ROWS * 2)
        print(BOX_BL + (BOX_H * 3 + BOX_BM) * (COLS - 1) + BOX_H * 3 + BOX_BR)
        
        self.draw_pieces()

    def draw_pieces(self):
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    screen_x = BOARD_OFFSET_X + 1 + col * 4 + 1
                    screen_y = BOARD_OFFSET_Y + 1 + row * 2
                    piece.draw(screen_x, screen_y)

    def update_piece_visual(self, row, col):
        screen_x = BOARD_OFFSET_X + 1 + col * 4 + 1
        screen_y = BOARD_OFFSET_Y + 1 + row * 2
        
        piece = self.board[row][col]
        
        bext.goto(screen_x - 1, screen_y)
        bg_color = COLOR_BOARD_LIGHT if (row + col) % 2 == 0 else COLOR_BOARD_DARK
        print(f"{bg_color}   {COLOR_RESET}", end='')
        
        if piece != 0:
            piece.draw(screen_x, screen_y)

    def move(self, piece, row, col, visual=True):
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        
        if visual:
            self.update_piece_visual(piece.row, piece.col)
        
        piece.row = row
        piece.col = col

        if row == ROWS - 1 or row == 0:
            if (piece.color == RED and row == 0) or (piece.color == BLACK and row == ROWS - 1):
                piece.make_king()

        if visual:
            self.update_piece_visual(row, col)

    def get_piece(self, row, col):
        return self.board[row][col]

    def get_valid_moves(self, piece):
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row

        if piece.color == RED or piece.king:
            moves.update(self._traverse_left(row - 1, max(row - 3, -1), -1, piece.color, left))
            moves.update(self._traverse_right(row - 1, max(row - 3, -1), -1, piece.color, right))
        
        if piece.color == BLACK or piece.king:
            moves.update(self._traverse_left(row + 1, min(row + 3, ROWS), 1, piece.color, left))
            moves.update(self._traverse_right(row + 1, min(row + 3, ROWS), 1, piece.color, right))
    
        return moves

    def _traverse_left(self, start, stop, step, color, left, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0:
                break
            
            current = self.board[r][left]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, left)] = last + skipped
                else:
                    moves[(r, left)] = last
                
                if last:
                    if step == -1:
                        row = max(r-3, -1)
                    else:
                        row = min(r+3, ROWS)
                    moves.update(self._traverse_left(r+step, row, step, color, left-1, skipped=last))
                    moves.update(self._traverse_right(r+step, row, step, color, left+1, skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            left -= 1
        
        return moves

    def _traverse_right(self, start, stop, step, color, right, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= COLS:
                break
            
            current = self.board[r][right]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, right)] = last + skipped
                else:
                    moves[(r, right)] = last
                
                if last:
                    if step == -1:
                        row = max(r-3, -1)
                    else:
                        row = min(r+3, ROWS)
                    moves.update(self._traverse_left(r+step, row, step, color, right-1, skipped=last))
                    moves.update(self._traverse_right(r+step, row, step, color, right+1, skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            right += 1
        
        return moves
    
    def remove(self, pieces, visual=True):
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if visual:
                self.update_piece_visual(piece.row, piece.col)
            if piece != 0:
                if piece.color == RED:
                    self.red_left -= 1
                else:
                    self.black_left -= 1
    
    def winner(self):
        if self.red_left <= 0:
            return BLACK
        elif self.black_left <= 0:
            return RED
        
        return None
    
    def evaluate(self):
        return self.black_left - self.red_left + (self.black_kings * 0.5 - self.red_kings * 0.5)

    def get_all_valid_moves(self, color):
        moves = []
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.color == color:
                    valid_moves = self.get_valid_moves(piece)
                    for move, skipped in valid_moves.items():
                        moves.append( (piece, move, skipped) )
        return moves

    def get_all_pieces(self, color):
        pieces = []
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.color == color:
                    pieces.append(piece)
        return pieces
