## Cristian Navarrete
# Slapper

import pygame
from pygame.locals import *
import random
import functools as functools
import numpy as np
import matplotlib.pyplot as plt

from time import sleep

#%% Window Class Defintion (for displaying the game)

# Class for the display window
class Window():
    def __init__(self, window_width, window_height, background_color):
        self.window_width = window_width
        self.window_height = window_height
        self.background_color = background_color
        
        self.block_dim = 100
        self.player_offset = 25 
        
        self.black_color = (0,0,0)
        self.white_color = (250,250,250)
        self.player_color = (0,250,0)
        self.hazard_color = (250,0,0)
        self.goal_color = (0,0,250)
        
        # Initialise screen
        pygame.init()
        self.screen = pygame.display.set_mode((window_width, window_height))
        pygame.display.set_caption('Slapper Q-Learning')

        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill(background_color)
        self.font = pygame.font.Font(None, 24)
        

    def display(self, score, state, action, environment, agent, playing=False):     
        self.screen.blit(self.background, (0, 0))
        self.background.fill(self.background_color)

        block = int(self.window_height / self.block_dim)

        # Horizontal Lines
        for i in range(block+1):   
            pygame.draw.line(self.background, self.black_color, (i*self.block_dim,0), (i*self.block_dim,self.window_height), width = 2)
            # pygame.draw.line(self.background, self.black_color, (100,0), (100,600), width = 2)

        # Vertical Lines
        for j in range(block+1):   
            # pygame.draw.line(self.background, self.black_color, (0,0), (0,600), width = 2)
            pygame.draw.line(self.background, self.black_color, (0,j*self.block_dim), (self.window_height,j*self.block_dim), width = 2)

        # Text Display
        score_text = self.font.render("Score : " + str(score), 1, (0, 0, 0))
        state_text1 = self.font.render("Y Pos : " + str(state[0]), 1, (0, 0, 0))
        state_text2 = self.font.render("X Pos : " + str(state[1]), 1, (0, 0, 0))
        state_text_NE = self.font.render(str(state[2]), 1, (0, 0, 0))
        state_text_SE = self.font.render(str(state[3]), 1, (0, 0, 0))
        state_text_SW = self.font.render(str(state[4]), 1, (0, 0, 0))
        state_text_NW = self.font.render(str(state[5]), 1, (0, 0, 0))
        agent_text = self.font.render("Agent : " + str(agent.get_agent_name()), 1, (0, 0, 0))
        action_text = self.font.render("Action : " + str(action), 1, (0, 0, 0))     
        instructions_text = self.font.render("Press [key] to : " , 1, (0, 0, 0))
        controls_text = self.font.render("[P] - Play Game,  [ESC] - Stop Game" , 1, (0, 0, 0))
        controls2_text = self.font.render("[Q] - Train Q Agent" , 1, (0, 0, 0))
        controls3_text = self.font.render("[D] - Train Double-Q Agent" , 1, (0, 0, 0))
        controls4_text = self.font.render("[S] - Train SARSA Agent" , 1, (0, 0, 0))
        controls5_text = self.font.render("[A] - Have Agent Take Move" , 1, (0, 0, 0))
        
        self.background.blit(score_text, (620, 20))
        self.background.blit(state_text1, (620, 100))
        self.background.blit(state_text2, (620, 130))        
        self.background.blit(state_text_NE, (700, 160))
        self.background.blit(state_text_SE, (700, 220))
        self.background.blit(state_text_SW, (620, 220))
        self.background.blit(state_text_NW, (620, 160))      
        self.background.blit(agent_text, (620, 270))
        self.background.blit(action_text, (620, 300))
        self.background.blit(instructions_text, (620, 370))
        self.background.blit(controls_text, (620, 400))
        self.background.blit(controls2_text, (620, 430))
        self.background.blit(controls3_text, (620, 460))
        self.background.blit(controls4_text, (620, 490))
        self.background.blit(controls5_text, (620, 520))

        # Display Game Objects if playing
        if playing:
                        
            # Draw Current Environment(hazards and goal)
            for i in range(len(environment)):
                for j in range(len(environment[i])):
                    
                    # Goal Cell
                    if environment[i][j] == 1:
                        goal=pygame.Rect(j*self.block_dim, i*self.block_dim, self.block_dim, self.block_dim)
                        pygame.draw.rect(self.background, self.goal_color, goal)
                        
                        goal_text = self.font.render("GOAL" , 1, (0, 0, 0))
                        self.background.blit(goal_text, (j*self.block_dim + self.block_dim/4, i*self.block_dim + self.block_dim/2))

                    # Hazard Cell
                    if environment[i][j] == -1:
                        hazard=pygame.Rect(j*self.block_dim, i*self.block_dim, self.block_dim, self.block_dim)
                        pygame.draw.rect(self.background, self.hazard_color, hazard)
        
            # Draw Player
            player=pygame.Rect(state[1]*self.block_dim + self.player_offset, state[0]*self.block_dim + self.player_offset, self.block_dim/2, self.block_dim/2)
            pygame.draw.rect(self.background, self.player_color, player)
            
        pygame.display.flip()

