## Cristian Navarrete
# Slapper

import pygame
from pygame.locals import *
import numpy as np
# import copy as cp

import matplotlib.pyplot as plt

import random

#%% Class Definitions

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
        

    def display(self, score, state, action, environment, playing=False):     
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
        state_text_N = self.font.render(str(state[2]), 1, (0, 0, 0))
        state_text_E = self.font.render(str(state[3]), 1, (0, 0, 0))
        state_text_S = self.font.render(str(state[4]), 1, (0, 0, 0))
        state_text_W = self.font.render(str(state[5]), 1, (0, 0, 0))
        state_text_NE = self.font.render(str(state[6]), 1, (0, 0, 0))
        state_text_SE = self.font.render(str(state[7]), 1, (0, 0, 0))
        state_text_SW = self.font.render(str(state[8]), 1, (0, 0, 0))
        state_text_NW = self.font.render(str(state[9]), 1, (0, 0, 0))
        action_text = self.font.render("Action : " + str(action), 1, (0, 0, 0))     
        instructions_text = self.font.render("Press [key] to : " , 1, (0, 0, 0))
        controls_text = self.font.render("(P - Play, Q - Learn (Q), D - Learn (DoubleQ))" , 1, (0, 0, 0))
        controls2_text = self.font.render("(S - Sim Agent, ESC - Stop Game)" , 1, (0, 0, 0))
        
        self.background.blit(score_text, (620, 20))
        self.background.blit(state_text1, (620, 100))
        self.background.blit(state_text2, (620, 130))        
        self.background.blit(state_text_N, (660, 160))
        self.background.blit(state_text_E, (700, 190))
        self.background.blit(state_text_S, (660, 220))
        self.background.blit(state_text_W, (620, 190))
        self.background.blit(state_text_NE, (700, 160))
        self.background.blit(state_text_SE, (700, 220))
        self.background.blit(state_text_SW, (620, 220))
        self.background.blit(state_text_NW, (620, 160))      
        self.background.blit(action_text, (620, 400))
        self.background.blit(instructions_text, (620, 470))
        self.background.blit(controls_text, (620, 500))
        self.background.blit(controls2_text, (620, 530))

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

