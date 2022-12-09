# Have the agents battle entire games

from board.board import Board
from minimax import Minimax_Agent
from mcts import MCTS_Agent



# Battle 2 games, return the first agent's wins, second agent's wins, and ties
def battle_agents(agent1_move_rule, agent2_move_rule):
    
    start = [-1, 1]
    agent1_wins = 0
    agent2_wins = 0
    ties = 0
    # Agent 1 will be -1, agent 2 will be 1
    
    for starting_player in start:
        board = Board(starting_player)
        
        while(1):
            # Check turn
            turn = board.get_turn()
            
            # If first agent's turn
            if(turn == -1):
                move = agent1_move_rule(board)
                board.move(move)
                # Did agent win?
                if(board.check_win(turn)):
                    agent1_wins += 1
                    break
            # If second agent's turn
            else:
                move = agent2_move_rule(board)
                board.move(move)
                # Did agent win?
                if(board.check_win(turn)):
                    agent2_wins += 1
                    break
            # If tie
            if(board.check_full()):
                ties += 1
                break
    return agent1_wins, agent2_wins, ties



print("Agent 1 is Minimax.")
depth = int(input("Search depth: "))
agent1_move_rule = Minimax_Agent(depth).get_move

print("Agent 2 is Monte-Carlo TS.")
iterations = int(input("Number of iterations: "))
agent2_move_rule = MCTS_Agent(iterations).get_move

number_of_games = int(input("Number of games: "))
agent1_wins = 0
agent2_wins = 0
ties = 0

for game in range(number_of_games):
    new_a1_wins, new_a2_wins, new_ties = battle_agents(agent1_move_rule, agent2_move_rule)
    agent1_wins += new_a1_wins
    agent2_wins += new_a2_wins
    ties += new_ties

print("Minimax agent won", agent1_wins, "games.")
print("Monte-Carlo TS agent won", agent2_wins, "games.")
print("There were", ties, "ties.")