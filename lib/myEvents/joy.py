import pygame
from pygame.locals import *

class JoyEvents(object):
    def checkJoy(self, event):
        self.onJoyEvent(event)
        
        if event.type == pygame.JOYAXISMOTION:
            self.onJoyAxisMotion(event)
                
        if event.type == pygame.JOYBALLMOTION:
            self.onJoyBallMotion(event)

        if event.type == pygame.JOYHATMOTION:
            self.onJoyHatMotion(event)

                
        if event.type == pygame.JOYBUTTONDOWN:
            self.onJoyButtonDown(event)

                
        if event.type == pygame.JOYBUTTONUP:
            self.onJoyButtonUp(event)
                
    
    def onJoyEvent(self, event):
        pass
    def onJoyAxisMotion(self, event):
        pass
    def onJoyBallMotion(self, event):
        pass
    def onJoyHatMotion(self, event):
        pass
    def onJoyButtonDown(self, event):
        pass
    def onJoyButtonUp(self, event):
        pass
        