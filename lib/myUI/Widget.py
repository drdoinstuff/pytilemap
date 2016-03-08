
import pygame
from pygame.locals import *

from ..effects.surface import scale as surf_scale
from ..loaders.image import load_image as load_image

from ..shared import SharedObjects

from ..myEvents.eventlistener import Listener
#from ..myEvents.eventlistener import MouseListener
from ..myEvents.eventlistener import PushComponent as PushComponent
from ..myEvents.eventtype import EventTypes as EventTypes

from Shared import UIShared

from ..myEvents.controlers import EventManager

from ..input import Dragable as Dragable


## widget template #############################################################
class Widget(Listener, UIShared):
    #not a listener
    #this is a base for all buttons, dont use this
    
    def __init__(self, rect, img):
        super(Widget, self).__init__()
        self.parent = None
        self.EventManager.listeners.remove(self)
        
        ##load in surface
        if type(img) != pygame.surface.Surface:
            self.img = load_image(img)
        else:
            self.img = img
            
        if type(rect) is tuple:  
            self.rect = pygame.rect.Rect(rect, self.img.get_size())
        else:
            self.rect = rect
            
    def set_parent(self, obj):
        self.parent = obj
        
    def on_widget_focus(self, event):
        print "called widget:", self
        self.set_focused_widget(self)
        self.block_event(True)
        
    def get_my_pos(self, realative_to):
        scale =  SharedObjects.getScale()
        x = realative_to[0] + (self.rect.x * scale) #* scale
        y = realative_to[1] + (self.rect.y * scale) #* scale
        return (x,y)
        
    def draw(self, screen, realative_to):
        surf = surf_scale(self.img, SharedObjects.getScale())
        #update widget size from surface size
        self.rect.size = surf.get_size()
        #getpos relative to parent window
        pos = self.get_my_pos(realative_to)
        screen.blit(surf, pos)

################################################################################
 
class QuitButton(Widget, PushComponent):
    def __init__(self,  rect, img):
        super(QuitButton, self).__init__(rect, img)     
        
    def on_widget_focus(self, event):
        #super(QuitButton, self).set_event_consumed(True)
        self.push(EventTypes.push_quit) 
        
# class CloseButton(Widget, PushComponent):
    # def __init__(self,  rect, img):
        # super(CloseButton, self).__init__(rect, img)
        
    # def on_widget_focus(self, event):
        # pass #self.partial_function()

class HideButton(Widget, PushComponent):
    def __init__(self,  rect, img):
        super(HideButton, self).__init__(rect, img)     
        
    def on_widget_focus(self, event):
        #super(QuitButton, self).set_event_consumed(True)
        #print self.parent
        UIShared.window_manager.listeners.remove(self.parent)
        UIShared.focused_window = UIShared.window_manager.listeners[0]

class Button(Widget):
        def __init__(self,  rect, img):
            super(Button, self).__init__(rect, img)
        def on_widget_focus(self, event):
            print 'pressed button'
            
class TextWidget(Widget):
    def __init__(self, string, font,  rect, img):
        super(TextWidget, self).__init__(rect, img)
        
        self.font = font #dict
        self.string = ''.split(string)
        self.last_character = 0
        
    def get_next(self):
        self.img.fill(SharedObjects.get_flush_to_color())
        
        char_idx = self.last_character
        pos = (0,0)
        
        while True:
            if char_idx > len(self.string):
                return False
            print self.string[char_idx]
            char_img = self.font[self.string[char_idx]]
            self.img.blit(char_img, pos)
            char_idx+=1
            
            if pos[0] + char_img.get_width() > self.rect.width:
                pos[0] = 0
                pos[1] = pos[1]+1
                
            if pos[1] + char_img.get_height() > self.rect.height:
                self.last_character = char_idx
                print '!'
                return True
                
    def on_widget_focus(self, event):
        super(TextWidget, self).event_blocked(True)
        if not self.get_next():
            self.parent.DESTROY = True
        
        
################################################################################            
################################################################################            
################################################################################
            
