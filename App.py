#!/usr/bin/env python

from time import time
import os, sys, time, random, math, string
#from functools import partial
import pygame
from pygame.locals import *

from lib.main import Game
from lib.myEvents.eventtype import EventTypes as EventTypes
from lib.shared import SharedObjects
from lib.shared import SimpleEvents as simpleevents
import lib.myEvents.eventlistener as eventlistener
from lib.myEvents.eventlistener import Quitter
import lib.input as input
import lib.main
from lib.myUI import myUI
from lib.myUI.Shared import UIShared
from lib.loaders.image import load_image
from lib.loaders.load_little_assets import ImageSets as IS
from lib.loaders.map_loader import ReadMap
import lib.myTilemap.tilemap  as  tilemap
from lib.game_specific.player import Avatar

class myKBD(eventlistener.KeyBoardListener, eventlistener.PushComponent, SharedObjects):
    def on_key_escape_down(self, event):
        self.push(EventTypes.push_quit)
    def on_key_down(self, event):
        self.push( EventTypes.push_redraw)
    def on_key_q_down(self, event):
        self.push(EventTypes.push_quit)
    def on_key_z_down(self, event):
        x = SharedObjects.Scale()
        SharedObjects.setScale(  x+1 )
    def on_key_x_down(self, event):
        x = SharedObjects.Scale()
        if x != 1:
            SharedObjects.setScale(  x-1 )

class ShowWin(myUI.Widget.Button):
    def __init__(self, img, pos, child_window):
        super(ShowWin, self).__init__(img, pos)
        #I think partial functions wold be sexy
        #but dont seem to fit in well with the way ive done things so far
        self.child_window = child_window
        #remove it from window_manager display list
        print self.child_window
        UIShared.window_manager.listeners.remove(self.child_window)
    def on_widget_focus(self, event):
        UIShared.window_manager.listeners.push(self.child_window)
        UIShared.focused_window = self.child_window
        #window_manager.listeners.push(self.child_window)

class CommandMoveToTile(myUI.Widget.Button):
    def __init__(self, img, pos, subject):
        super(CommandMoveToTile, self).__init__(img, pos)
        self.subject = subject
    def on_widget_focus(self, event):
        player.state = 'move'

class CommandSetZoom(myUI.Widget.Button):
    def __init__(self, img, pos, interval):
        super(CommandSetZoom, self).__init__(img, pos)
        self.interval = interval
    def on_widget_focus(self, event):
        scale = SharedObjects.Scale() + self.interval
        if scale < 1:
            scale -= self.interval
        SharedObjects.setScale(scale)
        SharedObjects.setRedrawRequested()

class CycleMap(myUI.Widget.Button):
    #need a away to update all references to the map in use!
    def __init__(self, img, pos, tiler, maps, basepath):
        super(CycleMap, self).__init__(img, pos)
        self.maps = []
        #self.tiler = weakref.proxy(tiler)
        self.tiler = tiler
        for i in maps:
            tmap = ReadMap(i)
            mapobj = tmap.parse(basepath)
            self.maps.append(mapobj)
        self.picked = 0
    def on_widget_focus(self, event):
        game.eventmanager.listeners.remove(self.tiler)
        self.tiler = tilemap.TMXTiler(self.maps[self.picked], (game.res[0], game.res[1]),(0,0))
        game.eventmanager.listeners.append(self.tiler)
        self.picked += 1
        if self.picked > len(self.maps) - 1:
            self.picked = 0

class ArtAssets(object):
    def __init__(self, path):
        self.assets = IS(path)
        #self.images = self.assets.spider()

game = Game()
# quitter just waits for quit events
quitter = Quitter()
### Keyboard listener/controler
# example of myKBD listener
# esc key pushes a quit event
kbdman = myKBD()
#SharedObjects.setFlushColor((255,255,255))
SharedObjects.setFlushColor((0,0,0))
#filepath =  string.join(game.paths.assets + ["maps", "test_pathfinding.tmx"], os.path.sep)
filepath =  game.paths.assets + os.path.sep + "maps" + os.path.sep + "test2.tmx"
## reading map data
tmap = ReadMap(filepath)
mapobj = tmap.parse(game.paths.assets)
## actual tiler- attaches to event and render manager
s = mapobj.map.properties['spawn_player_at']
scale = SharedObjects.Scale()
x = s[0] * mapobj.map.tilewidth * scale
y = s[1] * mapobj.map.tileheight * scale
mx =  (mapobj.map.width * scale/2) #- x
my =  (mapobj.map.height * scale/2) #- y
tiler = tilemap.TMXTiler(mapobj, (game.res[0], game.res[1]),(0,0))
path = os.path.sep.join([game.paths.assets, 'tiles','_no_ownership' , 'oryx_lofi_1.2' ,'oryx_lofi_1.1',])
#path = string.join(s, os.path.sep)
art = ArtAssets(path)
img =  art.assets.retrieve("lofi_char_a", ((0, 0),(8, 8)) )
s = mapobj.map.properties['spawn_player_at']
player = Avatar(img, s, tiler)
game.rendermanager.listeners.append(player)
## UI test ##
windowmanager = myUI.WindowManager()
#window 2
#makes a surface
#uses the "" name to get the sprite sheet
#and rect to make a subsurface
img1 = art.assets.retrieve("lofi_halls_a", ((67, 725),(10, 10)) )
img2 = art.assets.retrieve("lofi_halls_a", ((78, 725),(10, 10)) )
img3 = art.assets.retrieve("lofi_halls_a", ((53, 673),(10, 10)) )
img4 = art.assets.retrieve("lofi_halls_a", ((31, 725),(10, 10)) )
img5 = art.assets.retrieve("lofi_halls_a", ((41, 419),(10, 10)) )
img6 = art.assets.retrieve("lofi_halls_a", ((52, 419),(10, 10)) )
win1 = art.assets.retrieve("lofi_halls_a", ((9, 601), (55, 31)) )
#show window demo
winroot = myUI.Window(win1, (20,20))#
close = myUI.Widget.HideButton( (2,2), img2)
map1 =  os.path.sep.join([game.paths.assets, "maps", "test.tmx"])
map2 =  os.path.sep.join([game.paths.assets, "maps", "test2.tmx"])
map3 =  os.path.sep.join([game.paths.assets, "maps", "test_property_test.tmx"])
nextmap = CycleMap( (13,2), img1, tiler, [map1, map2, map3], game.paths.assets)
child = myUI.Window(win1, (60, 30))
child.attach_widget(nextmap)
child.attach_widget(close)
quit = myUI.Widget.QuitButton((2,2), img2)
widg = ShowWin((13,2), img3, child)
move = CommandMoveToTile( (24,2), img4, player)
zoomin = CommandSetZoom( (2,13), img5, 1)
zoomout = CommandSetZoom( (13,13), img6, -1)
winroot.attach_widget(widg)
winroot.attach_widget(quit)
winroot.attach_widget(move)
winroot.attach_widget(zoomin)
winroot.attach_widget(zoomout)
#FIXME widget rect argument is a tuple and rect, img should be img, rect
#intuitive order
game.eventmanager.listeners.remove(tiler)
game.eventmanager.listeners.append(tiler)

print( 'Entering Mainloop')
while True:
    game.update()
