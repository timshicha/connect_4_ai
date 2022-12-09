
from board.board import Board
from mcts import MCTS_Agent

# Play against the MCTS agent

board = Board()
agent = MCTS_Agent(int(input("Enter the number of iterations: ")))
print("You are X")
# Play until the game is over
while(1):
    board.print_board()
    # If user's turn
    if(board.get_turn() == 1):
        board.move(int(input("Move:")))
        # User win
        if(board.check_win(1)):
            print("You win!")
            break
    # If agent's turn
    else:
        move = agent.get_move(board)
        board.move(move)
        print("Agent moves:", move)
        # Agent win
        if(board.check_win(-1)):
            print("Agent wins!")
            break
    # If tie
    if(board.check_full()):
        print("Tie game")
        break
