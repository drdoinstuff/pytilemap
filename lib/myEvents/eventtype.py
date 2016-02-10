import pygame
from pygame.locals import *

class MyEvents(object):
        
        DRAW_SCREEN = 'redraw screen'
        DRAW_RECT = 'dirty rect'
        
        TIMER_EVENT_ELAPSED = 'timer elapsed'
        TIMER_EVENT_STARTED = 'timer started'
        
        ON_WIDGET_FOCUS = 'widget focused'
    
class EventTypes(MyEvents):
        
    display = [pygame.USEREVENT, pygame.ACTIVEEVENT, pygame.VIDEOEXPOSE, pygame.VIDEORESIZE, pygame.NOFRAME, pygame.SYSWMEVENT]
    kbd = [pygame.KEYDOWN, pygame.KEYUP, ]
    mouse = [pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP,]
    joy = [pygame.JOYAXISMOTION, pygame.JOYBALLMOTION, pygame.JOYHATMOTION, pygame.JOYBUTTONDOWN, pygame.JOYBUTTONUP,]
    quit = [pygame.QUIT,]
    
    
    
    MyEvents = MyEvents()
    timers = [pygame.USEREVENT,]#[MyEvents.TIMER_EVENT_STARTED, MyEvents.TIMER_EVENT_ELAPSED, ]
    
    ## PUSH events
    push_redraw = (pygame.USEREVENT, {MyEvents.DRAW_SCREEN:True} )
    push_quit = (pygame.QUIT, {})
    
    timer_elapsed = (pygame.USEREVENT, {MyEvents.TIMER_EVENT_ELAPSED:True})
    def __init__(self):
        pass
        #EventPool = []
        #activeevents = []
    def create_event(self, event_template):
        if type(event_template) != tuple:
            print "must be in format (int , dict)"        
        event_id = event_template[0]
        dict = event_template[1]
        event = pygame.event.Event(event_id, dict)
        return event