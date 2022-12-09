
from board.board import Board
from mcts import MCTS_Agent


board = Board()
agent = MCTS_Agent(int(input("Enter the number of iterations: ")))
print("You are X")

while(1):
    board.print_board()
    if(board.get_turn() == 1):
        board.move(int(input("Move:")))
        if(board.check_win(1)):
            print("You win!")
            break
    else:
        move = agent.get_move(board)
        board.move(move)
        print("Agent moves:", move)
        if(board.check_win(-1)):
            print("Agent wins!")
            break
        
    if(board.check_full()):
        print("Tie game")
        break
