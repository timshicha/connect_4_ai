import numpy as np
import random
from colorama import Fore


ROWS = 6 # Limit to 10 or less (heuristic may become bad)
COLUMNS = 7

# A connect 4 board.
# Filling the board: -1 is opponent, 0 is empty, 1 is the agent
class Board:


    def __init__(self, starting_player=None):
        self.__board = np.zeros((ROWS,COLUMNS), dtype=int) # (First row is bottom row)
        self.__top = np.zeros(COLUMNS, dtype=int) # Lowest empty row of this column (i.e., where a piece would fall)
        self.__history = [] # Allows us to simulate and undo moves
        if(starting_player == None):
            self.__turn = random.choice([-1, 1])
        else:
            self.__turn = starting_player
    
    
    # Return a board in the form of an array
    def get_board(self):
        return np.matrix.flatten(self.__board)
    
    # Print the board in a way that's easy for humans to understand.
    def print_board(self):
        def filter(number):
            if(number == 1):
                return Fore.RED + 'X' + Fore.RESET
            if(number == -1):
                return Fore.YELLOW + 'O' + Fore.RESET
            if(number == 0):
                return '.'
        for row in range(ROWS - 1, -1, -1):
            for column in range(COLUMNS):
                print(filter(self.__board[row][column]), end=" ")
            print()
        print("\n0 1 2 3 4 5 6")
    
    
    # Swap turn: -1 -> 1, 1 -> -1
    def __swap_turn(self):
        if(self.__turn == 1): self.__turn = -1
        else: self.__turn = 1
        
    
    # Get the current player's turn
    def get_turn(self):
        return self.__turn
        
    # Returns the legal moves (i.e., columns that are not full)
    def get_legal_moves(self):
        legal_moves = []
        # For each column
        for column in range(COLUMNS):
            # Examine the piece in the top row of this column
            if(self.__board[ROWS - 1, column] == 0):
                legal_moves.append(column)
        return legal_moves
    
    
    # Make a move (assume the move is legal, otherwise a crash may occur)
    def move(self, column):
        row = self.__top[column]
        self.__board[row, column] = self.__turn # Make the move
        self.__history.append([row, column]) # Store move to history
        self.__top[column] += 1 # New drop location will be one row higher
        self.__swap_turn()
        
    
    # Undo one move (the most recent one)
    def unmove(self):
        if(len(self.__history) == 0): return # Nothing to undo
        [row, column] = self.__history.pop() # Remove move from history
        self.__board[row, column] = 0 # Clear move
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
                    if(self.__board[row, column] != player):
                        win = 0
                        break
                if(win == 1): return 1
        # Check horizontal wins (go through each row)
        for row in range(ROWS):
            for leftmost_piece_column in range(0, COLUMNS - 3):
                win = 1
                for column in range(leftmost_piece_column, leftmost_piece_column + 4):
                    if(self.__board[row, column] != player):
                        win = 0
                        break
                if(win == 1): return 1
        # Check diagonal (/) wins
        for bottom_piece_row in range(0, ROWS - 3):
            for leftmost_piece_column in range(0, COLUMNS - 3):
                win = 1
                row = bottom_piece_row
                column = leftmost_piece_column
                for i in range(4):
                    if(self.__board[row, column] != player):
                        win = 0
                        break
                    row += 1
                    column += 1
                if(win == 1): return 1
        # Check diagonal (\) wins
        for bottom_piece_row in range(0, ROWS - 3):
            for rightmost_piece_column in range(3, COLUMNS):
                win = 1
                row = bottom_piece_row
                column = rightmost_piece_column
                for i in range(4):
                    if(self.__board[row, column] != player):
                        win = 0
                        break
                    row += 1
                    column -= 1
                if(win == 1): return 1
        # If no win
        return 0
    
    
    # Apply the heuristic. Specify which heuristic (there are a few
    # different heuristic functions).
    def heuristic(self, heuristic_number):
        if(heuristic_number == 0): return self.__heuristic0_1_2(version=0)
        if(heuristic_number == 1): return self.__heuristic0_1_2(version=1)
        if(heuristic_number == 2): return self.__heuristic0_1_2(version=2)
    
        
    
    # Heuristic 1:
    # Gives a point for each 4-in-a-row minus one piece (must be empty).
    # In version 0, it gives no additiona points for pieces in the middle column.
    # In version 1, it gives points for each piece in the middle column.
    # In version 2, it gives points only for the bottom 4 piece in the middle
    # column since top middle pieces might not mean much.
    def __heuristic0_1_2(self, version):
        score = 0
        # Look for 4-in-a-row patterns where either player has
        # 3 of their pieces and the last one is empty.
        #
        # Check vertical in each column:
        for column in range(COLUMNS):
            # If fewer than 3 pieces in this column, it's not possible:
            if(self.__top[column] < 3):
                continue
            eval = self.__board[self.__top[column] - 1, column] +\
                self.__board[self.__top[column] - 2, column] +\
                self.__board[self.__top[column] - 3, column]
            if(eval == 3): score += 1
            elif(eval == -3): score -= 1
        # Check horizontals in each row:
        for row in range(ROWS):
            for leftmost_piece_column in range(0, COLUMNS - 3):
                # Pieces must add up to 3
                eval = self.__board[row, leftmost_piece_column] +\
                    self.__board[row, leftmost_piece_column + 1] +\
                    self.__board[row, leftmost_piece_column + 2] +\
                    self.__board[row, leftmost_piece_column + 3]
                if(eval == 3): score += 1
                elif(eval == -3): score -= 1
        # Check diagonal (/) wins:
        for bottom_piece_row in range(0, ROWS - 3):
            for leftmost_piece_column in range(0, COLUMNS - 3):
                eval = self.__board[bottom_piece_row, leftmost_piece_column] +\
                    self.__board[bottom_piece_row + 1, leftmost_piece_column + 1] +\
                    self.__board[bottom_piece_row + 2, leftmost_piece_column + 2] +\
                    self.__board[bottom_piece_row + 3, leftmost_piece_column + 3]
                if(eval == 3): score += 1
                elif(eval == -3): score -= 1
        # Check diagonal (\) wins:
        for bottom_piece_row in range(0, ROWS - 3):
            for rightmost_piece_column in range(3, COLUMNS):
                eval = self.__board[bottom_piece_row, rightmost_piece_column] +\
                    self.__board[bottom_piece_row + 1, rightmost_piece_column - 1] +\
                    self.__board[bottom_piece_row + 2, rightmost_piece_column - 2] +\
                    self.__board[bottom_piece_row + 3, rightmost_piece_column - 3]
                if(eval == 3): score += 1
                elif(eval == -3): score -= 1
        #
        # Finally, give points for having pieces in the middle column,
        # giving more points to lower rows:
        if(version == 1):
            weight = 1
            for row in range(ROWS):
                score += self.__board[row, int(COLUMNS / 2)] * weight
                weight -= 0.1
        elif(version == 2):
            weight = 1
            for row in range(4):
                score += self.__board[row, int(COLUMNS / 2)] * weight
                weight -= 0.1
        return score
                