"""
Constants Module for Console Checkers.

This module defines all the constants used throughout the game, including
board dimensions, colors, symbols, and box-drawing characters.
"""

import colorama

colorama.init()

# Board Dimensions
ROWS = 8
COLS = 8
SQUARE_SIZE = 1

# Player Constants
RED = 1
BLACK = 2
EMPTY = 0

# Color Definitions
COLOR_RED = colorama.Fore.RED
COLOR_BLACK = colorama.Fore.BLUE
COLOR_RESET = colorama.Style.RESET_ALL
COLOR_BOARD_LIGHT = colorama.Back.WHITE
COLOR_BOARD_DARK = colorama.Back.BLACK
COLOR_HIGHLIGHT = colorama.Back.YELLOW

# Game Symbols
PIECE_SYMBOL = '●'
KING_SYMBOL = '♔'

# Box Drawing Characters
BOX_H = '─'
BOX_V = '│'
BOX_TL = '┌'
BOX_TR = '┐'
BOX_BL = '└'
BOX_BR = '┘'
BOX_TM = '┬'
BOX_BM = '┴'
BOX_LM = '├'
BOX_RM = '┤'
BOX_CROSS = '┼'

# Rendering Offsets
BOARD_OFFSET_X = 4
BOARD_OFFSET_Y = 2
