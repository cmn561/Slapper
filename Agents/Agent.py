# -*- coding: utf-8 -*-
"""
Created on Sun Jul 14 18:08:16 2024

@author: Cristian Navarrete
"""

import numpy as np
import random
import functools as functools

#%% Agent Class Defintions (for learning the game)

## This Class is the default agent (i.e. all random decisions)
class DefaultAgent():    
    def __init__(self):
        self.agent_name = 'Default Agent'
        
    def get_agent_name(self):
        return self.agent_name
       
    def choose_action_per_policy(self, policy, new_y, new_x, haz_NE, haz_SE, haz_SW, haz_NW, h_onHazard):
        state = (new_y, new_x, haz_NE, haz_SE, haz_SW, haz_NW, h_onHazard)
        
        # if state in policy dictionary
        if (state in policy.keys()):
            return np.argmax(policy[state])     
            print('Chose Best Move')
        # if state not in policy dictionary
        else: 
            return random.randint(0,3)
            print('Chose Random Move')
        
## This Class is the Q-Learning agent 
class QAgent():
    def __init__(self, num_games, learn_rate, discount, epsilon, epsilon_decay, epsilon_min):
        self.num_games = num_games
        self.learn_rate = learn_rate
        self.discount = discount
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.epsilon_min = epsilon_min
        
        self.agent_name = 'Q Agent'

    def get_agent_name(self):
        return self.agent_name
    
    def choose_action(self, state, Q_table, current_epsilon):     
        # Choose action according to epsilon greedy
        random_roll=random.random()
        if (random_roll<current_epsilon):
            #Explore
            movement_ind = random.randint(0, 3)
        else:
            #Exploit (With Random Tiebreaker)
            Q_values = Q_table[state]
            movement_ind = np.random.choice(np.argwhere(Q_values == np.amax(Q_values)).flatten().tolist())
    
        return movement_ind
    
    def learn(self, game):
        
        trial_Q_table = {}
        trial_N_table = {}
        score_running_average = 0
        score_performance = np.empty((self.num_games,))      
        current_epsilon = self.epsilon
        
        for game_index in range(self.num_games):
            # new_y, new_x, haz_N, haz_E, haz_S, haz_W, haz_NE, haz_SE, haz_SW, haz_NW, score = game.initialize_agent_grid()
            new_y, new_x, haz_NE, haz_SE, haz_SW, haz_NW, h_onHazard, score = game.initialize_agent_grid()
                            
            done=False
            action = 0
            while (done != True):
            # while (num_moves < 4):
                # Given state, use epsilon-greedy method to choose an action
                # state = (new_y, new_x, haz_N, haz_E, haz_S, haz_W, haz_NE, haz_SE, haz_SW, haz_NW)
                state = (new_y, new_x, haz_NE, haz_SE, haz_SW, haz_NW, h_onHazard)
                # print('Current State is : ' + str(state))
                                    
                # Check if state has occured before
                state_action_Q = np.zeros((4,))
                if state in trial_Q_table.keys():
                    # Choose Move according to epsilon-greedy method
                    action = self.choose_action(state, trial_Q_table, current_epsilon)                       
                    state_action_Q = trial_Q_table[state]
                    trial_N_table[state] += 1
                else: 
                    # Choose Random Move if no record of this state before
                    action = random.randint(0, 3)
                    
                    trial_Q_table[state] = state_action_Q
                    trial_N_table[state] = 1
                                            
                # print('Action is : ' + str(action))
                # print('current_state ')
                # print(state)                        
                    
                # new_y, new_x, haz_N, haz_E, haz_S, haz_W, haz_NE, haz_SE, haz_SW, haz_NW, score, done = game.sim_move(action)
                # new_state = (new_y, new_x, haz_N, haz_E, haz_S, haz_W, haz_NE, haz_SE, haz_SW, haz_NW)
                new_y, new_x, haz_NE, haz_SE, haz_SW, haz_NW, h_onHazard, score, done = game.sim_move(action)
                new_state = (new_y, new_x, haz_NE, haz_SE, haz_SW, haz_NW, h_onHazard)

                # print('new_state ')
                # print(new_state)
                
                # Do Q-Learning (Get Current Reward and Expected Reward of new state)
                new_state_action_Q = np.zeros((4,))
                if new_state in trial_Q_table.keys():
                    new_state_action_Q = trial_Q_table[new_state]
                
                Q_retain = (1-self.learn_rate) * state_action_Q[action]
                Q_learn = self.learn_rate * (score + self.discount * max(new_state_action_Q))
                
                trial_Q_table[state][action] = Q_retain + Q_learn
                # V[current_y][current_x] = max(trial_Q_table[current_y][current_x])
                
                # print(game.environment)
            
                # num_moves+=1
                                    
                # Testing
                # if (state == (3,3,1,0,0,0,0) and action == 0):
                #     print('Cur State : {0}'.format(state))
                #     # print('Action is {0}'.format(action))
                #     print('Q {0}'.format(trial_Q_table[(3,3,1,0,0,0,0)]))
                #     print('New State : {0}'.format(new_state))
                #     print('Q {0}'.format(new_state_action_Q))
                    
                #     # print('Done is {0}'.format(done))
                #     # print('Score is {0}'.format(score))
                    
                #     print(Q_retain)
                #     print(Q_learn)
                    
                #     print('-----------------------------')
            ## end current game
            
            score_running_average = score_running_average + 1/(game_index+1) * (score-score_running_average)
            score_performance[game_index] = score_running_average
            
            # print('Game {0} has Score {1} with epsilon {2}'.format(game_index, score, current_epsilon))
        
            # Reduce epsilon (if over the min amount)
            if current_epsilon > self.epsilon_min:
                current_epsilon = current_epsilon * self.epsilon_decay
                
        ## end learning

        # Generate the average state-value table
        grid_state_value = np.zeros((6,6))
        grid_state_count = np.zeros((6,6))        
        
        for key in trial_Q_table.keys():
            # print(key)
            # print(trial_Q_table[key])
            y = key[0:1]
            x = key[1:2]
            
            max_value = np.max(trial_Q_table[key])
            # print(max_value)
            grid_state_count[y][x] += 1            
            grid_state_value[y][x] = grid_state_value[y][x] + 1/(grid_state_count[y][x]) * (max_value-grid_state_value[y][x])
            
        # print(grid_state_count)
        # print(grid_state_value)
        
            
        # Testing
        # print('=================================Q-Table Values==============================')
        # for key in trial_Q_table.keys():
        #     print(key)
        #     print(trial_Q_table[key])
            
        # agent.Q_table = trial_Q_table
        
        return trial_Q_table, grid_state_value, score_performance
        # return policy

    def choose_action_per_policy(self, policy, new_y, new_x, haz_NE, haz_SE, haz_SW, haz_NW, h_onHazard):
        state = (new_y, new_x, haz_NE, haz_SE, haz_SW, haz_NW, h_onHazard)
        
        # if state in policy dictionary
        if (state in policy.keys()):
            return np.argmax(policy[state])     
            print('Chose Best Move')
        # if state not in policy dictionary
        else: 
            return random.randint(0,3)
            print('Chose Random Move')


