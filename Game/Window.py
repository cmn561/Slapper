# -*- coding: utf-8 -*-
"""
Created on Sun Jul 14 17:34:00 2024

@author: Cristian Navarrete
"""

import pygame
from pygame.locals import *

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
        # pygame.init()
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