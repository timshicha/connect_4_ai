
from board.board import Board
from minimax import Minimax_Agent
from mcts import MCTS_Agent
from time import time

# Quick tool to compare how long it takes for the two algorithms to run.


# Time how long it takes for minimax to return its best move on
# an empty board.
def time_minimax(board, depth):
    minimax_agent = Minimax_Agent(depth)
    start_time = time()
    minimax_agent.get_move(board)
    end_time = time()
    return end_time - start_time


# Time how long it takes for MCTS to return its best move on
# an empty board.
def time_mcts(board, iterations):
    mcts_agent = MCTS_Agent(iterations)
    start_time = time()
    mcts_agent.get_move(board)
    end_time = time()
    return end_time - start_time


print("Which algorithm?")
print("1) Minimax")
print("2) Monte-Carlo Tree Search")
selection = int(input("1 or 2: "))

if(selection == 1):
    depth = int(input("Depth: "))
    board = Board()
    print("Running...")
    time_elapsed = time_minimax(board, depth)
    print(f"Time: {time_elapsed}")
    
else:
    iterations = int(input("Number of iterations: "))
    board = Board()
    print("Running...")
    time_elapsed = time_mcts(board, iterations)
    print(f"Time: {time_elapsed}")