# Class for Managing the game
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
        self.is_running=False
        
        self.environment = [[1,1,1,1,1,1],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]]
     

    def initialize_player_grid(self):
        self.current_y = self.start_y
        self.current_x = self.start_x
        
        self.environment = [[1,1,1,1,1,1],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]]
        
        return self.start_y, self.start_x, 0, 0, 0, 0, 0, 0, 0, 0, 0
        
    def initialize_agent_grid(self):
        self.current_y = self.start_y
        self.current_x = self.start_x
        
        self.environment = [[1,1,1,1,1,1],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]]
        
        return self.start_y, self.start_x, 0, 0, 0, 0, 0, 0, 0, 0, 0
    
    def start_learning(self):
        self.current_y = self.start_y
        self.current_x = self.start_x
        
        self.environment = [[1,1,1,1,1,1],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]]
        
        return self.start_y, self.start_x, 0, 0, 0, 0, 0, 0, 0, 0, 0
    
    def start_game(self):
        self.is_running = True
        
        # Return Playing=True, GameDone=False
        return True, False
        
    def stop_game(self):
        self.is_running = False
        return False
    
    def sim_game(self, agent):
        return True 
    
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
                if (rand < 0.2):
                    self.environment[i][5] = -1
                    
            elif(i == 2):
                rand = random.random()
                if (rand < 0.15):
                    self.environment[i][5] = -1  
                    
            elif(i == 3):
                rand = random.random()
                if (rand < 0.1):
                    self.environment[i][5] = -1  
                    
            elif(i == 4):
                rand = random.random()
                if (rand < 0.05):
                    self.environment[i][5] = -1                                              

        
        # Built Current Hazard State        
        h_N = 1 if (self.environment[self.game_floor(self.current_y-1)][self.current_x] == -1) else 0
        h_NE = 1 if (self.game_ceiling(self.current_x+1) != self.current_x and self.environment[self.game_floor(self.current_y-1)][self.game_ceiling(self.current_x+1)] == -1) else 0
        
        h_E = 1 if (self.environment[self.current_y][self.game_ceiling(self.current_x+1)] == -1) else 0
        h_SE = 1 if (self.game_ceiling(self.current_x+1) != self.current_x and self.environment[self.game_ceiling(self.current_y+1)][self.game_ceiling(self.current_x+1)] == -1) else 0
        
        h_S = 1 if (self.environment[self.game_ceiling(self.current_y+1)][self.current_x] == -1) else 0
        h_SW = 1 if (self.game_floor(self.current_x-1) != self.current_x and self.environment[self.game_ceiling(self.current_y+1)][self.game_floor(self.current_x-1)] == -1) else 0
        
        h_W = 1 if (self.environment[self.current_y][self.game_floor(self.current_x-1)] == -1) else 0
        h_NW = 1 if (self.game_floor(self.current_x-1) != self.current_x and self.environment[self.game_floor(self.current_y-1)][self.game_floor(self.current_x-1)] == -1) else 0
        
        
        # Check If Win
        done = False
        score=0
        if ((self.current_y, self.current_x) in self.win_states):
            score = self.reward
            done = True
            
        # Check If Lose
        if (self.environment[self.current_y][self.current_x] == -1):
            score = -15
            done = True
        
        return self.current_y, self.current_x, h_N, h_E, h_S, h_W, h_NE, h_SE, h_SW, h_NW, score, done
    
    
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
                if (rand < 0.2):
                    self.environment[i][5] = -1
                    
            elif(i == 2):
                rand = random.random()
                if (rand < 0.15):
                    self.environment[i][5] = -1  
                    
            elif(i == 3):
                rand = random.random()
                if (rand < 0.1):
                    self.environment[i][5] = -1  
                    
            elif(i == 4):
                rand = random.random()
                if (rand < 0.05):
                    self.environment[i][5] = -1                                              

        
        # Built Current Hazard State        
        h_N = 1 if (self.environment[self.game_floor(self.current_y-1)][self.current_x] == -1) else 0
        h_NE = 1 if (self.game_ceiling(self.current_x+1) != self.current_x and self.environment[self.game_floor(self.current_y-1)][self.game_ceiling(self.current_x+1)] == -1) else 0
        
        h_E = 1 if (self.environment[self.current_y][self.game_ceiling(self.current_x+1)] == -1) else 0
        h_SE = 1 if (self.game_ceiling(self.current_x+1) != self.current_x and self.environment[self.game_ceiling(self.current_y+1)][self.game_ceiling(self.current_x+1)] == -1) else 0
        
        h_S = 1 if (self.environment[self.game_ceiling(self.current_y+1)][self.current_x] == -1) else 0
        h_SW = 1 if (self.game_floor(self.current_x-1) != self.current_x and self.environment[self.game_ceiling(self.current_y+1)][self.game_floor(self.current_x-1)] == -1) else 0
        
        h_W = 1 if (self.environment[self.current_y][self.game_floor(self.current_x-1)] == -1) else 0
        h_NW = 1 if (self.game_floor(self.current_x-1) != self.current_x and self.environment[self.game_floor(self.current_y-1)][self.game_floor(self.current_x-1)] == -1) else 0
        
        
        # Check If Win
        done = False
        score=0
        if ((self.current_y, self.current_x) in self.win_states):
            score = self.reward
            done = True
            
        # Check If Lose
        if (self.environment[self.current_y][self.current_x] == -1):
            score = -15
            done = True
        
        return self.current_y, self.current_x, h_N, h_E, h_S, h_W, h_NE, h_SE, h_SW, h_NW, score, done
     