## This Class is the Double Q-Learning agent 
class DQAgent():
    def __init__(self, num_games, learn_rate, discount, epsilon, epsilon_decay, epsilon_min):
        self.num_games = num_games
        self.learn_rate = learn_rate
        self.discount = discount
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.epsilon_min = epsilon_min
    
        self.agent_name = 'Double Q Agent'
    
    def get_agent_name(self):
        return self.agent_name
    
    def choose_action(self, state, Q1_table, Q2_table, current_epsilon):     
        # Choose action according to epsilon greedy
        random_roll=random.random()
        if (random_roll<current_epsilon):
            #Explore
            movement_ind = random.randint(0, 3)
        else:
            #Exploit (With Random Tiebreaker)

            # Add the Q values for both q table to make a decision
            Q_values = np.add((Q1_table.get(state, False) or [0,0,0,0]), (Q2_table.get(state, False) or [0,0,0,0]))
            movement_ind = np.random.choice(np.argwhere(Q_values == np.amax(Q_values)).flatten().tolist())
        
        return movement_ind
    
    def learn(self, game): 
        trial_Q1_table = {}
        trial_Q2_table = {}
        trial_N_table = {}
        score_running_average = 0
        score_performance = np.empty((self.num_games,))      
        current_epsilon = self.epsilon
        
        for game_index in range(self.num_games):
            # new_y, new_x, haz_N, haz_E, haz_S, haz_W, haz_NE, haz_SE, haz_SW, haz_NW, score = game.initialize_agent_grid()
            new_y, new_x, haz_NE, haz_SE, haz_SW, haz_NW, h_onHazard, score = game.initialize_agent_grid()
                            
            done=False
            action = 0
            while (done != True):
            # while (num_moves < 4):
                # Given state, use epsilon-greedy method to choose an action
                # state = (new_y, new_x, haz_N, haz_E, haz_S, haz_W, haz_NE, haz_SE, haz_SW, haz_NW)
                state = (new_y, new_x, haz_NE, haz_SE, haz_SW, haz_NW, h_onHazard)
                # print('Current State is : ' + str(state))
                                    
                # Check if state has occured before
                state_action_Q = [0,0,0,0]
                if (state in trial_Q1_table.keys()) or (state in trial_Q2_table.keys()):
                    # Choose Move according to epsilon-greedy method
                    action = self.choose_action(state, trial_Q1_table, trial_Q2_table, current_epsilon)                       
                    trial_N_table[state] += 1
                else: 
                    # Choose Random Move if no record of this state before
                    action = random.randint(0, 3)
                    
                    trial_Q1_table[state] = state_action_Q
                    trial_Q2_table[state] = state_action_Q
                    trial_N_table[state] = 1
                                            
                # print('Action is : ' + str(action))
                # print('current_state ')
                # print(state)                        
                    
                # new_y, new_x, haz_N, haz_E, haz_S, haz_W, haz_NE, haz_SE, haz_SW, haz_NW, score, done = game.sim_move(action)
                # new_state = (new_y, new_x, haz_N, haz_E, haz_S, haz_W, haz_NE, haz_SE, haz_SW, haz_NW)
                new_y, new_x, haz_NE, haz_SE, haz_SW, haz_NW, h_onHazard, score, done = game.sim_move(action)
                new_state = (new_y, new_x, haz_NE, haz_SE, haz_SW, haz_NW, h_onHazard)

                # print('new_state ')
                # print(new_state)
                # print(score)      
                
                # Do Double Q-Learning (Get Current Reward and Expected Reward of new state and update ONE q table randomly)
                # Update Q1 Table (using Q2 new_state state-action values)
                if random.random() < .5:        
                    # print(state)
                    # print(trial_Q1_table.get(state, False) or [0,0,0,0])
                    # print(trial_Q1_table.get(state, False))
                    new_state_Q1_values = trial_Q1_table.get(new_state, False) or [0,0,0,0]
                    best_action_ind_new_state = np.random.choice(np.argwhere(new_state_Q1_values == np.amax(new_state_Q1_values)).flatten().tolist())
                    
                    # trial_Q1_table[state][action] = (trial_Q1_table.get(state, False) or [0,0,0,0])[action]
                    trial_Q1_table[state][action] = trial_Q1_table[state][action] + self.learn_rate * (score + self.discount*((trial_Q2_table.get(new_state, False) or [0,0,0,0])[best_action_ind_new_state]) - trial_Q1_table[state][action])
                    
                # Update Q2 Table (using Q1 new_state state-action values)
                else:
                    # print(state)
                    # print(trial_Q2_table.get(state, False) or [0,0,0,0])
                    # print(trial_Q1_table.get(state, False))
                    new_state_Q2_values = trial_Q2_table.get(new_state, False) or [0,0,0,0]
                    best_action_ind_new_state = np.random.choice(np.argwhere(new_state_Q2_values == np.amax(new_state_Q2_values)).flatten().tolist())
                    
                    # trial_Q2_table[state][action] = (trial_Q2_table.get(state, False) or [0,0,0,0])[action]
                    trial_Q2_table[state][action] = trial_Q2_table[state][action] + self.learn_rate * (score + self.discount*((trial_Q1_table.get(new_state, False) or [0,0,0,0])[best_action_ind_new_state]) - trial_Q2_table[state][action])

                # print(game.environment)
            
                # num_moves+=1
                                    
                # Testing
                # if (state == (3,3,1,0,0,0,0) and action == 0):
                #     print('Cur State : {0}'.format(state))
                #     # print('Action is {0}'.format(action))
                #     print('Q {0}'.format(trial_Q_table[(3,3,1,0,0,0,0)]))
                #     print('New State : {0}'.format(new_state))
                #     print('Q {0}'.format(new_state_action_Q))
                    
                #     # print('Done is {0}'.format(done))
                #     # print('Score is {0}'.format(score))
                    
                #     print(Q_retain)
                #     print(Q_learn)
                    
                #     print('-----------------------------')
            ## end current game
            
            score_running_average = score_running_average + 1/(game_index+1) * (score-score_running_average)
            score_performance[game_index] = score_running_average
            
            # print('Game {0} has Score {1} with epsilon {2}'.format(game_index, score, current_epsilon))
        
            # Reduce epsilon (if over the min amount)
            if current_epsilon > self.epsilon_min:
                current_epsilon = current_epsilon * self.epsilon_decay
                   
        ## end learning
                
        # Testing
        # print('=================================Q-Table Values==============================')
        # for key in trial_Q_table.keys():
        #     print(key)
        #     print(trial_Q_table[key])
            
        # agent.Q_table = trial_Q_table
        
        # Consolidate both Q1 and Q2 tables into one master table        
        consolidated_Q_policy = {}
        all_keys = functools.reduce(lambda x, y: x.union(y.keys()), [trial_Q1_table,trial_Q2_table], set())
        for key in all_keys:
            consolidated_Q_policy[key] = np.add((trial_Q1_table.get(key, False) or [0,0,0,0]), (trial_Q2_table.get(key, False) or [0,0,0,0]))/2


        # Generate the average state-value table
        grid_state_value = np.zeros((6,6))
        grid_state_count = np.zeros((6,6))        
        
        for key in consolidated_Q_policy.keys():
            # print(key)
            # print(trial_Q_table[key])
            y = key[0:1]
            x = key[1:2]
            
            max_value = np.max(consolidated_Q_policy[key])
            # print(max_value)
            grid_state_count[y][x] += 1            
            grid_state_value[y][x] = grid_state_value[y][x] + 1/(grid_state_count[y][x]) * (max_value-grid_state_value[y][x])

        # print(trial_Q1_table)
        # print(trial_Q2_table)
        return consolidated_Q_policy, grid_state_value, score_performance

    def choose_action_per_policy(self, policy, new_y, new_x, haz_NE, haz_SE, haz_SW, haz_NW, h_onHazard):
        state = (new_y, new_x, haz_NE, haz_SE, haz_SW, haz_NW, h_onHazard)
        
        # if state in policy dictionary
        if (state in policy.keys()):
            return np.argmax(policy[state])     
            print('Chose Best Move')
        # if state not in policy dictionary
        else: 
            return random.randint(0,3)
            print('Chose Random Move')

