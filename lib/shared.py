#!/usr/bin/env python

#python built in modules
import os, sys, time, logging, string

#import mymath, events, time
#from loaders.fileoperations import ConfFile

#pygame
import pygame
from pygame.locals import *

#my modules
from effects.surface import scale

import myEvents.eventlistener as eventlistener

def query_obj(obj):#, exclude = []):
    for i in dir(obj):
        yield getattr(obj, i)

class SimpleEvents(object):

    # try to create a new event type
    # The docs say not to use event ids above NUMEVENTS
    # doesnt really simplify anything, it should
    # size of sdl event que is 256, only use this sparingly
    # officialy only ~ 8 events are free
    __user_assigned__ = list()
    # for i in __iterEvents__('UserEvent'):
        # __user_assigned__[i] = None

    @staticmethod
    def __iterEvents__(filter = None):
        for i in range(255):
            e = pygame.event.event_name(i)
            if (filter != None) and ( filter == e):
                yield i, e

    @staticmethod
    def getEventID(event):
        pass
    @staticmethod
    def getNewEvent(typeID, Attributes):
        #if it isnt in an available range or been assigned already
        if (typeID in range(pygame.USEREVENT, pygame.NUMEVENTS)) and (typeID not in SimpleEvents.__user_assigned__ ):

            SimpleEvents.__user_assigned__.append(typeID)
            newevent = pygame.event.Event(typeID, Attributes)
            SimpleEvents.__user_assigned__.sort()

            return newevent

        else:
            ### try to salvage the call and assign something
            SimpleEvents.__user_assigned__.sort()

            n = len(SimpleEvents.__user_assigned__)

            if n is 0:
                newID = pygame.USEREVENT
            else:
                newID = SimpleEvents.__user_assigned__[n-1]+1

            if pygame.USEREVENT <= newID < pygame.NUMEVENTS:
                typeID = newID
                SimpleEvents.__user_assigned__.append(typeID)

            newevent = pygame.event.Event(typeID, Attributes)

            return newevent

    @staticmethod
    def RemoveEvent(typeID):
        SimpleEvents.__userassigned.__delitem__(typeID)

    @staticmethod
    def getUnusedEvents():
        events = []
        for i in SimpleEvents.__iterEvents__():
            events.append(i)
        return events

    @staticmethod
    def getAvailableEvents():
        events = []
        for i in SimpleEvents.__iterEvents__('UserEvent'):
            events.append(i)
        return events

    @staticmethod
    def postEvent(EventID):
        pygame.event.post(EventID)

class Timer(object):

    def __init__(self, interval):
        #self.time = time.time()
        self.time = 0
        self.elapsed = 0

        self.interval = interval
        self.started = interval

    def Reset(self):
        #self.time = time.time()
        self.time = 0
        self.elapsed = 0

    def Trigger(self):
        self.elapsed = self.interval

    def getTimeRun(self):
        return self.time + self.elapsed

    def Update(self):
        #now = time.time()
        self.elapsed += 1

        if self.elapsed >= self.interval:
            self.time = self.elapsed
            self.elapsed = 0

            return True
        else:
            return False

class ConsoleOutput(object):
    '''A stand in for propper logging, uses logging module... how ironic'''
    def __init__(self):
        self.message_que = []
        self.message_types = {'WARNING': logging.warning, \
        'DEBUG': logging.debug, 'INFO': logging.info}

    def Write(self, logging_level, object, message):
        self.message_que.append([logging_level, object, message, time.ctime()])

    def Flush(self):
        for msg in self.message_que:

            logging_level = string.upper(str(msg[0]))
            object = msg[1]
            message = msg[2]
            time = msg[3]
            if logging_level in self.message_types:
                self.message_types[logging_level]( "@ %s : %s : \t%s" % \
                ( time, object, message ) )
            else:
                print ("@ %s : %s : \t%s") % (time, object, message )
		self.message_que = []

