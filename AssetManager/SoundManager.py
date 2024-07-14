# -*- coding: utf-8 -*-
"""
Created on Sun Jul 14 19:01:26 2024

@author: Cristian Navarrete
"""

from pygame.mixer import Sound

class SoundManager():
    
    def __init__(self):
        self.move_effect = Sound('./resources/sounds/move.wav')
        self.success_effect = Sound('./resources/sounds/success.wav')
        self.failure_effect = Sound('./resources/sounds/failure.wav')
        self.training_effect = Sound('./resources/sounds/training.wav')
        
    def play_move_effect(self):
        self.move_effect.play()

    def play_success_effect(self):
        self.success_effect.play()

    def play_failure_effect(self):
        self.failure_effect.play()
               
    def play_training_effect(self):
        self.move_effect.play()
        
