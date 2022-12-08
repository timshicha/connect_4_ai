
from board.board import Board
from mcts import MCTS_Agent
from minimax import Minimax_Agent
import random


agent = MCTS_Agent()

board = Board()

agent.get_move(board, 10000)