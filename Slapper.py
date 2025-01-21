# -*- coding: utf-8 -*-
"""
Created on Mar 06 13:14:00 21

@author: Cristian Navarrete
"""

## Local packages
from Game import Game
from Game import Window
from Agents import Agent

## Global Packages
# import numpy as np
import matplotlib.pyplot as plt
# import random

import pygame
# from pygame.locals import *

#%% Initiialize Variables

width, height = 1000, 600
background_color = 250, 250, 250

# Initialize Window, Game, Agent classes
game = Game.Game(6, 6, 5, 5, 10, [(0,0),(0,1),(0,2),(0,3),(0,4),(0,5)])
agent = Agent.DefaultAgent()
policy={}

window = Window.Window(width, height, background_color)
window.display(0, [0,0,0,0,0,0,0,0,0,0], '', game.environment, game.transition_environment, agent, 0)

# Game Parameters
action_dict = {0 : "UP", 1 : "RIGHT", 2 : "DOWN", 3 : "LEFT", -1: "Null"}
action=-1
score=0
playing = False
game_done = False
animating = False

# new_y, new_x, haz_N, haz_E, haz_S, haz_W, haz_NE, haz_SE, haz_SW, haz_NW, score = game.initialize_player_grid()
new_y, new_x, haz_NE, haz_SE, haz_SW, haz_NW, h_onHazard, score = game.initialize_player_grid()

#%% Start Playing