class UIControl(Button):
    def __init__(self, rect, img):
        super(UIControl, self).__init__( rect, img)
        self.object_ref = None
        
    def set_controled_object(self, obj):
        self.object_ref = object_ref

        
# ################################################################################
# class ScrollBar(UIControl, Dragable):
    # def __init__(self, lock_axis,  rect, img):
        # super(ScrollButton, self).__init__( rect, img)
        # self.lock_axis = lock_axis #string
        
    # def on_mouse_lbutton_down(self, event):
        # self.CLICKED = True
        # self.button_down( 1, event.pos, (-self.x, -self.y))
    
    # def on_mouse_lbutton_up(self, event):
        # #print 'b_up'
        # self.CLICKED = False
        # self.button_up(0, event.pos )
    
    # def on_mouse_motion(self, event):
        # #print 'mm'
        # if self.CLICKED:
            # self.redraw = True
            # self.moved(event.pos)
            # scale = SharedObjects.getScale()
            # mv =  self.movement()
            
            # x, y = -mv[0], -mv[1]
            # print x,y
            # if self.lock_axis is (0,0):
                # scroll_var = (0,0)
            # elif self.lock_axis is (1,0):
                # scroll_var = (x,0)
            # elif self.lock_axis is (0,1):
                # scroll_var = (0, y)
            # elif self.lock_axis is (1,1):
                # scroll_var = (x, y)
                
            # self.parent.scroll(scroll_var)
            
        
# class ScrollButton(Button):
    # def __init__(self, step_delt,  rect, img):
        # super(ScrollButton, self).__init__( rect, img)
        # self.step = step_delt
    # def on_widget_focus(self, event):
        # super(ScrollButton, self).on_widget_focus(event)
        # self.parent.scroll(self.step)
        
# class UIScrollList(UIControl):
    # def __init__(self, object_ref,  rect, img):
        # super(UIControl, self).__init__( rect, img)
        
        # #init controls
        # up_img = img['up']
        # down_img = img['down']
        # scroll_img = img['scroll']
        
        # up_rect = rect['up']
        # down_rect = rect['down']
        # scroll_rect = rect['scroll']
        
        # up_button = ScrollButton( (0,-1), self,  up_rect, up_img)
        # down_button = ScrollButton( (0,1), self,  down_rect, down_img)
        # scroll_bar = ScrollButton( self,  scroll_rect, scroll_img)
        
        # self.controls = {'up':up_button, 'down':down_button, 'scroll':scroll_bar}
        
    # def scroll(delta)    :
        # pass
        
    # def on_widget_focus(self, event):
        # super(UIControl, self).on_widget_focus(event)
        # for i in self.controls:
            # i.on_widget_focus()
            
        
class UIPotion(UIControl):
    def __init__(self, key,  rect, img):
        super(UIPotion, self).__init__(rect, img)
        
        self.key = key
        
    def on_widget_focus(self, event):
        super(UIPotion, self).on_widget_focus(event)
        print self.object_ref.inventory.List()
        self.object_ref.health = self.object_ref.inventory.Use(self.key)(self.object_ref.health)
        print self.object_ref.health
    
    def draw(self, screen, realative_to):
    
        if self.object_ref.inventory.Get(self.key)['uses'] > 0:
            surf = surf_scale(self.img, SharedObjects.getScale())
            #update widget size from surface size
            self.rect.size = surf.get_size()
            #getpos relative to parent window
            pos = self.get_my_pos(realative_to)
            screen.blit(surf, pos)
            
# class UIText(UIControl):
    # def __init__(self, widget_size, object_ref,  rect, img):
        # super(UIControl, self).__init__( rect, img)
        # self.widget_size = widget_size
        # self.text = []
    # def set_text(self, text):
        # self.text = ''.split(text)
    # def draw(self, screen,realative_to):
        
        # surf = surf_scale(self.img, SharedObjects.getScale())
        # #update widget size from surface size
        # self.rect.size = surf.get_size()
        # #getpos relative to parent window
        # pos = self.get_my_pos(realative_to)
        # screen.blit(surf, pos)
