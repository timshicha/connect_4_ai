
from board.board import Board
from minimax import Minimax_Agent

# Play against the Minimax agent

board = Board()
agent = Minimax_Agent(int(input("Enter search depth: ")), 1)

board.print_board()

# Play until the game is over
while(1):
    
    # Agent turn
    if(board.get_turn() == 1):
        best_move = agent.get_move(board)
        print("Agent's move:", best_move)
        board.move(best_move)
    # User turn
    else:
        move = int(input("\nYour turn. Your move: "))
        while(move not in board.get_legal_moves()):
            move = int(input("Illegal move. Try again: "))
        board.move(move)
        
    board.print_board()
    
    # Check end game conditions
    if(board.check_win(-1)):
        print("You win!")
        break
    elif(board.check_win(1)):
        print("Agent wins!")
        break
    elif(board.check_full()):
        print("Tie game.")
        break
    