#%% Game Class Defintion (for managing the game)
class Game():
    def __init__(self, grid_y, grid_x, start_y, start_x, reward, win_states):
        self.grid_y = grid_y
        self.grid_x = grid_x
        self.start_y = start_y
        self.start_x = start_x
        self.reward = reward
        self.win_states = win_states

        self.current_y = start_y        
        self.current_x = start_x
        self.is_running = False
        
        self.environment = [[1,1,1,1,1,1],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]]
     

    def initialize_player_grid(self):
        self.current_y = self.start_y
        self.current_x = self.start_x
        
        self.environment = [[1,1,1,1,1,1],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]]
        
        # return self.start_y, self.start_x, 0, 0, 0, 0, 0, 0, 0, 0, 0
        return self.start_y, self.start_x, 0, 0, 0, 0, 0, 0
        
    def initialize_agent_grid(self):
        self.current_y = self.start_y
        self.current_x = self.start_x
        
        self.environment = [[1,1,1,1,1,1],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]]
        
        # return self.start_y, self.start_x, 0, 0, 0, 0, 0, 0, 0, 0, 0
        return self.start_y, self.start_x, 0, 0, 0, 0, 0, 0
        
    def start_game(self):
        self.is_running = True
        
        # Return Playing=True, GameDone=False
        return True, False
        
    def stop_game(self):
        self.is_running = False
        return False
    
    def sim_game(self, agent):
        sleep(0.1) 
    
    def is_game_running(self):
        return self.is_running
        
    def get_environment(self):
        return self.environment

    def game_floor(self, value):
        if value < 0:
            return 0
        
        return value
 
    def game_ceiling(self, value):
        if value > 5:
            return 5
        
        return value   
 
    # Taking player's action
    def update(self, action):
        # UP
        if (action==0):
            if (self.current_y != 0):
                self.current_y+=-1
            
        # RIGHT
        elif (action==1):
            if (self.current_x != self.grid_x-1):
                self.current_x+=1
                
        # DOWN
        elif (action==2):
            if (self.current_y != self.grid_y-1):
                self.current_y+=1
                
        # LEFT
        else:
            if (self.current_x != 0):
                self.current_x+=-1
        
        # Update Hazards
        for i in range(1, len(self.environment)-1):
            for j in range(len(self.environment[i])):
                
                # Remove hazards on left edge
                if (j == 0):
                    self.environment[i][j] = 0
                
                # Update Existing Hazards
                else:
                    if (self.environment[i][j] == -1):
                        # print('moving')
                        self.environment[i][j-1] = -1
                        self.environment[i][j] = 0
   
            # Check for New Hazards for this lane
            if (i == 1):
                rand = random.random()                        
                if (rand < 0.4):
                    self.environment[i][5] = -1
                    
            elif(i == 2):
                rand = random.random()
                if (rand < 0.3):
                    self.environment[i][5] = -1  
                    
            elif(i == 3):
                rand = random.random()
                if (rand < 0.2):
                    self.environment[i][5] = -1  
                    
            elif(i == 4):
                rand = random.random()
                if (rand < 0.1):
                    self.environment[i][5] = -1                                              

        
        # Built Current Hazard State        
        # h_N = 1 if (self.environment[self.game_floor(self.current_y-1)][self.current_x] == -1) else 0
        h_NE = 1 if (self.game_ceiling(self.current_x+1) != self.current_x and self.environment[self.game_floor(self.current_y-1)][self.game_ceiling(self.current_x+1)] == -1) else 0
        
        # h_E = 1 if (self.environment[self.current_y][self.game_ceiling(self.current_x+1)] == -1) else 0
        h_SE = 1 if (self.game_ceiling(self.current_x+1) != self.current_x and self.environment[self.game_ceiling(self.current_y+1)][self.game_ceiling(self.current_x+1)] == -1) else 0
        
        # h_S = 1 if (self.environment[self.game_ceiling(self.current_y+1)][self.current_x] == -1) else 0
        h_SW = 1 if (self.game_floor(self.current_x-1) != self.current_x and self.environment[self.game_ceiling(self.current_y+1)][self.game_floor(self.current_x-1)] == -1) else 0
        
        # h_W = 1 if (self.environment[self.current_y][self.game_floor(self.current_x-1)] == -1) else 0
        h_NW = 1 if (self.game_floor(self.current_x-1) != self.current_x and self.environment[self.game_floor(self.current_y-1)][self.game_floor(self.current_x-1)] == -1) else 0
               
        # Check If Win
        done = False
        score=0
        if ((self.current_y, self.current_x) in self.win_states):
            score = self.reward
            done = True
            
        # Check If Lose
        if (self.environment[self.current_y][self.current_x] == -1):
            # score = -15
            score = - self.reward
            done = True
        
        h_onHazard = 1 if done==True else 0
        
        # return self.current_y, self.current_x, h_N, h_E, h_S, h_W, h_NE, h_SE, h_SW, h_NW, score, done
        return self.current_y, self.current_x, h_NE, h_SE, h_SW, h_NW, h_onHazard, score, done
    
    
    # For simming an agent's move action
    def sim_move(self, action):
        # UP
        if (action==0):
            if (self.current_y != 0):
                self.current_y+=-1
            
        # RIGHT
        elif (action==1):
            if (self.current_x != self.grid_x-1):
                self.current_x+=1
                
        # DOWN
        elif (action==2):
            if (self.current_y != self.grid_y-1):
                self.current_y+=1
                
        # LEFT
        else:
            if (self.current_x != 0):
                self.current_x+=-1
        
        # Update Hazards
        for i in range(1, len(self.environment)-1):
            for j in range(len(self.environment[i])):
                
                # Remove hazards on left edge
                if (j == 0):
                    self.environment[i][j] = 0
                
                # Update Existing Hazards
                else:
                    if (self.environment[i][j] == -1):
                        # print('moving')
                        self.environment[i][j-1] = -1
                        self.environment[i][j] = 0
   
            # Check for New Hazards for this lane
            if (i == 1):
                rand = random.random()                        
                if (rand < 0.4):
                    self.environment[i][5] = -1
                    
            elif(i == 2):
                rand = random.random()
                if (rand < 0.3):
                    self.environment[i][5] = -1  
                    
            elif(i == 3):
                rand = random.random()
                if (rand < 0.2):
                    self.environment[i][5] = -1  
                    
            elif(i == 4):
                rand = random.random()
                if (rand < 0.1):
                    self.environment[i][5] = -1                                              

        
        # Built Current Hazard State        
        # h_N = 1 if (self.environment[self.game_floor(self.current_y-1)][self.current_x] == -1) else 0
        h_NE = 1 if (self.game_ceiling(self.current_x+1) != self.current_x and self.environment[self.game_floor(self.current_y-1)][self.game_ceiling(self.current_x+1)] == -1) else 0
        
        # h_E = 1 if (self.environment[self.current_y][self.game_ceiling(self.current_x+1)] == -1) else 0
        h_SE = 1 if (self.game_ceiling(self.current_x+1) != self.current_x and self.environment[self.game_ceiling(self.current_y+1)][self.game_ceiling(self.current_x+1)] == -1) else 0
        
        # h_S = 1 if (self.environment[self.game_ceiling(self.current_y+1)][self.current_x] == -1) else 0
        h_SW = 1 if (self.game_floor(self.current_x-1) != self.current_x and self.environment[self.game_ceiling(self.current_y+1)][self.game_floor(self.current_x-1)] == -1) else 0
        
        # h_W = 1 if (self.environment[self.current_y][self.game_floor(self.current_x-1)] == -1) else 0
        h_NW = 1 if (self.game_floor(self.current_x-1) != self.current_x and self.environment[self.game_floor(self.current_y-1)][self.game_floor(self.current_x-1)] == -1) else 0
        
        
        # Check If Win
        done = False
        score=0
        if ((self.current_y, self.current_x) in self.win_states):
            score = self.reward
            done = True
            
        # Check If Lose
        if (self.environment[self.current_y][self.current_x] == -1):
            # score = -15
            score = - self.reward
            done = True
        
        # return self.current_y, self.current_x, h_N, h_E, h_S, h_W, h_NE, h_SE, h_SW, h_NW, score, done
        h_onHazard = 1 if done==True else 0
        
        # return self.current_y, self.current_x, h_N, h_E, h_S, h_W, h_NE, h_SE, h_SW, h_NW, score, done
        return self.current_y, self.current_x, h_NE, h_SE, h_SW, h_NW, h_onHazard, score, done

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
        
        self.agent_name = 'Random Agent'

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
                Q_learn = self.learn_rate * (score + DISCOUNT * max(new_state_action_Q))
                
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
            
        # Testing
        # print('=================================Q-Table Values==============================')
        # for key in trial_Q_table.keys():
        #     print(key)
        #     print(trial_Q_table[key])
            
        # agent.Q_table = trial_Q_table
        
        return trial_Q_table, score_performance
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
            consolidated_Q_policy[key] = np.add((trial_Q1_table.get(key, False) or [0,0,0,0]), (trial_Q2_table.get(key, False) or [0,0,0,0]))   

        # print(trial_Q1_table)
        # print(trial_Q2_table)
        return consolidated_Q_policy, score_performance

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
                new_state_best_action = np.random.choice(np.argwhere(new_state_action_Q == np.amax(new_state_action_Q)).flatten().tolist())
                probabilities = np.array([(1-current_epsilon)/3,(1-current_epsilon)/3,(1-current_epsilon)/3,(1-current_epsilon)/3])
                probabilities[new_state_best_action] = current_epsilon                
                new_state_expected_value = np.sum(np.multiply(new_state_action_Q, probabilities))
                # Q_learn = self.learn_rate * (score + self.discount * new_state_action_Q[new_action] - state_action_Q[action])
                Q_learn = self.learn_rate * (score + self.discount * new_state_expected_value - state_action_Q[action])
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
            
        # Testing
        # print('=================================Q-Table Values==============================')
        # for key in trial_Q_table.keys():
        #     print(key)
        #     print(trial_Q_table[key])
            
        # agent.Q_table = trial_Q_table
        
        return trial_Q_table, score_performance
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
    

