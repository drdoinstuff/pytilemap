#!/usr/bin/env python

import os, sys

#from weakref import WeakKeyDictionary as wkdict
#from weakref import WeakValueDictionary as wvdict
from ..myTypes.weakreflist import WeakRefList as wrl

import pygame
from pygame.locals import *


from ..myEvents.eventlistener import Listener as Listener

from Shared import UIShared

from ..myEvents.eventlistener import Listener as CombinedMouseKeyBoard
from ..myEvents.controlers import RegisterComponent as RegisterComponent
from ..myEvents.eventtype import EventTypes as EventTypes

## Window Manager ##############################################################
class WindowManager(RegisterComponent, UIShared, CombinedMouseKeyBoard):
    #__dict__ = wvdict() #shared for all instances

    def __init__(self):
        #FIXME super doesnt appear to be working here!

        super(WindowManager, self).__init__()
        self.EventManager.attach(self)
        self.RenderManager.attach(self)

        RegisterComponent.__init__(self)
        #call the unbound method
        UIShared.set_window_manager(self)
        ## CombinedMouseKeyBoard.__init__(self)
        ## this is needed probably because
        ## I have some pretty crappy class design
        self.listeningEvents = EventTypes.mouse + EventTypes.kbd

        self.listeners = wrl() #else it will have its own object in the dict


    def attach(self, listener):
        print 'added', listener
        if len(self.listeners)== 0:
            UIShared.focused_window = listener
        self.listeners.append(listener)
        listener.parent = self

    def on_key_s_down(self, event):
        if self.on_key_shift_down(event):
            for i in self.listeners:
                i.window_attributes.CLOSED = True

    def on_key_menu_down(self, event):
        for i in self.listeners:
            i.window_attributes.CLOSED = True

    def notify(self, event):
        super(WindowManager, self).notify(event)
        self.__event_to_windows__(event)

        #if UIShared.focused_window:
            ### FIXME self.focused_window is self
            #self.listeners.remove(self.focused_window)
            #self.listeners.push(self.focused_window)

    def __event_to_windows__(self, event):
        destroy = []
        sorted_l = self.listeners

        #note: another reverse at the end of the method, crazy!
        #sorted_l.reverse()

        for window in sorted_l:
            #if (event.type in window.listening_to):
                window = window()
                if not window.window_attributes.CLOSED:
                    window.notify(event)
                    #if UIShared.focused_window is window:
                    #    break
                else:
                    if window.window_attributes.DESTROY is True:
                        destroy+=[window,]

        map(self.listeners.__delitem__, destroy)
        #sorted_l.reverse()


    def onDraw(self, screen, event):
        sorted_l = self.listeners
        sorted_l.reverse()
        for window in sorted_l:
            window = window()
            if not window.window_attributes.CLOSED:
                window.draw( screen, event)
        sorted_l.reverse()