class SharedObjects(object):
    __scale__ = 1

    __screen__ = None

    __state__ = None

    __cameraoffset__ = (0,0) #essentialy camera topright

    __animation_step__ = 10

    __movement_delta__ = 0

    # __output__ = ConsoleOutput()

    __paused__ = False

    __surface_flush_color__ = (255,255,255) #(0,0,0) #

    __redrawrequested__ = False
    @classmethod
    def RedrawRequested(self):
        return self.__redrawrequested__

    @classmethod
    def setRedrawRequested(self):
        self.__redrawrequested__ = True

    @classmethod
    def Pause(self):
        self.__paused__ = (abs(self.__paused__-1))

    @classmethod
    def getPause(self):
        return self.__paused__

    # @classmethod
    # def Write(self, logging_level, object, message):
        # self.__output__.Write(logging_level, object, message)

    # @classmethod
    # def flush(self):
        # self.__output__.Flush()

    @classmethod
    def DeltaTime(self):
        return self.__movement_delta___

    @classmethod
    def setDeltaTime(self, dt):
        self.__movement_delta___ = dt

    # @classmethod
    # def DeltaTime(self):
        # return self.__movement_delta___

    # @classmethod
    # def setMovementTime(self, dt):
        # self.__movement_delta___ = dt

    @classmethod
    def setState(self, state, default = None):
        if self.__state__ is not state :
            self.__state__ = state
            return True
        else:
            self.__state__ = default
        return False
    @classmethod
    def State(self):
        return self.__state__

    @classmethod
    def setScale(self, scale ):
        self.__scale__  = scale
    @classmethod
    def Scale(self):
        return self.__scale__

    @classmethod
    def setScreen(self, screen):
        self.__screen__ = screen
    @classmethod
    def Screen(self):
        return self.__screen__

    @classmethod
    def setCameraOffset(self, xy):
        self.__cameraoffset__ = xy
    @classmethod
    def CameraOffset(self):
        return self.__cameraoffset__

    @classmethod
    def setAnimationStep(self, flag):
        self.__animation_step__ = flag
    @classmethod
    def AnimationStep(self):
        return self.__animation_step__

    @classmethod
    def setFlushColor(self, color):
        self.__surface_flush_color__ = color
    @classmethod
    def FlushColor(self):
        return self.__surface_flush_color__

class Camera(SharedObjects):
    def __init__(self, rect, origin_coord):
        self.rect = rect
        self.topleft = origin_coord
        self.vect = (0,0)

    def set_drag_point(self, draged_topleft):
        self.draged_topleft = draged_topleft

    def button_down(self, mouse_pos, draged_topleft):
        self.draged_topleft = draged_topleft
        self.start = mouse_pos
        self.current = self.start
        self.clicked = True

    def button_up(self, pos):
        self.current = pos
        #self.draged_origin = None #
        self.clicked = False
        return (self.draged_topleft[0] - self.current[0], self.draged_topleft[1] - self.current[1])

    def _get_vect(self):
        return (self.start[0] - self.current[0], self.start[1] - self.current[1])

    def movement(self):
        self.vect = self._get_vect()
        movement = self.draged_topleft[0] - self.vect[0], self.draged_topleft[1]- self.vect[1]
        return movement

class AnimateBase(object):
    '''to be used in conjuction with SharedObjects'''
    current_frame = 0

    def check_frame(self, frame_list, frame):
        if frame+1 > len(frame_list)-1:
            frame = 0
        else:
            frame+=1
        return frame

    def animate(self, frame_list):
        if self.get_animation_step() == True:
            self.current_frame = self.check_frame(frame_list , self.current_frame )

    def set_frame(self, current_frame):
        self.current_frame = current_frame

class ObjectBase(SharedObjects, AnimateBase):

    x,y = None, None

    def set_pos(self, x,y):
        self.x = x
        self.y = y
    def get_pos(self):
        pass
    def set_coord(self, x,y):
        worldoffset = self.get_worldoffset()
        scale = self.get_scale()

        self.x = (-x + worldoffset[0])/ scale
        self.y = (-y + worldoffset[1])/ scale

    def get_coord(self):
        worldoffset = self.get_worldoffset()
        scale = self.get_scale()

        x = worldoffset[0] - (self.x * scale)
        y = worldoffset[1] - (self.y * scale)
        return (x,y)

    def move(self, x, y):
        #coord = self.get_coord()
        #scale = self.get_scale()

        nx = self.x - x #* scale
        ny = self.y - y #* scale
        self.set_coord(nx, ny)

class SpriteStore(object):
    def __init__(self, surf, rects, gids, animations, names):
        self.surface = surf #single bitmap
        self.rects = rects #all frames
        self.gids = gids #to frames
        self.animations = animations #name : rects
        #do mapping by name too

        self.animation = 0
        self.frame_gid = 0
        self.frame_id = 0


    def get_frame(self):
        anim = self.animations[self.animation]
        if len(anim) < self.frame_id:
            return anim[selg.frame_gid + self.frame_id]

    def get_frame_by_gid(self):
        return self.gid[self.frame_gid]
    #mapping a frame number to a surface with animation cycles!
        #cycle = self.animations['walking']
        #frame_id = cycle[currentframe]
        #frame_surf = self.sprites[frame_id]
        #blit etc


class Entity(pygame.sprite.Sprite, ObjectBase):
    def __init__(self, pos, spritestore):
        pygame.sprite.Sprite.__init__(self)

        self.image = sprites[self.current_frame]
        self.rect = self.image.get_rect()
        self.sprites = spritestore

        #finer grained movement than a rect can do (float vs int)
        self.x = pos[0]
        self.y = pos[1]

    def draw(self):
        self.animate()
        #set sprite image
        self.image = self.sprites[self.current_frame]
        topleft = self.get_coord()
        self.rect.topleft = topleft
        self.get_screen().blit(scale(self.image, self.get_scale()), topleft)

class SpriteRender(pygame.sprite.Sprite):
    def __blit(sp):
        sp = sp[0]
        coord = sp[1]