#%% Initiialize Classes and Start Playing

width, height = 1000, 600
background_color = 250, 250, 250

# Initialize Window, Game, Agent classes
game = Game(6, 6, 5, 5, 10, [(0,0),(0,1),(0,2),(0,3),(0,4),(0,5)])
agent = DefaultAgent()
policy={}

window = Window(width, height, background_color)
window.display(0, [0,0,0,0,0,0,0,0,0,0], '', game.environment, agent, 0)

# Game Parameters
action_dict = {0 : "UP", 1 : "RIGHT", 2 : "DOWN", 3 : "LEFT", -1: "Null"}
action=-1
score=0
playing = False
game_done = False



# new_y, new_x, haz_N, haz_E, haz_S, haz_W, haz_NE, haz_SE, haz_SW, haz_NW, score = game.initialize_player_grid()
new_y, new_x, haz_NE, haz_SE, haz_SW, haz_NW, h_onHazard, score = game.initialize_player_grid()

# Event loop
while True:
    # Event Handler
    for event in pygame.event.get():
        if event.type == pygame.locals.QUIT:
            pygame.quit()
            
        elif event.type == pygame.locals.KEYDOWN:
            # If Game is currently playing
            if game.is_game_running():
                if event.key == pygame.locals.K_ESCAPE:
                    print('Stop Game')
                    playing=game.stop_game()
                    # pygame.quit()
            
                if event.key == pygame.locals.K_a:
                    action = agent.choose_action_per_policy(policy, new_y, new_x, haz_NE, haz_SE, haz_SW, haz_NW, h_onHazard)
                    new_y, new_x, haz_NE, haz_SE, haz_SW, haz_NW, h_onHazard, score, game_done = game.update(action) 
            
                if event.key == pygame.locals.K_UP:
                    # print('Move Up')
                    action=0
                    # new_y, new_x, haz_N, haz_E, haz_S, haz_W, haz_NE, haz_SE, haz_SW, haz_NW, score, game_done = game.update(action)
                    new_y, new_x, haz_NE, haz_SE, haz_SW, haz_NW, h_onHazard, score, game_done = game.update(action)
                    
                if event.key == pygame.locals.K_RIGHT:
                    # print('Move Right')
                    action=1
                    # new_y, new_x, haz_N, haz_E, haz_S, haz_W, haz_NE, haz_SE, haz_SW, haz_NW, score, game_done = game.update(action)
                    new_y, new_x, haz_NE, haz_SE, haz_SW, haz_NW, h_onHazard, score, game_done = game.update(action)
   
                if event.key == pygame.locals.K_DOWN:
                    # print('Move Down')
                    action=2
                    # new_y, new_x, haz_N, haz_E, haz_S, haz_W, haz_NE, haz_SE, haz_SW, haz_NW, score, game_done = game.update(action)
                    new_y, new_x, haz_NE, haz_SE, haz_SW, haz_NW, h_onHazard, score, game_done = game.update(action)

                if event.key == pygame.locals.K_LEFT:
                    # print('Move Left')
                    action=3
                    # new_y, new_x, haz_N, haz_E, haz_S, haz_W, haz_NE, haz_SE, haz_SW, haz_NW, score, game_done = game.update(action)
                    new_y, new_x, haz_NE, haz_SE, haz_SW, haz_NW, h_onHazard, score, game_done = game.update(action)
                
                if event.key == pygame.locals.K_s:    
                    # if (bool(policy) == True):
                    print('Sim an agent move with agent : {0}'.format(type(agent)))
                    action = agent.choose_action_per_policy(policy, new_y, new_x, haz_NE, haz_SE, haz_SW, haz_NW, h_onHazard)
                    new_y, new_x, haz_NE, haz_SE, haz_SW, haz_NW, h_onHazard, score, game_done = game.update(action)     
                    # else:
                    #     print('No Policy to Simulate Play')

            else:
                if event.key == pygame.locals.K_p:
                    print('Start Player Game')
                    playing, game_done = game.start_game()
                    # new_y, new_x, haz_N, haz_E, haz_S, haz_W, haz_NE, haz_SE, haz_SW, haz_NW, score = game.initialize_player_grid()
                    new_y, new_x, haz_NE, haz_SE, haz_SW, haz_NW, h_onHazard, score = game.initialize_player_grid()
                                
                if event.key == pygame.locals.K_q:
                    print('Start Q-Learning')
                    NUM_GAMES = 125000
                    # NUM_GAMES = 2
                    ALPHA=0.5
                    DISCOUNT=0.9
                    EPSILON=1
                    EPSILON_DECAY=0.99996
                    # EPSILON_DECAY=1
                    EPSILON_MIN=0.10
                    
                    # Creat agent and start learning to play
                    agent = QAgent(NUM_GAMES, ALPHA, DISCOUNT, EPSILON, EPSILON_DECAY, EPSILON_MIN) 
                    policy, score_performance = agent.learn(game)
                    
                    print("Q Agent Learned")
                    
                    # Print Score running average score per game
                    plt.figure(figsize=(12,7))
                    plt.title('Average Score per Game Plot (Q-Learning)')
                    plt.xlabel('Game Number')
                    plt.ylabel('Running Average Score')
                    plt.plot(score_performance)
                    plt.show()
                  
                if event.key == pygame.locals.K_d:
                    print('Start Double Q-Learning')
                    NUM_GAMES = 125000
                    # NUM_GAMES = 2
                    ALPHA=0.5
                    DISCOUNT=0.9
                    EPSILON=1
                    EPSILON_DECAY=0.99996
                    # EPSILON_DECAY=1
                    EPSILON_MIN=0.10
                    
                    # Creat agent and start learning to play
                    agent = DQAgent(NUM_GAMES, ALPHA, DISCOUNT, EPSILON, EPSILON_DECAY, EPSILON_MIN) 
                    policy, score_performance = agent.learn(game)
                    
                    print("Double Q Agent Learned")
                    
                    # Print Score running average score per game
                    plt.figure(figsize=(12,7))
                    plt.title('Average Score per Game Plot (Double Q-Learning)')
                    plt.xlabel('Game Number')
                    plt.ylabel('Running Average Score')
                    plt.plot(score_performance)
                    plt.show()

                if event.key == pygame.locals.K_s:
                    print('Start SARSA Learning')
                    NUM_GAMES = 125000
                    # NUM_GAMES = 2
                    ALPHA=0.4
                    DISCOUNT=0.9
                    EPSILON=1
                    EPSILON_DECAY=0.99996
                    # EPSILON_DECAY=1
                    EPSILON_MIN=0.10
                    
                    # Create agent and start learning to play
                    agent = SARSAAgent(NUM_GAMES, ALPHA, DISCOUNT, EPSILON, EPSILON_DECAY, EPSILON_MIN) 
                    policy, score_performance = agent.learn(game)
                                        
                    print("SARSA Agent Learned")
                    
                    # Print Score running average score per game
                    plt.figure(figsize=(12,7))
                    plt.title('Average Score per Game Plot (SARSA Learning)')
                    plt.xlabel('Game Number')
                    plt.ylabel('Running Average Score')
                    plt.plot(score_performance)
                    plt.show()
                               
    window.display(score, [new_y, new_x, haz_NE, haz_SE, haz_SW, haz_NW, h_onHazard], action_dict[action], game.environment, agent, playing)


    # Check if game finished
    if (playing and game_done):
        print('Game Over')
        playing=game.stop_game()
                        
    ## End Event Handler            
    
    
