
from board import Board
   
board = Board()

while(1):
    a = input()
    if(a == 'move'):
        print("Legal moves:", board.get_legal_moves())
        board.move(int(input()))
    elif(a == "unmove"):
        board.unmove()
    board.print_board()
    print("Heuristic:", board.heuristic())