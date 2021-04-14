# Slapper

Project Inspired by Melanie Mitchell's "Artificial Intelligence : A Guide To Thinking Humans"
This project is my attempt at training an agent to learn how to play a simple game based on Reinforcement Learning principles.


Video Overview
-----------------------------------------------
https://www.youtube.com/watch?v=1YzOaIBsIQo


Program Requirements
-----------------------------------------------
Python (I have version 3.8.5; to install, go to https://www.python.org/downloads/)

Python Dependencies
-----------------------------------------------
numpy				(run command "pip install numpy" in python terminal)
pygame 				(run command "pip install pygame" in python terminal)
matplotlib.pyplot 	(run command "pip install matplotlib" in python terminal)


Overview/Inspiration:
-----------------------------------------------------------------------------
-----------------------------------------------------------------------------
There are three main methods of machine learning: unsupervised, supervised, and reinforcement learning.

Unsupervised learning is any kind of learning where the algorithm must generate its results with no label data to train the network on. 
This type of learning usually focuses on finding patterns and relationships between supplied datapoints.

Supervised learning is learning with a label so the algorithm can adjust its parameters during training to get a better prediction down the line. 
This type of learning focuses on classification and prediction.

Reinforcement learning is learning that involves rewarding an agent that takes certain actions in order to reinforce that behavior. 
This type of learning involves trial-and-error simulations where the agent makes educated decisions on the best action to take given the state of the environment.


Reinforcement learning has really taken off since the folks at DeepMind have created AlphaGo, which was able to beat the Go world champion in a series of 5 matches. 
Since then, AlphaGo has been expanded to include other games in its belt of expertise like chess and shogi. 
Using reinforcement learning, the people of DeepMind have created a system that eerily resembles how people normally learn to play video games; i.e. through hours of practice and trial and error. 


This project (while not nearly as impressive) is my attempt to create a simple reinforcement learning game that can learn to play the game of "Slapper" (definitely not inspired by the Frogger game series).

	
Slapper Instructions:
-----------------------------------------------------------------------------
Slapper is a green square frog that wants to get across the road to the long river that he calls home. 
However, there are red hazards in the way that we wants to avoid in order to avoid getting squashed.

THE OBJECTIVE OF THE GAME IS TO GUIDE SLAPPER TO THE RIVER WITHOUT TOUCHING A CAR.

The possible actions that Slapper can take are "UP", "RIGHT", "DOWN", "LEFT" (mapped to the UP, RIGHT, DOWN, LEFT arrow keys). 
The environment is a 6x6 grid where the top row (the goal) and bottom row (start) are free of obstacles.
The four rows in between spawn cars that have a small chance to appear on the right side, and once spawned, move to the left-side one block at a time. 
The bottom most rows spawns the least amount of hazards and the topmost row before the goal spawns the most hazards.

The only way to lose is to have Slapper occupy the same space as a hazard at any moment. This means he can take any action unimpeded and a check is made after every action event to see if Slapper is in a hazard spot.
Getting Slapper to the end results in 10 points and getting squashed results in -10 points. 

	
