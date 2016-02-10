import pygame
from pygame.locals import *

class myEvents(object):
    # http://pygametutorials.wikidot.com/tutorials-three

    #these events are here to make it clear that the do nothing
    #overridden with KeyBoardEvents and co
    def onEvent(self, event):
        #print self
        self.checkGeneral(event)

        self.checkMouse(event)
        self.checkKeyBoard(event)

        self.checkJoy(event)

    def checkGeneral(self, event):
        pass
    def checkKeyBoard(self, event):
        pass
    def checkMouse(self, event):
        pass
    def checkJoy(self, event):
        pass

class GeneralEvents(object):
    def checkGeneral(self, event):

        if event.type == pygame.NOEVENT:
            self.onNoEvent(event)

        elif event.type == pygame.ACTIVEEVENT:
            self.onActiveEvent(event)

        elif event.type == pygame.QUIT:
            self.onQuit(event)

        elif event.type == pygame.SYSWMEVENT:
            self.onSysWMEvent(event)

        elif event.type == pygame.VIDEORESIZE:
            self.onVideoResize(event)

        elif event.type == pygame.VIDEOEXPOSE:
            self.onVideoExpose(event)

        elif event.type == pygame.USEREVENT:

            self.onUserEvent(event)

    def onNoEvent(self, event):
        pass
    def onActiveEvent(self, event):
        pass
    def onQuit(self, event):
        pass
    def onSysWMEvent(self, event):
        pass
    def onVideoResize(self, event):
        pass
    def onVideoExpose(self, event):
        pass
    def onUserEvent(self, event):
        pass
