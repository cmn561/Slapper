# -*- coding: utf-8 -*-
"""
Created on Sun Jul 14 17:36:57 2024

@author: Cristian Navarrete
"""

from AssetManager import SoundManager

from time import sleep
import random
import pygame


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
        
        pygame.init()
        
        # Environments contain the present and past states of objects in the game
        self.environment = [[1,1,1,1,1,1],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]]
        self.transition_environment = [[1,1,1,1,1,1],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]]
        self.sound_manager = SoundManager.SoundManager()
     

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
        # For transitiong to new environment with animations
        self.transition_environment = self.environment
        
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
            self.sound_manager.play_success_effect()
            done = True
            
        # Check If Lose (Lose if currently on a hazard square or if collided with a hazard while moving right)
        elif (self.environment[self.current_y][self.current_x] == -1 or (action==1 and self.environment[self.current_y][self.current_x-1] == -1)):
            # score = -15
            score = - self.reward
            self.sound_manager.play_failure_effect()
            done = True
        else:
            self.sound_manager.play_move_effect()
        
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
   
            # # Check for New Hazards for this lane
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
        elif (self.environment[self.current_y][self.current_x] == -1 or (action==1 and self.environment[self.current_y][self.current_x-1] == -1)):
            # score = -15
            score = - self.reward
            done = True
        
        # return self.current_y, self.current_x, h_N, h_E, h_S, h_W, h_NE, h_SE, h_SW, h_NW, score, done
        h_onHazard = 1 if done==True else 0
        
        # return self.current_y, self.current_x, h_N, h_E, h_S, h_W, h_NE, h_SE, h_SW, h_NW, score, done
        return self.current_y, self.current_x, h_NE, h_SE, h_SW, h_NW, h_onHazard, score, done
