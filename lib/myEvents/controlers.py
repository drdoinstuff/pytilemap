#!/usr/bin/env python
from time import time as time
from register import RegisterComponent
from weakref import proxy as weakref_proxy
#from myTypes.weakreflist import WeakRefList
from eventlistener import Listener
#for post process test
from ..shared import SharedObjects
from string import join as join
import pygame
from pygame.locals import *
from eventtype import EventTypes as EventTypes

class EventManager(RegisterComponent):
    def __init__(self):
        super(EventManager, self).__init__() ## WeakRefList())
        ## set us as the eventmanager for all listeners
        Listener.setEventManager(self)
    def post(self):
        events = pygame.event.get()
        l_sorted = self.listeners
        for event in events:
            for y in l_sorted:
                l = y()
                if (event.type in l.listeningEvents):
                    l.notify(event)
                ## FIXME
                ## why doesnbt this work
                ## if (event.type in l.listeningEvents) and (self.eventBlocked is (None or l)) or (l.isControler):
                ##      if (self.eventBlocked is (None or l)) or (hasattr(l, "isControler")):
                ##          if self.eventBlocked:
                ##              self.eventBlocked = None

class RenderManager(RegisterComponent):
    def __init__(self):
        super(RenderManager, self).__init__()#WeakRefList())
        Listener.setRenderManager(self)
    def render(self, display, screen, bg_color, event):
        ''' leave it up to the object to manage a what it want to redraw and buffer surfaces'''
        screen.fill(bg_color)
        l =  self.listeners
        [x().onDraw(screen, event) for x in l]
        display.update()
# def Composite(self, screen):
    [x().onDraw(screen, event) for x in self.listeners]

