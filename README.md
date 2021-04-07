# Slapper
 Slapper Reinforcement Learning Project

Project Inspired by Melanie Mitchell's "Artificial Intelligence : A Guide To Thinking Humans"

Overview/Inspiration:
There are three different methods of machine learning: unsupervised, supervised, and reinforcement learning.

Unsupervised learning is any kind of learning where the algorithm must generate its results with no label data to train the network on. 
	This type of learning usually focuses on finding patterns and relationships between supplied datapoints.

Supervised learning is learning with a label so the algorithm can adjust its parameters during training to get a better prediction down the line. 
	This type of learning focuses on classification and prediction.

Reinforcement learning is learning that involves rewarding an agent that takes certain actions in order to reinforce that behavior. 
	This type of learning involves trial-and-error simulations where the agent makes educated decisions on the best action to take given the state of the environment.
	
	
Reinforcement learning has really taken off since the folks at DeepMind have created AlphaGo, which was able to beat the Go world champion in a series of 5 matches. 
Since then, AlphaGo has been expanded to include other games in its belt of expertise like chess and shogi. 
Using reinforcement learning, the people of DeepMind have created a system that eerily resembles how people normally learn to play video games; i.e. through hours of practice and trial and error. 
	
	
My project (while not nearly as impressive) is my attempt to create a simple deep learning game that can learn to play the game of "Slapper" (definitely not a clone/ripoff of Frogger).

	
	
Slapper Instructions:

Slapper is a green square frog that wants to get across the road to that rectangular river. 
However, there are red square cars in the way that we wants to avoid in order to not get squashed.

The objective : guide Slapper to the river without touching a car.
The possible actions that Slapper can take are "UP", "RIGHT", "DOWN", "LEFT". The environment is a 6x6 grid where the top row (goal) and bottom row (start) are free of obstacles.
The four rows in between spawn cars that have a small chance to appear on the right side, and once spawned, make their way over to the right side one-block at a time.

Getting Slapper to the end results in 50 points and getting squashed results in -15 points. 


