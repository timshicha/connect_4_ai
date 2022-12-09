
from board.board import Board
from minimax import Minimax_Agent



board = Board()
agent = Minimax_Agent(int(input("Enter search depth: ")), 1)

board.print_board()

while(1):
    
    if(board.get_turn() == 1):
        best_move = agent.get_move(board)
        print("Agent's move:", best_move)
        board.move(best_move)
        
    else:
        move = int(input("\nYour turn. Your move: "))
        while(move not in board.get_legal_moves()):
            move = int(input("Illegal move. Try again: "))
        board.move(move)
        
    board.print_board()
    
    if(board.check_win(-1)):
        print("You win!")
        break
    elif(board.check_win(1)):
        print("Agent wins!")
        break
    elif(board.check_full()):
        print("Tie game.")
        break
    