## This Class is the SARSA Learning agent 
class SARSAAgent():
    def __init__(self, num_games, learn_rate, discount, epsilon, epsilon_decay, epsilon_min):
        self.num_games = num_games
        self.learn_rate = learn_rate
        self.discount = discount
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.epsilon_min = epsilon_min
        
        self.agent_name = 'SARSA Agent'
    
    def get_agent_name(self):
        return self.agent_name
    
    def choose_action(self, state, Q_table, current_epsilon):     
        # Choose action according to epsilon greedy
        random_roll=random.random()
        if (random_roll<current_epsilon):
            #Explore
            movement_ind = random.randint(0, 3)
        else:
            #Exploit (With Random Tiebreaker)
            Q_values = Q_table[state]
            movement_ind = np.random.choice(np.argwhere(Q_values == np.amax(Q_values)).flatten().tolist())
    
        return movement_ind
    
    def learn(self, game):
        trial_Q_table = {}
        trial_N_table = {}
        score_running_average = 0
        score_performance = np.empty((self.num_games,))      
        current_epsilon = self.epsilon
        
        for game_index in range(self.num_games):
            new_y, new_x, haz_NE, haz_SE, haz_SW, haz_NW, h_onHazard, score = game.initialize_agent_grid()
            state = (new_y, new_x, haz_NE, haz_SE, haz_SW, haz_NW, h_onHazard)
            action = 0
            
            state_action_Q = np.zeros((4,))
            if state in trial_Q_table.keys():
                # Choose Move according to epsilon-greedy method
                action = self.choose_action(state, trial_Q_table, current_epsilon)                       
                state_action_Q = trial_Q_table[state]
                trial_N_table[state] += 1
            else: 
                # Choose Random Move if no record of this state before
                action = random.randint(0, 3)
                
                trial_Q_table[state] = state_action_Q
                trial_N_table[state] = 1
            
            done=False
            num_moves=0
            while (done != True):
            # while (num_moves < 4):
                # Given state, use epsilon-greedy method to choose an action
                # state = (new_y, new_x, haz_N, haz_E, haz_S, haz_W, haz_NE, haz_SE, haz_SW, haz_NW)
                # state = (new_y, new_x, haz_NE, haz_SE, haz_SW, haz_NW, h_onHazard)
                # print('Current State is : ' + str(state))
                                    
                new_y, new_x, haz_NE, haz_SE, haz_SW, haz_NW, h_onHazard, score, done = game.sim_move(action)
                new_state = (new_y, new_x, haz_NE, haz_SE, haz_SW, haz_NW, h_onHazard)

                # Choose next_action from next_state
                new_state_action_Q = np.zeros((4,))
                new_action = 0
                if new_state in trial_Q_table.keys():
                    # Choose Move according to epsilon-greedy method
                    new_action = self.choose_action(new_state, trial_Q_table, current_epsilon)                       
                    new_state_action_Q = trial_Q_table[new_state]
                    trial_N_table[state] += 1
                else: 
                    # Choose Random Move if no record of this state before
                    new_action = random.randint(0, 3)
                    
                    trial_Q_table[new_state] = new_state_action_Q
                    trial_N_table[new_state] = 1

                # print('new_state ')
                # print(new_state)
                
                # Q_retain = (1-self.learn_rate) * state_action_Q[action]
                # Q_learn = self.learn_rate * (score + DISCOUNT * max(new_state_action_Q))
                
                # Do SARSA Learning (Get Current Reward and Expected Reward of new state)
                # Q_retain = (1-self.learn_rate) * state_action_Q[action]
                                               
                # Get expected value of new state
                # new_state_best_action = np.random.choice(np.argwhere(new_state_action_Q == np.amax(new_state_action_Q)).flatten().tolist())
                # probabilities = np.array([(1-current_epsilon)/3,(1-current_epsilon)/3,(1-current_epsilon)/3,(1-current_epsilon)/3])
                # probabilities[new_state_best_action] = current_epsilon                
                # new_state_expected_value = np.sum(np.multiply(new_state_action_Q, probabilities))
                Q_learn = self.learn_rate * (score + self.discount * new_state_action_Q[new_action] - state_action_Q[action])
                # Q_learn = self.learn_rate * (score + self.discount * new_state_expected_value - state_action_Q[action])
                trial_Q_table[state][action] = state_action_Q[action] + Q_learn
                
                # On-Policy End of Update (update the state and action to new values)
                state = new_state
                action = new_action
                
                # Check if exceeded move count
                num_moves+=1
                if (num_moves>=100):
                    score = -10
                    done = True
                
                # print(game.environment)
                # num_moves+=1
                                    
                # Testing
                # if (state == (3,3,1,0,0,0,0) and action == 0):
                #     print('Cur State : {0}'.format(state))
                #     # print('Action is {0}'.format(action))
                #     print('Q {0}'.format(trial_Q_table[(3,3,1,0,0,0,0)]))
                #     print('New State : {0}'.format(new_state))
                #     print('Q {0}'.format(new_state_action_Q))
                    
                #     # print('Done is {0}'.format(done))
                #     # print('Score is {0}'.format(score))
                    
                #     print(Q_retain)
                #     print(Q_learn)
                    
                #     print('-----------------------------')
            ## end current game
            
            score_running_average = score_running_average + 1/(game_index+1) * (score-score_running_average)
            score_performance[game_index] = score_running_average
            
            # print('Game {0} has Score {1} with epsilon {2}'.format(game_index, score, current_epsilon))
        
            # Reduce epsilon (if over the min amount)
            if current_epsilon > self.epsilon_min:
                current_epsilon = current_epsilon * self.epsilon_decay
                
        ## end learning
            
        
        # Generate the average state-value table
        grid_state_value = np.zeros((6,6))
        grid_state_count = np.zeros((6,6))        
        
        for key in trial_Q_table.keys():
            # print(key)
            # print(trial_Q_table[key])
            y = key[0:1]
            x = key[1:2]
            
            max_value = np.max(trial_Q_table[key])
            # print(max_value)
            grid_state_count[y][x] += 1            
            grid_state_value[y][x] = grid_state_value[y][x] + 1/(grid_state_count[y][x]) * (max_value-grid_state_value[y][x])
        
        # Testing
        # print('=================================Q-Table Values==============================')
        # for key in trial_Q_table.keys():
        #     print(key)
        #     print(trial_Q_table[key])
            
        # agent.Q_table = trial_Q_table
        
        return trial_Q_table, grid_state_value, score_performance
        # return policy

    def choose_action_per_policy(self, policy, new_y, new_x, haz_NE, haz_SE, haz_SW, haz_NW, h_onHazard):
        state = (new_y, new_x, haz_NE, haz_SE, haz_SW, haz_NW, h_onHazard)
        
        # if state in policy dictionary
        if (state in policy.keys()):
            return np.argmax(policy[state])     
            print('Chose Best Move')
        # if state not in policy dictionary
        else: 
            return random.randint(0,3)
            print('Chose Random Move')
    
