import pygame

from ..myTypes.weakreflist import WeakRefList as wrl

class RegisterComponent(object):
    def __init__(self):#, list):
        self.listeners = wrl()
        self.eventBlocked = None
    def set_event_blocked(self, bool):
        self.eventBlocked = bool
    def attach(self, listener, bool = False):
        self.listeners.append(listener)
    def detach(self, listener, bool = False):
        self.listeners.remove(listener)

class PushComponent(object):
    ''' Pushes events back onto pygame event stack'''
    def push(self, event_template):
        if type(event_template) != tuple:
            print "must be in format (int , dict)"
        event_id = event_template[0]
        dict = event_template[1]
        event = pygame.event.Event(event_id, dict)

        pygame.event.post(event)