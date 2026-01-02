"""
Board Module for Console Checkers.

This module handles the game state, including the board representation,
piece movement, rule validation, and rendering to the console.
"""

import bext
import colorama
from constants import *

class Piece:
    """
    Represents a single checker piece.

    Attributes:
        row (int): The row index of the piece.
        col (int): The column index of the piece.
        color (int): The color of the piece (RED or BLACK).
        king (bool): Whether the piece has been promoted to a king.
    """
    def __init__(self, row, col, color):
        """
        Initializes a new Piece.

        Args:
            row (int): Row index.
            col (int): Column index.
            color (int): Color constant (RED or BLACK).
        """
        self.row = row
        self.col = col
        self.color = color
        self.king = False

    def make_king(self):
        """Promotes the piece to a king."""
        self.king = True

    def draw(self, x, y, bg_color=None):
        """
        Draws the piece at the specified screen coordinates.

        Args:
            x (int): The x-coordinate on the terminal screen.
            y (int): The y-coordinate on the terminal screen.
            bg_color (str, optional): ANSI background color code. Defaults to None.
        """
        try:
            bext.goto(x, y)
            symbol = KING_SYMBOL if self.king else PIECE_SYMBOL
            color = COLOR_RED if self.color == RED else COLOR_BLACK
            
            if bg_color:
                print(f"{bg_color}{color}{symbol}{COLOR_RESET}", end='')
            else:
                print(f"{color}{symbol}{COLOR_RESET}", end='')
        except:
            pass

class Board:
    """
    Represents the game board and logic.

    Attributes:
        board (list): 2D list representing the grid.
        red_left (int): Number of red pieces remaining.
        black_left (int): Number of black pieces remaining.
        red_kings (int): Number of red kings.
        black_kings (int): Number of black kings.
        last_move (tuple): Stores the start and end coordinates of the last move for highlighting.
    """
    def __init__(self):
        """Initializes the board and sets up the pieces."""
        self.board = []
        self.red_left = self.black_left = 12
        self.red_kings = self.black_kings = 0
        self.last_move = None
        self.create_board()

    def create_board(self):
        """Populates the board with pieces in their starting positions."""
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
        """Renders the entire board to the console."""
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
                if self.last_move and ((row, col) == self.last_move[0] or (row, col) == self.last_move[1]):
                    bg_color = COLOR_HIGHLIGHT
                else:
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
        """Draws all pieces on the board."""
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    screen_x = BOARD_OFFSET_X + 1 + col * 4 + 1
                    screen_y = BOARD_OFFSET_Y + 1 + row * 2
                    
                    if self.last_move and ((row, col) == self.last_move[0] or (row, col) == self.last_move[1]):
                        bg_color = COLOR_HIGHLIGHT
                    else:
                        bg_color = COLOR_BOARD_LIGHT if (row + col) % 2 == 0 else COLOR_BOARD_DARK
                        
                    piece.draw(screen_x, screen_y, bg_color)

    def update_piece_visual(self, row, col):
        """
        Updates the visual representation of a specific square.

        Args:
            row (int): Row index.
            col (int): Column index.
        """
        screen_x = BOARD_OFFSET_X + 1 + col * 4 + 1
        screen_y = BOARD_OFFSET_Y + 1 + row * 2
        
        piece = self.board[row][col]
        
        bext.goto(screen_x - 1, screen_y)
        
        if self.last_move and ((row, col) == self.last_move[0] or (row, col) == self.last_move[1]):
            bg_color = COLOR_HIGHLIGHT
        else:
            bg_color = COLOR_BOARD_LIGHT if (row + col) % 2 == 0 else COLOR_BOARD_DARK
            
        print(f"{bg_color}   {COLOR_RESET}", end='')
        
        if piece != 0:
            piece.draw(screen_x, screen_y, bg_color)

    def move(self, piece, row, col, visual=True):
        """
        Moves a piece to a new location.

        Args:
            piece (Piece): The piece to move.
            row (int): The target row.
            col (int): The target column.
            visual (bool, optional): Whether to update the display. Defaults to True.
        """
        if visual:
            if self.last_move:
                # Clear previous highlight
                prev_start, prev_end = self.last_move
                self.last_move = None
                self.update_piece_visual(prev_start[0], prev_start[1])
                self.update_piece_visual(prev_end[0], prev_end[1])
            
            # Set new highlight
            self.last_move = ((piece.row, piece.col), (row, col))

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
        """Returns the piece at the given coordinates."""
        return self.board[row][col]

    def get_valid_moves(self, piece):
        """
        Calculates all valid moves for a specific piece.

        Args:
            piece (Piece): The piece to check.

        Returns:
            dict: A dictionary where keys are target coordinates (row, col)
                  and values are lists of skipped pieces (captures).
        """
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
        """Helper function to check diagonal moves to the left."""
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
        """Helper function to check diagonal moves to the right."""
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
        """
        Removes pieces from the board (e.g., after capture).

        Args:
            pieces (list): List of Piece objects to remove.
            visual (bool, optional): Whether to update the display. Defaults to True.
        """
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
        """
        Checks if there is a winner.

        Returns:
            int or None: The color of the winner (RED or BLACK), or None if no winner yet.
        """
        if self.red_left <= 0:
            return BLACK
        elif self.black_left <= 0:
            return RED
        
        return None
    
    def evaluate(self):
        """
        Simple evaluation function for the board state.

        Returns:
            float: Score based on piece count.
        """
        return self.black_left - self.red_left + (self.black_kings * 0.5 - self.red_kings * 0.5)

    def get_all_valid_moves(self, color):
        """
        Gets all valid moves for a player.

        Args:
            color (int): The player's color.

        Returns:
            list: List of tuples (piece, move, skipped).
        """
        moves = []
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.color == color:
                    valid_moves = self.get_valid_moves(piece)
                    for move, skipped in valid_moves.items():
                        moves.append( (piece, move, skipped) )
        return moves

    def get_all_pieces(self, color):
        """Returns a list of all pieces belonging to a specific color."""
        pieces = []
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.color == color:
                    pieces.append(piece)
        return pieces
