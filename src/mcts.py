
from board.board import Board
import numpy as np
from math import sqrt, log, inf
import random



# MCTS builds a tree; these nodes will be used for the tree.
# score/possible is the favorability of this node.
# children is a list of child nodes. The index is the action, the
# element is the child node pointer.
class TreeNode: 
    def __init__(self, current_board):
        self.game_result = None # If game didn't end
        # If game ended, can't have children:
        # Check win for previous move's player (notice '-' sign)
        if(current_board.check_win(-current_board.get_turn())):
            self.game_result = 1
        elif(current_board.check_full()):
            self.game_result = 0.5
            
        self.score = 0 # Keep track of number of wins
        self.games = 0 # Keep track of number of games played
        # Create a dictionary of children.
        # Key is action, value is child TreeNode pointer
        self.children = None
            
    
    # Given the parent's (this node's) board, find out what the children are
    def create_children(self, current_board):
        legal_actions = current_board.get_legal_moves()
        self.children = {}
        for action in legal_actions:
            current_board.move(action)
            self.children[action] = TreeNode(current_board)
            current_board.unmove()
            
            
    # Calcualte how favorable it is to expand this node:
    # wi/ni + c * sqrt(lnNi / ni)
    # N is the total number of simulations through parent node.
    # c is the exploration paremter.
    def expansion_favorability(self, N, c):
        # If this is a winning board, "expand" this way all the time:
        if(self.game_result == 1):
            return 1
        # If tie, this would be the only move available. Return anything (0):
        elif(self.game_result == 0.5):
            return 0.5
        # If no games through this node have been played (divide by 0),
        # return out a decent number to encourage to expand this way at least
        # once:
        if(self.games == 0): return inf
        return self.score/self.games + c * sqrt(log(N) / self.games)
    
    
    # Get the action node we should expand next
    def choose_expansion(self, c):
        """
        # If we haven't created children yet, create children
        if(self.children == None):
            self.create_children(current_board)
        """
        # Now find and return the child with the maximum expansion favorability
        max_child = None
        max_child_favorability = -inf
        for child in self.children:
            child_favorability = self.children[child].expansion_favorability(self.games, c)
            if(child_favorability > max_child_favorability):
                max_child = child
                max_child_favorability = child_favorability
        return max_child
    
    
    # Get the favorability of choosing this action in a test-game
    def calculate_favorability(self):
        if(self.game_result == 1): return inf
        if(self.game_result == 0.5): return 0.5
        if(self.games == 0): return 0
        else: return self.score / self.games
        
        
class MCTS_Agent:
    
    def __init__(self, exploration_paremeter=sqrt(2)):
        self.__exploration_parameter = exploration_paremeter
    
    
    # Return the score from the opponent's perspective
    def opponent_score(self, score):
        if(score == 1): return 0
        if(score == 0): return 1
        return 0.5

    
    # Simulate a game given a board.
    # Must provide the caller, i.e., the player that called this simulation
    # function. We need this to assign the correct result value.
    def simulate(self, current_board, caller):
        depth = 0
        result = None
        # Loop until the game is over (win or tie).
        while(1):
            turn = current_board.get_turn()
            legal_moves = current_board.get_legal_moves()
            action = random.choice(legal_moves) # Make random move
            current_board.move(action)
            depth += 1
            # Check for win
            if(current_board.check_win(turn)):
                if(turn == caller): result = 1
                else: result = 0
                break
            # Check for tie
            if(current_board.check_full()):
                result = 0.5
                break
        # Undo the moves:
        for i in range(depth):
            current_board.unmove()
        return result


    # Called on a leaf treenode. If this leaf is a finished game, return the
    # result. Otherwise, simulate the game and update the treenode.
    def simulate_and_update_leaf(self, board, treenode):
        # If it's a win or tie, return result
        if(treenode.game_result == 1):
            return 1
        elif(treenode.game_result == 0.5):
            return 0.5
        # Otherwise, simulate and update the score and games played
        result = self.simulate(board, board.get_turn())
        result = self.opponent_score(result)
        treenode.score += result
        treenode.games += 1
        # Return the result as it would appear to the opponent:
        return result
        
        
    # Go down the tree, find a leaf, expand it and run a simulation on it
    def expand(self, current_board, treenode, c):
        # If this is a leaf, expand this leaf and run simulation. Exception: if
        # this is the end of a game, return the game result.
        if(treenode.children == None):
            if(treenode.game_result == 1): return 1
            if(treenode.game_result == 0.5): return 0.5
            # Otherwise, expand children
            treenode.create_children(current_board)
            # Choose random child to expand
            child = random.choice(list(treenode.children))
            current_board.move(child)
            # Run simulation on child
            result = self.simulate_and_update_leaf(current_board, treenode.children[child])
            result = self.opponent_score(result)
            treenode.score += result
            treenode.games += 1
            # Undo the move and return the result
            current_board.unmove()
            return result
        # Otherwise, this is not a leaf. We need to keep going until we find a leaf.
        # Choose an action and traverse in that direction:
        child = treenode.choose_expansion(c)
        current_board.move(child)
        result = self.expand(current_board, treenode.children[child], c)
        result = self.opponent_score(result)
        # Update this treenode's info, undo move, and return result to parent
        treenode.score += result
        treenode.games += 1
        current_board.unmove()
        return result
        
            
    # Given a board, make the best move.
    # Choose how many trials/simulations to play out.
    # Assumes the current board is not already a winning or tying board.
    def get_move(self, board, simulations, exploration_parameter=sqrt(2)):
        # Make a tree (root node) and create the children
        treenode = TreeNode(board)
        
        # Run expansion/simulation algorithm for specific number of moves
        for i in range(simulations):
            self.expand(board, treenode, exploration_parameter)
            
        max_child = None
        max_child_favorability = -inf    
        for child in treenode.children:
            favorability = treenode.children[child].calculate_favorability()
            if(favorability > max_child_favorability):
                max_child = child
                max_child_favorability = favorability
            print("Action:", child)
            print("   Favorability:", favorability)

        return max_child
    
            
            
            