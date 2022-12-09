
from board.board import Board, ROWS, COLUMNS
from math import inf

# Instead of inf, use big value so that decreasing it has an impact.
# Useful for choosing paths that lead to shortest win or longest loss.
big_value = 10000000
# Decrease big value by 100 per turn until we reach 100000
decrease_above = 100000

class Minimax_Agent:
    
    
    def __init__(self, search_depth, heuristic_number=1):
        self.__search_depth = search_depth
        self.__heuristic_number = heuristic_number
        
        
    # Return value of the agent's best move.
    # If we find a value >= the kickout value, stop immidiately
    # and return that value (alpha-beta pruning).
    # Depth_left tells us how much farther down the tree we will
    # search before applying the heuristic.
    def max_move(self, board, kickout_value, depth_left, heuristic_number):
        max_value = -big_value
        legal_moves = board.get_legal_moves()
        
        # Try each move:
        for move in legal_moves:
            turn = board.get_turn()
            board.move(move) # Make the move
            # If this was a winning move, just return (guaranteed best value).
            if(board.check_win(turn)):
                board.unmove()
                return big_value
            # If tie, return 0
            elif(board.check_full()):
                board.unmove()
                return 0
            # Otherwise we need to play-out or estimate.
            # If we reached max search depth, apply heuristic:
            if(depth_left == 0):
                max_value = max(max_value, board.heuristic(heuristic_number))
            # Otherwise play out:
            else:
                estimate = self.min_move(board, max_value, depth_left - 1, heuristic_number)
                if(estimate > decrease_above):
                    estimate -= 100
                max_value = max(max_value, estimate)
            board.unmove() # Undo the simulation move
            # If we can prune:
            if(max_value > kickout_value):
                return max_value
        return max_value

        
    
    def min_move(self, board, kickout_value, depth_left, heuristic_number):
        min_value = big_value
        legal_moves = board.get_legal_moves()
        
        # Try each move:
        for move in legal_moves:
            turn = board.get_turn()
            board.move(move) # Make the move
            # If this was a winning move (losing for agent), just
            # return (guaranteed worst value).
            if(board.check_win(turn)):
                board.unmove()
                return -big_value
            # If tie, return 0
            elif(board.check_full()):
                board.unmove()
                return 0
            # Otherwise we need to play-out or estimate.
            # If we reached max search depth, apply heuristic:
            if(depth_left == 0):
                min_value = min(min_value, board.heuristic(heuristic_number))
            # Otherwise play out:
            else:
                estimate = self.max_move(board, min_value, depth_left - 1, heuristic_number)
                if(estimate < -decrease_above):
                    estimate += 100
                min_value = min(min_value, estimate)
            board.unmove() # Undo the simulation move
            # If we can prune:
            if(min_value < kickout_value):
                return min_value
        return min_value



    # Get the best move for player given a board.
    def get_move(self, board):
        # Return the move that's closer to the middle. This will help
        # settle ties, since middle moves are generally prefered.
        def better_move(move1, move2):
            if(move1 == None): return move2
            order = [3,2,4,1,5,0,7]
            for move in order:
                if(move1 == move): return move1
                if(move2 == move): return move2
            return move1

        max_value = -big_value
        best_move = None # Ties will be settled by choosing middle-most column.
        legal_moves = board.get_legal_moves()
        
        # Try each move:
        for move in legal_moves:
            turn = board.get_turn()
            board.move(move) # Make the move
            # If this was a winning move, just return (guaranteed best value).
            # If full, this must be the only move, so also okay to return.
            if(board.check_win(turn) or board.check_full()):
                board.unmove()
                return move
            # Otherwise we need to play-out or estimate.
            # If we reached max search depth, apply heuristic:
            if(self.__search_depth == 0):
                estimate = board.heuristic(self.__heuristic_number)
                # If new best move found
                if(estimate > max_value):
                    max_value = estimate
                    best_move = move
                # If equally good best move found, favor middle move
                elif(estimate == max_value):
                    max_value = estimate
                    best_move = better_move(best_move, move)
            # Otherwise play out:
            else:
                estimate = self.min_move(board, max_value, self.__search_depth - 1, self.__heuristic_number)
                if(estimate > decrease_above):
                    estimate -= 100
                # If new best move found
                if(estimate > max_value):
                    max_value = estimate
                    best_move = move
                # If equally good best move found, favor middle move
                elif(estimate == max_value):
                    max_value = estimate
                    best_move = better_move(best_move, move)
            board.unmove() # Undo the simulation move
        return best_move

