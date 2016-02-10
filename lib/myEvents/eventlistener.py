# import pygame
# from pygame.locals import *

# from weakref import proxy
from weakref import WeakKeyDictionary as weakref

from register import RegisterComponent
from register import PushComponent

from coreevents import myEvents
from coreevents import GeneralEvents
from mykbd import KeyBoardEvents
from mouse import MouseEvents
from joy import JoyEvents

from eventtype import EventTypes

## perhaps my own events #######################################################

# EventListener  Template ################################################################

class Listener(myEvents):
    ''' Only acts on events '''

    EventManager = None
    RenderManager = None

    Blocking = None

    def __init__(self):
        self.listeningEvents = []
        self.blockingEvents = []

        self.isControler = False
        self.isBlocking = False
        self.isAnimation = False

        #error checking
        if self.EventManager is not None:
            self.EventManager.attach(self)
        else:
            print self,'##tried to add a Manager Object--> EventManager: %s, RenderManager: %s ' % (self.EventManager, self.RenderManager)
            exit()

    @classmethod
    def setEventManager(self, obj):
        self.EventManager = obj

    @classmethod
    def setRenderManager(self, obj):
        self.RenderManager = obj

    @classmethod
    def setBlocking(self, obj):
        self.Blocking = obj
        self.EventManager.eventBlocked = obj

    def get_blocked_event(self):
        return self.EventManager.event_blocked

    def block_event(self, obj):
        self.EventManager.set_event_blocked(obj)

    def notify(self, event):
        self.onEvent(event)


# Quitter ######################################################################
class Quitter(GeneralEvents, Listener): #order of this is very important!
    ''' use [pygame.QUIT, ] '''
    def __init__(self):
        super(Quitter, self).__init__()
        self.listeningEvents = EventTypes.quit

    def onQuit(self, event):
        print 'Quitting'
        exit()

# class TimerListener(Listener):
    # def __init__(self):
        # super(Quitter, self).__init__()
        # self.listeningEvents = EventTypes.timer
    # def onEvent(event):
        # super(TimerListener, self).onEvent(event):


# DisplayListener ##############################################################
#move this into render manager

# class DisplayListener(GeneralEvents, Listener):
    # #PushComponent has internal constants
    # #going to need an event Manager syle for calling .onDraw() methods
    # def __init__(self, screen, display, flush_color):
        # super(DisplayListener, self).__init__()

        # self.listeningEvents = EventTypes.display

        # self.screen = screen
        # self.display = display

        # self.flush_surface_on_draw = []

        # self.flush_screen_to = flush_color

    # def flush_surface(self, surf):
        # self.flush_surface_on_draw+=[proxy(surf),]

    # def onUserEvent(self, event):
        # #directly calls the manager it is attached to
        # #review this
        # if EventTypes.REDRAW_ENTIRE_SCREEN in event.dict:

            # self.render_manager.render(self.screen, event)
            # self.display.update()

    # def onDraw(self, screen, event):
        # screen.fill(self.FlushColor())

        # for i in self.flush_surface_on_draw:
            # i.fill(flush_color)


# *Manager #####################################################################
class KeyBoardListener(KeyBoardEvents, Listener):
    def __init__(self):
        super(KeyBoardListener, self).__init__()
        self.listeningEvents = EventTypes.kbd

class MouseListener(MouseEvents, Listener):
    def __init__(self):
        super(MouseListener, self).__init__()
        self.listeningEvents = EventTypes.mouse
        #self.blocking_events = EventTypes.mouse

class CombinedMouseKeyBoard(MouseEvents, KeyBoardEvents, Listener):
    def __init__(self):
        super(CombinedMouseKeyBoard, self).__init__()
        self.listeningEvents = EventTypes.mouse + EventTypes.kbd

class JoyListener(JoyEvents, Listener):
    def __init__(self):
        super(JoyListener, self).__init__()
        self.listeningEvents = EventTypes.joy

        #init joy
        js = self.new_joy()
        self.joystick, self.joystick_id = js[0], js[1]

    def new_joy(self):
        ##joystick must be between 0 and pygame.joystick.get_count()-1
        joystick = pygame.joystick.Joystick(pygame.joystick.get_count()-1)
        if joystick.init() == None:
            joystick_id = joystick.get_id()
            print "Initialised JoyStick..."
            print "JoyStick ID is: ", joystick_id
            print "Number of JoySticks: ", pygame.joystick.get_count()
            ##we must match the "joy" event attribute to the right joy stick
            ##if there are more than one players

        else:
            print "Sorry, the JoyStick might not work"

        return (joystick, joystick_id)


################################################################################
################################################################################
################################################################################

if __name__ == '__main__':
    import pygame
    from pygame.locals import *

    pygame.init()

    res = (100,100)
    fps = 360

    disp = pygame.display
    scrn = pygame.display.set_mode(res)

    clock = pygame.time.Clock()

    joy = JoyListener()
    while True:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type in joy.listening_to:
                print event
                joy.onEvent(event)