#%% Testing

# import numpy as np

# action_Q_values = np.ndarray((len(policy.items()),4))


# # for i in range(3):
# #     test3 = test3 + (1/(itercount+1)) * [test[i] - test3]
# #     print(test3)

# itercount=0
# for k, v in policy.items():
#     action_Q_values[itercount] = v
#     itercount+=1

# average = np.average(action_Q_values, axis=0)

# print(average)




d1 = {1 : [1,1,1,1]}
d2 = {1 : [1,1,1,1]}




# d3 = np.add((d1.get(1, False) or [0,0,0,0]), (d2.get(1, False) or [0,0,0,0]))
# variable_name = my_dict.get('keyname', False) or 'something else'
# print(d1.get(1, False) or np.array([0,0,0,0]))


test = d1.get(1, False) or [0,0,0,0]

print(type(d1))
print(type(test))
# print(np.where(np.array([0,0,0,0])))



# allkey = functools.reduce(lambda x, y: x.union(y.keys()), [d1,d2], set())

# for s in allkey:
#     print(s)
# print(allkey)
# allkey = d1.keys() | d2.keys()

# print(np.add([0,0,0,0],[1,1,1,1]))

Q = [10,-5,0,0]

current_epsilon = 0.4
probabilities = np.array([(1-current_epsilon)/3,(1-current_epsilon)/3,(1-current_epsilon)/3,(1-current_epsilon)/3])

probabilities[np.argmax(Q)] = current_epsilon


total_value = np.multiply(Q, probabilities)
print(np.sum(total_value))
