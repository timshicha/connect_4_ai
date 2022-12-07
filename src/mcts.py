
from board.board import Board
import numpy as np


class MCTS_Agent:
    
    def __init__(self):
        pass
    
    
    # Simulate a game, given the action policy the agent follows
    # and the action policy the opponent follows.
    # agent_player refers to the player the agent is (-1 or 1).
    # Assumes it's the agent's turn to move.
    def simulate(self, board, agent_policy, opponent_policy, agent_player=1):
        
        depth = 0
        result = None
        # Loop until the game is over (win or tie).
        while(1):
            turn = board.get_turn()
            # If opponent turn, let them move
            if(turn != agent_player):
                board.move(opponent_policy(board))
                depth += 1
                # If opponent won
                if(board.check_win(-agent_player)):
                    result = 0
                    break
            # If agent's turn
            else:
                board.move(agent_policy(board))
                depth += 1
                # If agent won
                if(board.check_win(agent_player)):
                    result = 1
                    break
            # Check for tie
            if(board.check_full()):
                result = 0.5
                break
        # Undo the moves:
        for i in range(depth):
            board.unmove()
        return result
            