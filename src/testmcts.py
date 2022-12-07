
from board.board import Board
from mcts import MCTS_Agent
from minimax import Minimax_Agent
import random


def random_policy(board):
    legal_moves = board.get_legal_moves()
    return random.choice(legal_moves)

mtcs_agent = MCTS_Agent()
minimax_agent = Minimax_Agent(0,1)


board = Board()

for i in range(100):
    print(mtcs_agent.simulate(Board(), random_policy, random_policy))