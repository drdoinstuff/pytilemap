import pygame
from pygame.locals import *

from weakref import WeakKeyDictionary as wkdict

from ..myTypes.weakreflist import WeakRefList as wrl

from ..effects.surface import scale as scale_surf



from ..effects.surface import scale as surf_scale
from ..input import Dragable as Dragable

from ..shared import SharedObjects
from ..myEvents.eventlistener import PushComponent as PushComponent
#from ..myEvents.eventlistener import Listener as Listener
from ..myEvents.eventlistener import CombinedMouseKeyBoard as Listener
from ..myEvents.eventlistener import MouseListener as MouseListener

from ..myEvents.eventtype import EventTypes as EventTypes

from Shared import UIShared
from Widget import Widget

from ..myEvents.controlers import RegisterComponent as RegisterComponent
from ..myEvents.controlers import EventManager

# Window #######################################################################
class WindowAttributes(object):
    def __init__(self):
        self.SCROLLED = False
        self.MAXIMISED = False
        self.DRAGGED = False
        self.CLICKED = False

        self.CLOSED = False

        self.DESTROY = False

class Window(RegisterComponent, Dragable, UIShared, Listener): #MouseListener):#

    def __init__(self, surface, pos):#, title_bar_width = 4):
        super(Window, self).__init__()
        ## this is needed probably because
        ## I have some pretty crappy class design
        UIShared.window_manager.listeners.remove(self)

        self.listeningEvents = EventTypes.mouse + EventTypes.kbd
        #add us to the window manager
        self.window_manager.attach(self)
        self.listeners = wrl()

        self.window_attributes = WindowAttributes()
        self.rect = surface.get_rect(topleft = pos)
        self.surface = surface
        self.widget_reference_coord = pos

    # def attach(self, listener):
        # print "you you you....", self, listener
        # exit()
    def attach_widget(self, listener):
        #try to check that the listerner is going to be within a window
        #kinda crappy, should warn
        ERROR = "widget out of window bounds: dropping"
        #print listener, type(listener)
        if listener.rect.x <= self.rect.width:
            if listener.rect.width <= self.rect.width >= listener.rect.x + listener.rect.width:

                if listener.rect.y <= self.rect.size[1]:
                    if listener.rect.size[1] <= self.rect.size[1] >= listener.rect.y + listener.rect.size[1]:

                        #super(Window, self).attach(listener)
                         self.attach(listener)
                         print 'set', self, ' as parent'
                         listener.set_parent(self)

                    else:
                        print ERROR
                else:
                    print ERROR
            else:
                print ERROR
        else:
            print ERROR

    def window_close(self):
        pass
    def window_minimise(self):
        pass
    def window_maximise(self):
        pass

    def draw(self, screen, event):
        if not self.window_attributes.SCROLLED:
            scale = SharedObjects.Scale()
            bg = scale_surf(self.surface, scale)
            self.rect.size = bg.get_size()

            x = self.rect.topleft[0] * scale
            y = self.rect.topleft[1] * scale
            rect = pygame.rect.Rect((x,y), self.rect.size)

            screen_rect = SharedObjects.Screen().get_rect()
            rect = rect.clamp(screen_rect)

            self.rect.x = rect.x / scale
            self.rect.y = rect.y / scale

            x = rect.x
            y = rect.y

            self.widget_reference_coord = (x,y)
            screen.blit(bg, (x,y))

            for widget in self.listeners:
                widget().draw(screen, (x,y))

    def __event_to_widgets__(self, event):
        scale = SharedObjects.Scale()

        for widget in self.listeners:
            widget = widget()
            pos = widget.get_my_pos((self.widget_reference_coord))

            if (pos[0] < event.pos[0] < pos[0] + widget.rect.size[0]):
                if ( pos[1] < event.pos[1] < pos[1] + widget.rect.size[1]):
                    widget.on_widget_focus(event)
                    Listener.setBlocking(self)


    def on_mouse_motion(self, event):
        if (UIShared.focused_window is self) and (self.window_attributes.DRAGGED):
            Listener.setBlocking(self.window_manager)

            self.moved(event.pos)
            mv = self.movement()#'unscaled')
            #'snap' to 'pixels'
            #scale = SharedObjects.Scale()
            #xq, yq = (-mv[0]%scale), (-mv[1]%scale)
            #dont 'snap' to 'pixels'
            xq, yq = 0, 0

            self.rect.topleft = (-mv[0]-xq, -mv[1]-yq)
            return True

    def on_mouse_button_down(self, event):
        #perfect
        #SharedUI.set_focused_window(False)
        ## NOTE: window focus is also set in window manager .__events_to_windows__

        self.window_attributes.CLICKED = True
        self.button_down( 1, event.pos, (-self.rect.x, -self.rect.y))

        scale =  SharedObjects.Scale()

        #window area
        if not self.window_attributes.SCROLLED:
            scale =  SharedObjects.Scale()
            # x = self.rect.x * scale
            # y = self.rect.y * scale
            x = self.widget_reference_coord[0] #* scale
            y = self.widget_reference_coord[1] #* scale
            width = self.rect.width
            height = self.rect.height
            #if __EventManager__.__getattr__('focused_window') == self:
            if x <= event.pos[0] <= x + width:# * scale:
                if y <= event.pos[1] <= y + height:# * scale:
                    #if not self.EventManager.eventBlocked and (self.focused_window is self):

                        #Listener.setBlocking(self)

                        print 'passing events to widgets'
                        self.window_attributes.DRAGGED = True

                        if UIShared.focused_window is self:
                            self.__event_to_widgets__(event)
                        else:


                            UIShared.set_focused_window(self)
                            self.window_manager.listeners.remove(self)

                            # this is a "push" because the window manager has reversed the window list
                            self.window_manager.listeners.push(self)

    def on_mouse_button_up(self, event):
        #self.block_event(False)
        #self.self.block_event(True)(False)
        #if self.DRAGGED is True:
        self.window_attributes.DRAGGED = False
        #print "dropped"
        self.window_attributes.CLICKED = False

        self.button_up(0, event.pos )

        Listener.setBlocking(None)