# The class for the Reinforcement Learning Q Agent
class QAgent():
    def __init__(self, num_trials, num_games, learn_rate, discount, epsilon, epsilon_decay, epsilon_min):
        self.num_trials = num_trials
        self.num_games = num_games
        self.learn_rate = learn_rate
        self.discount = discount
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.epsilon_min = epsilon_min
    
        # # Value for an action in a state
        # self.Q_table = {}
        # # Number of times a state has been encountered
        # self.N_table = {}
    
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
        
        score_performance = np.ndarray((self.num_trials,self.num_games))       
        
        for trial_index in range(self.num_trials):
            print('------------------- Trial ' + str(trial_index) + " ----------------")

            trial_Q_table = {}
            trial_N_table = {}

            print(trial_Q_table)
            
            current_epsilon = self.epsilon
            
            for game_index in range(self.num_games):
                new_y, new_x, haz_N, haz_E, haz_S, haz_W, haz_NE, haz_SE, haz_SW, haz_NW, score = game.initialize_agent_grid()
                                
                # num_moves=0
                done=False
                while (done != True):
                # while (num_moves < 4):
                    # Given state, use epsilon-greedy method to choose an action
                    state = (new_y, new_x, haz_N, haz_E, haz_S, haz_W, haz_NE, haz_SE, haz_SW, haz_NW)
                    action = 0
                    # print('Current State is : ' + str(state))
                    
                    # Check if state has occured before
                    state_action_Q = np.zeros((4,))
                    if state in trial_Q_table.keys():
                        # Choose Random Move if no record of this state before
                        action = self.choose_action(state, trial_Q_table, 1.0)                       
                        state_action_Q = trial_Q_table[state]
                        trial_N_table[state] += 1
                    else: 
                        # action = self.choose_action(state, trial_Q_table, current_epsilon)
                        action = random.randint(0, 3)
                        trial_Q_table[state] = state_action_Q
                        trial_N_table[state] = 1
                                       
                    # print('Action is : ' + str(action))
                    # print('current_state ')
                    # print(state)
                        
                        
                    new_y, new_x, haz_N, haz_E, haz_S, haz_W, haz_NE, haz_SE, haz_SW, haz_NW, score, done = game.sim_move(action)
                    new_state = (new_y, new_x, haz_N, haz_E, haz_S, haz_W, haz_NE, haz_SE, haz_SW, haz_NW)
                    # new_state = (new_y, new_x, haz_N, haz_E, haz_S, haz_W, haz_NE, haz_SE, haz_SW, haz_NW)
                    # print('new_state ')
                    # print(new_state)
                    
                    # Do Q-Learning (Get Current Reward and Expected Reward of new state)
                    new_state_action_Q = np.zeros((4,))
                    if new_state in trial_Q_table.keys():
                        new_state_action_Q = trial_Q_table[new_state]
                    
                    Q_retain = (1-self.learn_rate) * trial_Q_table[state][action]
                    Q_learn = self.learn_rate * (score + DISCOUNT * max(new_state_action_Q))
                    
                    trial_Q_table[state][action] = Q_retain + Q_learn
                    # V[current_y][current_x] = max(trial_Q_table[current_y][current_x])
                    
                    # print(game.environment)
                
                    # num_moves+=1
                
                score_performance[trial_index][game_index] = score
                # print('Game {0} has Score {1} with epsilon {2}'.format(game_index, score, current_epsilon))
            
                # Reduce epsilon (if over the min amount)
                if current_epsilon > self.epsilon_min:
                    current_epsilon = current_epsilon * self.epsilon_decay
            
            ## end game          
                
        ## end trial
        
        # Testing
        # print('=================================Q-Table Values==============================')
        # for key in trial_Q_table.keys():
        #     print(key)
        #     print(trial_Q_table[key])
            
        # agent.Q_table = trial_Q_table
        
        return trial_Q_table, score_performance
        # return policy
    
 
