# Monte-Carlo Tree Search to play connect-4

import numpy as np
import random
from math import inf
from board.board import Board



class MCTS_Agent:
    
    def __init__(self, number_hidden_nodes, hidden_layer_weights=None, output_layer_weights=None, output_layer_bias_weight=None, activation_function=None):
        # Initialize the Q-network
        if(hidden_layer_weights == None):
            self.__number_hidden_nodes = number_hidden_nodes
            # Create weight matrices
            if(hidden_layer_weights == None or output_layer_weights == None or output_layer_bias_weight == None):
                # Set random weights
                self.__hidden_layer_weights = np.random.rand((self.__number_hidden_nodes, 44))/10 + 5
                self.__output_layer_weights = np.random.rand(self.__number_hidden_nodes)/10 + 5
                self.__output_layer_bias_weight = np.random.rand(1)/10 + 5
            else:
                self.__hidden_layer_weights = hidden_layer_weights
                self.__output_layer_weights = output_layer_weights
                self.__output_layer_bias_weight = output_layer_bias_weight
            # Set activation function
            if(activation_function == None):
                self.__activation_function = self.__sigmoid
            else:
                self.__activation_function = activation_function
                
        # Learning rate. This can be changed using the set_learning_rate function
        self.__learning_rate = 0.01
        self.__exploration = 0.3 # Epsilon, i.e., chance of exploration
        self.__discount = 0.8
           
           
    # Default activation function will be sigmoid 
    def __sigmoid(z):
        return 1 / (1 + np.exp(-z))
    
    
    # Set parameters of exploring and training the Q-Network
    def set_parameters(self, learning_rate=None, exploration=None, discount=None):
        if(learning_rate != None): self.__learning_rate = learning_rate
        if(exploration != None): self.__exploration = exploration
        if(discount != None): self.__discount = discount
        
        
    # Train on a single state (a single instance of a connect 4 board)
    def train_single_example(self, board, action, target_q_value):
        state_action = np.append(board.get_board(), action, 1)
        # Propogation
        hidden_activation = self.__activation_function\
            (np.dot(state_action, self.__hidden_layer_weights.transpose()))
        output_activation = np.dot(hidden_activation, self.__output_layer_weights.transpose()) + self.__output_layer_bias_weight
        
        # Determine the errors
        output_error = output_activation * (1- output_activation) * (target_q_value - output_activation)
        hidden_error = hidden_activation * (1 - hidden_activation) * np.dot(self.__output_layer_weights, output_error)
        # Calculate weight changes
        output_update = self.__learning_rate * np.multiply.outer(output_error, hidden_activation)
        bias_update = self.__learning_rate * output_error
        hidden_update = self.__learning_rate * np.multiply.outer(hidden_error, state_action)
        # Update weights
        self.__output_layer_weights = self.__output_layer_weights + output_update
        self.__output_layer_bias_weight = self.__output_layer_bias_weight + bias_update
        self.__hidden_layer_weights = self.__hidden_layer_weights + hidden_update
        
        
    # Play a game and train from it given an opponent's rule (as a function) for playing.
    def train_game(self, opponent_policy):
        
        def step(current_board, opponent_policy, agent_player):
            # If the opponent's turn:
            if(current_board.get_turn() != agent_player):
                current_board.move(opponent_policy(current_board))
                # If opponent won:
                if(current_board.check_win(-1)):
                    current_board.unmove()
                    return -1, -1 # Reward is -1 for loss, max Q(s,a) is -1 since only loss is possible
                # If tie
                elif(current_board.check_full()):
                    current_board.unmove()
                    return 0, 0 # Reward is 0, max Q(s,a) is 0
                # If the game continues
                else:
                    reward, max_q = step(current_board, opponent_policy)
                    current_board.unmove()
                    return reward, max_q
            
            # Otherwise if it's the agent's turn
            agent_action = None
            # With probability 1 - epsilon, choose the best action
            if(random.random() > self.__exploration):
                # Find the maximum Q(s,a)
                best_actions = []
                best_actions_q = -inf
                # Examine each action for this state
                for action in current_board.get_legal_moves():
                    q = self.estimate_q_value(current_board, action)
                    # If better action found, replace previous actions
                    if(q > best_actions_q):
                        best_actions = [action]
                        best_actions_q = q
                    # If this action is the same as previous best actions, add it
                    elif(q == best_actions_q):
                        best_actions.append(action)    
                # Choose a best action at random
                agent_action = random.choice(best_actions)
            # Otherwise choose random action with equal probability
            else:
                agent_action = random.choice(current_board.get_legal_moves())
            
            # Perform the action
            current_board.move(agent_action)
            # If agent won
            if(current_board.check_win(agent_player)):
                current_board.unmove()
                self.train_single_example(current_board, agent_action, 1) # Train Q-Netowrk
                return 1, 1 # Reward is 1 for win, max Q(s,a) is 1 since only win is possible
            # If tie
            elif(current_board.check_full()):
                current_board.unmove()
                self.train_single_example(current_board, agent_action, 0) # Train Q-Network
                return 0, 0
            
            # Otherwise the game continues. Have the opponent go and record what the game's
            # result was and what the best action value (max Q-value) of the next state is.
            reward, max_q = step(current_board, opponent_policy)
            # Find the max Q-value of current state to return to previous state
            best_action_value = -inf
            for action in current_board.get_legal_moves():
                action_value = self.estimate_q_value(current_board, action)
                if(action_value > best_action_value):
                    best_action_value = action_value
            # Undo the move
            current_board.unmove()
            # Train the Q-Netowrk
            target_q_value = reward + self.__discount * max_q
            self.train_single_example(current_board, action, target_q_value)
            
            return reward, best_action_value
    
        # Call recursive function to train on the game
        board = Board()
        step(board, opponent_policy, 1)
                    

    # Estimate the Q-value of a board given the state and action (move)
    def estimate_q_value(self, board, action):
        state_action = np.append(board.get_board(), action, 1)
        # Propogation
        hidden_activation = self.__activation_function\
            (np.dot(state_action, self.__hidden_layer_weights.transpose()))
        output_activation = np.dot(hidden_activation, self.__output_layer_weights.transpose()) + self.__output_layer_bias_weight
        return output_activation
        
        

        