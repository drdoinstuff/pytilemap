#!/usr/bin/env python

import os 

import pygame
from pygame.locals import *

from shared import SharedObjects

class Dragable(object): #object
    clicked = False
    button = None
    draged_topleft = (0,0)
    current = (0,0)
    start = current
    vect = (0,0)
    
    down = False
    
    selected_obj = None
    
    def moved(self, current):
        self.current = current
        
    def button_down(self, button, mouse_pos, draged_topleft): #must be -draged_topleft
        self.button = button
        
        self.draged_topleft = draged_topleft
        
        self.start = mouse_pos
        self.current = self.start
        
        self.clicked = True

    def button_up(self, button, pos):
        self.button = button
        
        self.current = pos
        self.start = pos
        self.clicked = False
        self.down = False
        
        return (self.draged_topleft[0] - self.current[0], self.draged_topleft[1] - self.current[1])
        #return (-self.current[0] + self.draged_topleft[0], -self.current[1] + self.draged_topleft[1])
    
    def get_velocity(self, dt):
        v = self._get_vect()
        v1 = abs(v[0]/dt)
        v2 = abs(v[1]/dt)
        return (v1,v2)
    
    def _get_vect(self):
        return (self.current[0] - self.start[0],  self.current[1] - self.start[1])
        #return (-self.start[0] + self.current[0], -self.start[1] +  self.current[1])
    
    def _get_scaled_vect(self): #broken
        scale = SharedObjects.Scale()
        
        x0 = (self.start[0]/ scale)
        x1 = (self.current[0] / scale)
        y0 = (self.start[1]/ scale)
        y1 = (self.current[1]/ scale)
        
        #return ((x0 - x1), (y0 - y1))
        return ((x1 - x0), (y1 - y0))
    
    def movement(self, vect = 'scaled'):
        #self.vect = self._get_vect()
        if vect == 'scaled':
            self.vect = self._get_scaled_vect()
        else:
            self.vect = self._get_vect()
        movement = self.draged_topleft[0] - self.vect[0], self.draged_topleft[1] - self.vect[1]
        return movement
    