# Event loop
while True:
    # Event Handler
    for event in pygame.event.get():
        if event.type == pygame.locals.QUIT:
            pygame.quit()
            
        elif event.type == pygame.locals.KEYDOWN:
            # If Game is currently playing
            if game.is_game_running() and animating is False:
                if event.key == pygame.locals.K_ESCAPE:
                    print('Stop Game')
                    playing=game.stop_game()
                    # pygame.quit()
            
                if event.key == pygame.locals.K_a:
                    print('Sim an agent move with agent : {0}'.format(type(agent)))
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
                
                # if event.key == pygame.locals.K_s:    
                #     # if (bool(policy) == True):
                #     action = agent.choose_action_per_policy(policy, new_y, new_x, haz_NE, haz_SE, haz_SW, haz_NW, h_onHazard)
                #     new_y, new_x, haz_NE, haz_SE, haz_SW, haz_NW, h_onHazard, score, game_done = game.update(action)     
                #     # else:
                #     #     print('No Policy to Simulate Play')

            else:
                if event.key == pygame.locals.K_p:
                    print('Start Player Game')
                    playing, game_done = game.start_game()
                    # new_y, new_x, haz_N, haz_E, haz_S, haz_W, haz_NE, haz_SE, haz_SW, haz_NW, score = game.initialize_player_grid()
                    new_y, new_x, haz_NE, haz_SE, haz_SW, haz_NW, h_onHazard, score = game.initialize_player_grid()
                                
                if event.key == pygame.locals.K_q:
                    print('Start Q-Learning')
                    NUM_GAMES = 125000
                    # NUM_GAMES = 1
                    ALPHA=0.5
                    DISCOUNT=0.9
                    EPSILON=1
                    EPSILON_DECAY=0.99996
                    # EPSILON_DECAY=1
                    EPSILON_MIN=0.10
                    
                    # Creat agent and start learning to play
                    agent = Agent.QAgent(NUM_GAMES, ALPHA, DISCOUNT, EPSILON, EPSILON_DECAY, EPSILON_MIN) 
                    policy, state_values, score_performance = agent.learn(game)
                    
                    print("Q Agent Learned")
                    
                    # Print Score running average score per game
                    plt.figure(figsize=(12,7))
                    plt.title('Average Score per Game Plot (Q-Learning)')
                    plt.xlabel('Game Number')
                    plt.ylabel('Running Average Score')
                    plt.plot(score_performance)
                    plt.show()
                  
                    # Display state-values per location in color map        
                    fig = plt.figure(figsize=(6, 4))
                    ax = fig.add_subplot(111)
                    ax.set_title('State Value for y-x states (Q)')
                    plt.imshow(state_values, extent=[0,6,6,0])
                    ax.set_aspect('equal')
                    
                    cax = fig.add_axes([0.12, 0.1, 0.78, 0.8])
                    cax.get_xaxis().set_visible(False)
                    cax.get_yaxis().set_visible(False)
                    cax.patch.set_alpha(0)
                    cax.set_frame_on(False)
                    plt.colorbar(orientation='vertical')
                    plt.show()
                    
                  
                if event.key == pygame.locals.K_d:
                    print('Start Double Q-Learning')
                    NUM_GAMES = 125000
                    # NUM_GAMES = 1
                    ALPHA=0.5
                    DISCOUNT=0.9
                    EPSILON=1
                    EPSILON_DECAY=0.99996
                    # EPSILON_DECAY=1
                    EPSILON_MIN=0.10
                    
                    # Creat agent and start learning to play
                    agent = Agent.DQAgent(NUM_GAMES, ALPHA, DISCOUNT, EPSILON, EPSILON_DECAY, EPSILON_MIN) 
                    policy, state_values, score_performance = agent.learn(game)
                    
                    print("Double Q Agent Learned")
                    
                    # Print Score running average score per game
                    plt.figure(figsize=(12,7))
                    plt.title('Average Score per Game Plot (Double Q-Learning)')
                    plt.xlabel('Game Number')
                    plt.ylabel('Running Average Score')
                    plt.plot(score_performance)
                    plt.show()

                    # Display state-values per location in color map        
                    fig = plt.figure(figsize=(6, 4))
                    ax = fig.add_subplot(111)
                    ax.set_title('State Value for y-x states (DQ)')
                    plt.imshow(state_values, extent=[0,6,6,0])
                    ax.set_aspect('equal')
                    
                    cax = fig.add_axes([0.12, 0.1, 0.78, 0.8])
                    cax.get_xaxis().set_visible(False)
                    cax.get_yaxis().set_visible(False)
                    cax.patch.set_alpha(0)
                    cax.set_frame_on(False)
                    plt.colorbar(orientation='vertical')
                    plt.show()

                if event.key == pygame.locals.K_s:
                    print('Start SARSA Learning')
                    NUM_GAMES = 125000
                    # NUM_GAMES = 1
                    ALPHA=0.5
                    DISCOUNT=0.9
                    EPSILON=1
                    EPSILON_DECAY=0.99996
                    # EPSILON_DECAY=1
                    EPSILON_MIN=0.10
                    
                    # Create agent and start learning to play
                    agent = Agent.SARSAAgent(NUM_GAMES, ALPHA, DISCOUNT, EPSILON, EPSILON_DECAY, EPSILON_MIN) 
                    policy, state_values, score_performance = agent.learn(game)
                                        
                    print("SARSA Agent Learned")
                    
                    # Print Score running average score per game
                    plt.figure(figsize=(12,7))
                    plt.title('Average Score per Game Plot (SARSA Learning)')
                    plt.xlabel('Game Number')
                    plt.ylabel('Running Average Score')
                    plt.plot(score_performance)
                    plt.show()
                    
                    # Display state-values per location in color map        
                    fig = plt.figure(figsize=(6, 4))
                    ax = fig.add_subplot(111)
                    ax.set_title('State Value for y-x states (DQ)')
                    plt.imshow(state_values, extent=[0,6,6,0])
                    ax.set_aspect('equal')
                    
                    cax = fig.add_axes([0.12, 0.1, 0.78, 0.8])
                    cax.get_xaxis().set_visible(False)
                    cax.get_yaxis().set_visible(False)
                    cax.patch.set_alpha(0)
                    cax.set_frame_on(False)
                    plt.colorbar(orientation='vertical')
                    plt.show()
    
    # END KEYBOARD EVENT HANDLER       
    
    window.display(score, [new_y, new_x, haz_NE, haz_SE, haz_SW, haz_NW, h_onHazard], action_dict[action], game.environment, game.transition_environment, agent, animating, playing)


    # Check if game finished
    if (playing and game_done):
        print('Game Over')
        playing=game.stop_game()
                        
    
 