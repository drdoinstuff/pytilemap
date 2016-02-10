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
        super(EventManager, self).__init__()#WeakRefList())

        #set us as the eventmanager for all listeners
        Listener.setEventManager(self)

    def post(self):
        events = pygame.event.get()
        #filter
        l_sorted = self.listeners
        # print '###'
        # for i in l_sorted:
            # print i
        for event in events:
            for y in l_sorted:
                l = y()
                if (event.type in l.listeningEvents):
                    l.notify(event)

                #FIXME
                # why doesnbt this work
                #if (event.type in l.listeningEvents) and (self.eventBlocked is (None or l)) or (l.isControler):
                #if (self.eventBlocked is (None or l)) or (hasattr(l, "isControler")):
                    # if self.eventBlocked:
                        # self.eventBlocked = None

# RenderManager ################################################################

class RenderManager(RegisterComponent):
    def __init__(self):
        super(RenderManager, self).__init__()#WeakRefList())

        Listener.setRenderManager(self)

    def render(self, display, screen, bg_color, event):
        ''' clumsy but works'''
        screen.fill(bg_color)
        sorted_l = self.listeners
        #sorted_l.reverse()
        for y in sorted_l:
            l = y()
            #print l
            #if event in l.listeningEvents:
            #l.onDraw(screen, event)
            l.onDraw(screen, event)

        #post(screen)
        #sorted_l.reverse()

        display.update()

def post(screen):
  #test post process - an easy scan line effect
    screen_array = pygame.surfarray.pixels3d(screen)
    #screen_array-=100
    scan = 0
    sustain = 0
    width = 1#SharedObjects.Scale()
    #altscan = 1

    for line in screen_array:
        scan+=1
        if scan > width:
            #line+=(line - 255)/5 #stop values going above 255
            line+=(255 - line)/10#stop values going above 255
            #/20 #stop values going above 255
            #line-=100 #psyco~!
            sustain+=1
            if sustain > width:
                scan = 0
                sustain = 0
