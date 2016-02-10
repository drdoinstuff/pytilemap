import pygame
from pygame.locals import *


#from eventtype import EventTypes as EventTypes

class MouseEvents(object):
    def checkMouse(self, event):
    #def onEvent(self, event):
        #print self
        if event.type == pygame.MOUSEMOTION:
            self.on_mouse_motion(event)
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.on_mouse_button_down(event)
            
            if event.button == 1:
                self.on_mouse_lbutton_down(event)
            if event.button == 2:
                self.on_mouse_mbuttom_down(event)
            if event.button == 3:
                self.on_mouse_rbutton_down(event)
        
        elif event.type == pygame.MOUSEBUTTONUP:
            self.on_mouse_button_up(event)
            
            if event.button == 1:
                self.on_mouse_lbutton_up(event)
            if event.button == 2:
                self.on_mouse_mbuttom_up(event)
            if event.button == 3:
                self.on_mouse_rbutton_up(event)
                
    def on_mouse_motion(self, event):
        pass   
    def on_mouse_button_down(self, event):
        pass  
    def on_mouse_lbutton_down(self, event):
        pass
    def on_mouse_mbuttom_down(self, event):
        pass
    def on_mouse_rbutton_down(self, event):
        pass
        
    def on_mouse_button_up(self, event):
        pass
    def on_mouse_lbutton_up(self, event):
        pass
    def on_mouse_mbuttom_up(self, event):
        pass
    def on_mouse_rbutton_up(self, event):
        pass
        