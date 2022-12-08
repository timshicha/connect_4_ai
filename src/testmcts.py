
from board.board import Board
from mcts import MCTS_Agent
from minimax import Minimax_Agent
import random


agent = MCTS_Agent()

board = Board()

while(1):
    board.print_board()
    if(board.get_turn() == 1):
        board.move(int(input("Move:")))
        if(board.check_win(1)):
            print("You win!")
            break
    else:
        a = input("Agent: ")
        if(a == ""):
            move = agent.get_move(board, 10000)
        else:
            move = int(a)
        board.move(move)
        print("Agent moves:", move)
        if(board.check_win(-1)):
            print("Agent wins!")
            break
        
    if(board.check_full()):
        print("Tie game")
        break
