import numpy as np
import random

ROWS = 6
COLUMNS = 7

# A connect 4 board.
# Filling the board: -1 is opponent, 0 is empty, 1 is the agent
class Board:


    def __init__(self):
        self.__board = np.zeros((ROWS,COLUMNS), dtype=int) # (First row is bottom row)
        self.__top = np.zeros(COLUMNS, dtype=int) # Lowest empty row of this column (i.e., where a piece would fall)
        self.__history = [] # Allows us to simulate and undo moves
        self.__turn = random.choice([-1, 1])
    
    
    def print_board(self):
        print(self.__board)
    
    
    # Swap turn: -1 -> 1, 1 -> -1
    def __swap_turn(self):
        if(self.__turn == 1): self.__turn = -1
        else: self.__turn = 1
        
    # Returns the legal moves (i.e., columns that are not full)
    def get_legal_moves(self):
        legal_moves = []
        # For each column
        for column in range(COLUMNS):
            # Examine the piece in the top row of this column
            if(self.__board[ROWS - 1][column] == 0):
                legal_moves.append(column)
        return legal_moves
    
    
    # Make a move (assume the move is legal, otherwise a crash may occur)
    def move(self, column):
        row = self.__top[column]
        self.__board[row][column] = self.__turn # Make the move
        self.__history.append([row, column]) # Store move to history
        self.__top[column] += 1 # New drop location will be one row higher
        self.__swap_turn()
        
    
    # Undo one move (the most recent one)
    def unmove(self):
        if(len(self.__history) == 0): return # Nothing to undo
        [row, column] = self.__history.pop() # Remove move from history
        self.__board[row][column] = 0 # Clear move
        self.__top[column] -= 1 # Update new drop location
        self.__swap_turn()
        
    
    # Determine if the board is full
    def check_full(self):
        # If at least one column not full, return not full
        for column in range(COLUMNS):
            if(self.__top[column] < ROWS): return 0
        return 1
    
    
    # Determine if a player won
    def check_win(self, player):
        # Check vertical wins (go through each column)
        for column in range(COLUMNS):
            for bottom_piece_row in range(0, ROWS - 3):
                win = 1
                for row in range(bottom_piece_row, bottom_piece_row + 4):
                    if(self.__board[row][column] != player):
                        win = 0
                        break
                if(win == 1): return 1
        # Check horizontal wins (go through each row)
        for row in range(ROWS):
            for leftmost_piece_column in range(0, COLUMNS - 3):
                win = 1
                for column in range(leftmost_piece_column, leftmost_piece_column + 4):
                    if(self.__board[row][column] != player):
                        win = 0
                        break
                if(win == 1): return 1
        # Check diagonal (/) wins
        for bottom_piece_row in range(ROWS - 3):
            for leftmost_piece_column in range(0, COLUMNS - 3):
                win = 1
                row = bottom_piece_row
                column = leftmost_piece_column
                for i in range(4):
                    if(self.__board[row][column] != player):
                        win = 0
                        break
                    row += 1
                    column += 1
                if(win == 1): return 1
        # Check diagonal (\) wins
        for bottom_piece_row in range(ROWS - 3):
            for rightmost_piece_column in range(3, COLUMNS):
                win = 1
                row = bottom_piece_row
                column = rightmost_piece_column
                for i in range(4):
                    if(self.__board[row][column] != player):
                        win = 0
                        break
                    row += 1
                    column -= 1
                if(win == 1): return 1
        # If no win
        return 0