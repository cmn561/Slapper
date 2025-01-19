# -*- coding: utf-8 -*-
"""
Created on Sun Jul 14 23:00:27 2024

@author: Cristian Navarrete
"""

from time import sleep

class AnimationHandler():
    def __init__(self):
        self.currently_animating = False
        self.animation_frames_required = 5
        self.current_frame = 0
    
    def animate(self):
        if (not self.currently_animating):
            currently_animating = True
            current_frame = 0
            
        self.animate_hazards()
        self.animate_player()
        
        sleep(0.05)
        
    
    def animate_hazards(self):
        1==1
    
    def animate_player(self):
        1==1

