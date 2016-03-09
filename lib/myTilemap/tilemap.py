
import os, math, string, logging
import weakref
from itertools import product as product
#from numpy import array
from itertools import imap
import pygame
from pygame.locals import *

from ..shared import SharedObjects

from ..effects import surface #as

#events
#from ..myEvents.eventlistener import MouseListener as Tmxtlistener
from ..myEvents.eventlistener import CombinedMouseKeyBoard as Tmxtlistener

#behavior of mouse drag
from ..input import Dragable
#!!!
#from ..raycasting import RayCaster as Raycaster

#from myEvents.eventlistener import EventListener as EventListener

# While this is all fine and dandy it would be better to
# register an event ie window uncovered and only redraw the whole screen on that
# otherwise just dirty rect blit uncovered tiles

#class DrawOrderer(object):
#    def __init__(self):
#        self.layer = len(self.RenderManager.listeners)
#    def setLayer(self, layer):
#        self.RenderManager.listeners.remove[self.layer]
#        self.layer(layer):
#        self.RenderManager.listeners.insert

class TMXTiler(Tmxtlistener, Dragable, SharedObjects):
    '''TMXTiler is a very simple example of a smooth motion tiler\n \
        we use a single image and blit subsurface rects
       Methods: to do '''

    def __init__(self, MapObj, ViewArea, ViewXY = (0,0) ):
        ## for i in [SharedObjects, MouseListener, Dragable]:
        super(TMXTiler, self).__init__()
        self.map = MapObj
        self.redraw = True
        self.x = ViewXY[0] #pretty much unused!
        self.y = ViewXY[1]
        self._internal_surface_ = pygame.surface.Surface(ViewArea)
        self._view_height_ = ViewArea[0]
        self._view_width_ = ViewArea[1]
        self._fine_y_ = self._view_height_ / self.map.getMapTileHeight()
        self._fine_x_ = self._view_width_ / self.map.getMapTileWidth()
        ## out of power of 2 tiles? sometimes zero game.game.result?
        self._fine_offset_x_ = self._view_width_ & (self.map.getMapTileWidth()-1) 
        self._fine_offset_y_ = self._view_height_ & (self.map.getMapTileHeight() -1)
        self._tile_lead_ = 1#int(self.map.tileheight / self.map.tilewidth)
    
    def get_local_coords(x,y):
        pass
        
    def _to_tile(self, x, y):
        scale = SharedObjects.getScale()
        wo = self.getCameraOffset()
        x = x + self._fine_offset_x_ - ( wo[0] * scale)
        y = y + self._fine_offset_y_ - ( wo[1] * scale)
        tilewidth =  self.map.getMapTileWidth() * scale
        tileheight =  self.map.getMapTileHeight() * scale
        x = x / tilewidth
        y = y / tileheight
        return (y, x)

    def _to_coord(self, tile_index):
        scale = SharedObjects.getScale()
        tilewidth =  self.map.getMapTileWidth() * scale
        tileheight =  self.map.getMapTileHeight() * scale
        x = tile_index[1] * tilewidth
        y = tile_index[0] * tileheight
        wo = SharedObjects.getCameraOffset()
        ## working
        ## will draw 3x extra area to the top right of the player without extra checks
        screen_x = ( wo[0] * scale) + x - self._fine_offset_x_
        screen_y = ( wo[1] * scale) + y - self._fine_offset_y_
        return (screen_x, screen_y)

    def draw_dividers(self, screen):
        pass

    def _render(self, screen):
        scale = SharedObjects.getScale()
        tilewidth = self.map.getMapTileWidth()
        tileheight = self.map.getMapTileHeight()
        layers = self.map.getLayers()
        worldoffset = self.getCameraOffset()
        tile_lead = self._tile_lead_
        len_map_y = self.map.getMapHeight()
        len_map_x = self.map.getMapWidth()
        #scale tilesets
        screen_size = self.getScreen().get_size()
        map_width = tilewidth
        map_height = tileheight
        xiters = range( -tile_lead , (screen_size[0] / map_width)/ scale + tile_lead)
        yiters = range( -tile_lead , (screen_size[1] / map_height)/ scale + tile_lead)
        tile_id = self.map.getTileByIndex#(x,y, layer)
        getTile = self.map.getTileByGID
        getTileSurf = self.map.getTileSurface
        getTileCoord = self._to_coord
        screenBlit = screen.blit
        sScale = surface.scale
        def __blitTile__(a):
            x = a[0]-(worldoffset[0] / tilewidth)
            y = a[1]-(worldoffset[1] / tileheight)
            l = a[2]
            tid= tile_id(x,y, l)
            if ((tid != 0) & (0 <= y <= len_map_y) & (0 <= x <= len_map_x)) & (l.getVisible()==1):
                rt = getTile(tid)
                s = getTileSurf(rt[0],rt[1])
                s.set_alpha(l.getOpacity())
                T = sScale(s, scale )
                screenBlit(T,(getTileCoord((y,x)), (tilewidth, tileheight)))
        map(__blitTile__, [(x,y,l) for l in layers for y in yiters for x in xiters])

    def draw(self, screen):
        if self.redraw or SharedObjects.getRedrawRequested():
            self.redraw = False
            self._internal_surface_.fill(SharedObjects.getFlushColor())
            self._render(self._internal_surface_)
            self.redraw = False
        screen.blit(self._internal_surface_, (0,0))

    def change_tile(self, layer, tile_idx, new_gid):
        #self.self.map.layers[self.self.map.layer_order[layer]].data.ordered[tile_idx[0]][tile_idx[1]] = new_gid
        self.self.map.setTileByIndex(new_gid, tile_idx, layer)
        self.redraw = True

    ## EVENT OVERRIDES
    def onDraw(self, screen, event):
        self.draw(screen)

    def on_key_down(self, event):
        self.redraw = True

    def on_mouse_button_down(self, event):
        self.clicked = True
        self.button_down( 1, event.pos, (-self.x, -self.y))

    def on_mouse_button_up(self, event):
        self.clicked = False
        self.button_up(0, event.pos )

    def on_mouse_motion(self, event):
        if self.clicked and (Tmxtlistener.Blocking is None):
            self.redraw = True
            self.moved(event.pos)
            mv = self.movement()
            SharedObjects.setCameraOffset((-mv[0], -mv[1]))
            self.x, self.y = -mv[0], -mv[1]