
import os, math, string, logging
import weakref

#from numpy import array

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
#i might see a speed up if I use array (3 - 42!!!??? times faster)


class TMXTiler(Tmxtlistener, Dragable, SharedObjects):
    '''TMXTiler is a very simple example of a smooth motion tiler\n \
        we use a single image and blit subsurface rects
       Methods: to do '''

    def __init__(self, MapObj, ViewArea, ViewXY = (0,0) ):
        #for i in [SharedObjects, MouseListener, Dragable]:
        super(TMXTiler, self).__init__()

        self.RenderManager.attach(self)

        self.proc_map(MapObj)

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

    def proc_map(self, map):
        self.map = map

        # compound = []
        # for l in self.map.getLayers():
            # if l.getVisible() is 1:
                # new = array(l.data.ordered)
                # new = new.reshape(new.shape[1] * new.shape[0], 1)
            # #exit()
            # compound.append(new)

        # self.map.numpy_data = compound
        self.redraw = True

    def get_local_coords(x,y):
        pass
    def _to_tile(self, x, y):
        scale = SharedObjects.Scale()
        wo = self.CameraOffset()

        x = x + self._fine_offset_x_ - ( wo[0] * scale)
        y = y + self._fine_offset_y_ - ( wo[1] * scale)

        tilewidth =  self.map.getMapTileWidth() * scale
        tileheight =  self.map.getMapTileHeight() * scale

        x = x / tilewidth
        y = y / tileheight

        return (y, x)

    def _to_coord(self, tile_index):
        scale = SharedObjects.Scale()
        #????this needs wo var????
        #????wo = self.get_cameraoffset()????

        tilewidth =  self.map.getMapTileWidth() * scale
        tileheight =  self.map.getMapTileHeight() * scale

        x = tile_index[1] * tilewidth
        y = tile_index[0] * tileheight

        #wo = (self.x, self.y)
        wo = SharedObjects.CameraOffset()

        ### working
        screen_x = ( wo[0] * scale) + x - self._fine_offset_x_
        screen_y = ( wo[1] * scale) + y - self._fine_offset_y_

        return (screen_x, screen_y)

    def _iter_scrn(self, scale, screen_size, map_width, map_height, tile_lead):
        ## look for faster ways to do this
        ### Seamless
        xitrs = xrange( -tile_lead , (screen_size[0] / map_width)/ scale + tile_lead)
        yitrs = xrange( -tile_lead , (screen_size[1] / map_height)/ scale + tile_lead )

        for l in self.map.getLayers():
            if l.getVisible() is 1:
                for y in yitrs:
                    for x in xitrs:
                        yield(x , y , l)

    def draw_dividers(self, screen):
        pass

    def _render(self, screen):
        #map(self._draw_tile, self._iter_scrn() )
        scale = SharedObjects.Scale()

        tilewidth = self.map.getMapTileWidth()
        tileheight = self.map.getMapTileHeight()
        layers = self.map.getLayers()
        #gid = self.map.tiles.globalID

        worldoffset = self.CameraOffset()

        #len_data_ordered = len(layer.data.ordered) -1
        len_map_y = self.map.getMapHeight()
        len_map_x = self.map.getMapWidth()

        #scale tilesets
        tilesets = self.map.tiles.tilesets

        screen_size = self.Screen().get_size()
        #for l in self.map.Layers.numpy_data:
        #    draw = l[((worldoffset[0] / tilewidth), (worldoffset[1] / tileheight))

        for z in self._iter_scrn(scale, screen_size, tilewidth, tileheight, self._tile_lead_):
            x = z[0]-(worldoffset[0] / tilewidth)
            y = z[1]-(worldoffset[1] / tileheight)
            layer = z[2]
            tile_id = self.map.getTileByIndex(x,y, layer)

            if (tile_id != 0) and (0 <= y <= len_map_y) and (0 <= x <= len_map_x):
                tile = self.map.getTileByGID(tile_id)
                real_tile = self.map.getTileSurface(tile[0], tile[1])
                real_tile.set_alpha(layer.getOpacity())
                screen.blit(surface.scale(real_tile, scale ) , (self._to_coord((y,x)), (tilewidth, tileheight)))

    def draw(self, screen):
        #NOTE: using many layers kill this little tiler!
        if self.redraw or SharedObjects.RedrawRequested():
            self._internal_surface_.fill(SharedObjects.FlushColor())
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
            #scale = SharedObjects.Scale()
            mv =  self.movement()
            SharedObjects.setCameraOffset((-mv[0], -mv[1]))
            self.x, self.y = -mv[0], -mv[1]