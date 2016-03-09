import weakref, random
import pygame
from pygame.locals import *

from ..shared import SharedObjects
from ..shared import AnimateBase
from ..myEvents import eventlistener
from ..myEvents.eventtype import EventTypes
from ..myMath.linear import LinearInterpolate as Interpolate
from ..effects.surface import scale as scale_surf
from ..pathfinding import AStar
from inventory import Inventory

class AnimatedObject(SharedObjects, eventlistener.CombinedMouseKeyBoard, eventlistener.PushComponent):
    def __init__(self, img, pos, tiler):
        super(AnimatedObject, self).__init__()
        self.timed_animation = True
        self.tiler = weakref.proxy(tiler)
        self.image = img
        #classes AStar, Inventory
        #this should be warped with map into a single object where I can query path and data from the map, ie objects and monsters party members etc
        self.pathfinder = AStar(self.tiler.map)#, (self.image.get_width()/2,self.image.get_height()/2) )
        self.inventory = Inventory((1,5))
        #initialise position
        self.x = pos[0]
        self.y = pos[1]
        
    def onDraw(self, screen, event):
        scale = SharedObjects.get_scale()
        screen.blit(scale_surf(self.image, scale), self.tiler._to_coord((self.x,self.y)))

class NPC(AnimatedObject):
    def __init__(self, img, pos, tiler):
        super(NPC, self).__init__(img, pos, tiler)
        
class NPCMonster(NPC):
    def __init__(self, img, pos, tiler):
        super(NPCMonster, self).__init__(img, pos, tiler)

class Avatar(NPC):
    def __init__(self, img, pos, tiler):
        super(Avatar, self).__init__(img, pos, tiler)
        self.health = 10
        #this is abused and becomes a bool after the timer has run
        s = int(SharedObjects.getAnimationStep())
        self.scalar = lambda: s
        self.interpolate = Interpolate(self.scalar(), self.tiler._to_coord((self.x,self.y)), self.tiler._to_coord((self.x,self.y)) )
        self.state = None
    def notify(self, event):
        super(Avatar, self).notify(event)   
    def onTimerAnimate(self, *args):
        pos = self.pathfinder.pop()
        if pos != None:
            scale = SharedObjects.getScale()
            cam_offset = SharedObjects.getCameraOffset()
            start = self.tiler._to_coord((self.x, self.y))
            fin = self.tiler._to_coord(pos)
            start = (start[0] - (cam_offset[0] * scale), start[1] - (cam_offset[1] * scale))
            fin = (fin[0] - (cam_offset[0] * scale), fin[1] - (cam_offset[1] * scale))
            self.interpolate = Interpolate(self.scalar(),start ,fin)
            self.x = pos[0]
            self.y = pos[1]
        self.push(EventTypes.push_redraw)
    def onDraw(self, screen, event):
        ###########
        ## FIXME: the following should give unexpeted 
        ## behavior why woud it except in the first place
        ## 
        scale = SharedObjects.getScale()
        #on the animation  timer pop the new position to iterate towards
        if SharedObjects.getAnimationStep():
            self.onTimerAnimate()
        #use the interpolation generator function
        try:
            scale = SharedObjects.getScale()
            new_offset = SharedObjects.getCameraOffset()
            b = self.interpolate.next()
            #after the next step has been computed and set in sharedobjects
            #get the new camera offset
            cam_offset = SharedObjects.getCameraOffset()
            b = (b[0] + (cam_offset[0] * scale), b[1] + (cam_offset[1] * scale))
        #FIXME: or just give our position in pixels
        except StopIteration:
            b = self.tiler._to_coord((self.x,self.y)) 
        img = scale_surf(self.image, scale)
        screen.blit(img, (int(b[0]), int(b[1])))
    def on_key_m_down(self, event):
        self.state = 'move'
    def on_mouse_button_down(self, event):
        if self.state is 'move':
            self.state = None
            #find a path to the clicked location
            #print 'taget', event
            target = self.tiler._to_tile(event.pos[0], event.pos[1])
            #print target
            self.pathfinder.search((self.x, self.y), target)
        
class NPCPartyMember(Avatar):
    def __init__(self, img, pos, tiler):
        super(NPCPartyMember, self).__init__(img, pos, tiler)
        self.listening_to = [pygame.MOUSEBUTTONDOWN,]
    def on_mouse_rbutton_down(self, event):
        #find a path to the clicked location
        target = self.tiler._to_tile(event.pos[0], event.pos[1])
        self.pathfinder.search((self.x, self.y), (target[0],target[1]))
        #remove the position the player will be in
        if self.pathfinder.lastpath != None and len(self.pathfinder.lastpath) != 0:
            #print self.pathfinder.lastpath
            self.pathfinder.lastpath.reverse()
            # if len(self.pathfinder.lastpath) > 3:
            for i in range(random.randint(1,4)):
                try:
                    self.pathfinder.lastpath.pop()
                except:
                    pass
            self.pathfinder.lastpath.reverse()
            ## FIXME:
            ## delay to try to avoid overlaping with player
            ## hacky but good enough
            for i in range(random.randint(2,4)):
                self.pathfinder.lastpath.append((self.x , self.y))