# The class for the Reinforcement Learning Double Q Agent
class DQAgent():
    def __init__(self, grid_y, grid_x, start_y, start_x, reward):
        self.grid_y = grid_y
        self.grid_x = grid_x
        self.start_y = start_y
        self.start_x = start_x
        self.reward = reward

        self.Q1_Table = {}
        self.Q2_Table = {}

        self.current_y = start_y        
        self.current_x = start_x
        

    # def run_iteration():
    #     x=0

    # def update(self, action):
    #     x=0
   
#%% Start Playing/Learning

width, height = 1000, 600
background_color = 250, 250, 250

# Initialize Window, Game, Agent classes
game = Game(6, 6, 5, 5, 50, [(0,0),(0,1),(0,2),(0,3),(0,4),(0,5)])

window = Window(width, height, background_color)
window.display(0, [0,0,0,0,0,0,0,0,0,0], '', game.environment, 0)

# Game Parameters
action_dict = {0 : "UP", 1 : "RIGHT", 2 : "DOWN", 3 : "LEFT", -1: "Null"}
action=-1
score=0
playing = False
game_done = False

policy={}

new_y, new_x, haz_N, haz_E, haz_S, haz_W, haz_NE, haz_SE, haz_SW, haz_NW, score = game.initialize_player_grid()

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
            
                if event.key == pygame.locals.K_UP:
                    # print('Move Up')
                    action=0
                    new_y, new_x, haz_N, haz_E, haz_S, haz_W, haz_NE, haz_SE, haz_SW, haz_NW, score, game_done = game.update(action)
                    
                if event.key == pygame.locals.K_RIGHT:
                    # print('Move Right')
                    action=1
                    new_y, new_x, haz_N, haz_E, haz_S, haz_W, haz_NE, haz_SE, haz_SW, haz_NW, score, game_done = game.update(action)
                    
                if event.key == pygame.locals.K_DOWN:
                    # print('Move Down')
                    action=2
                    new_y, new_x, haz_N, haz_E, haz_S, haz_W, haz_NE, haz_SE, haz_SW, haz_NW, score, game_done = game.update(action)
                    
                if event.key == pygame.locals.K_LEFT:
                    # print('Move Left')
                    action=3
                    new_y, new_x, haz_N, haz_E, haz_S, haz_W, haz_NE, haz_SE, haz_SW, haz_NW, score, game_done = game.update(action)
                
            else:
                if event.key == pygame.locals.K_p:
                    print('Start Player Game')
                    playing, game_done = game.start_game()
                    new_y, new_x, haz_N, haz_E, haz_S, haz_W, haz_NE, haz_SE, haz_SW, haz_NW, score = game.initialize_player_grid()
                if event.key == pygame.locals.K_q:
                    print('Start Q-Learning')
                    NUM_TRIALS = 1
                    NUM_GAMES = 200000
                    ALPHA=0.1
                    DISCOUNT=0.9
                    EPSILON=1
                    # EPSILON_DECAY=0.99997
                    EPSILON_DECAY=1
                    EPSILON_MIN=0.15
                    
                    # Creat agent and start learning to play
                    agent = QAgent(NUM_TRIALS, NUM_GAMES, ALPHA, DISCOUNT, EPSILON, EPSILON_DECAY, EPSILON_MIN) 
                    policy, score_performance = agent.learn(game)
                    
                    print("Q Agent Learned")
                    
                    # print("Policy number of states".format(len(policy.keys())))
                        
                if event.key == pygame.locals.K_s:
                    print('Sim the Learned Agent')
                    game.initialize_agent_grid()
                    game.sim_game(agent)                   
                    
    window.display(score, [new_y, new_x, haz_N, haz_E, haz_S, haz_W, haz_NE, haz_SE, haz_SW, haz_NW], action_dict[action], game.environment, playing)
    
    # Check if game finished
    if (playing and game_done):
        print('Game Over')
        playing=game.stop_game()
                        
    ## End Event Handler            
    
    
#%% Plot 

averages=np.average(score_performance, axis=0)

plt.title('Score Plot')
plt.xlabel('Iteration Number')
plt.ylabel('Average Score')
plt.plot(averages)
plt.show()