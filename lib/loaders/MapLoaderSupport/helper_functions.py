import string, os

from wrapper_classes import FormatConstants as FCONST

import pygame
from pygame.locals import *

# def QueryTile(self, tile_array_position, layers, tilesets, layer = 0): #by location
    # y = tile_array_position[0]
    # x = tile_array_position[1]
    # alayer = layers[layer]
    
    # if y <= len(alayer.data.ordered) and x <= len(alayer.data.ordered[y]):
        # tile_idx = alayer.data.ordered[y][x]
        # if tile_idx in tilesets.properties:#.keys():
            # yield tilesets.properties[tile_idx]
            

def BuildGIDList(tilesets):
    #make a dict of tiles by gid
    
    gid = dict()
    
    for tileset in tilesets.values():
        # print tileset.firstgid
        # if hasattr(tileset, FCONST.properties):
            # print 'prop', type(tileset.properties.items()[0][0])
        # print dir(tileset)
        # try:
            # print "###"
            # print tileset.properties
            # print dir(tileset.properties.items()[0][0])
            # print "@@@"
        # except:
            # print 'noprop'
        count = 0
        for tile in tileset.rects:
            id = tileset.firstgid + count# -1
            gid[id] = tileset.rects[count]
            
            #also update properties o they are by global gid
            if hasattr(tileset, FCONST.properties):
                #print tileset.properties.values()
                if count in tileset.properties.values():
                    #print '!'
                    tmp = tileset.properties[count]
                    tileset.properties.__delitem__(count)
                    tileset.properties[id] = id

            count+=1
    return gid

    
def BuildTileRects(name, img, tilewidth, tileheight, margin, spacing):
    def _seq( width, height, tilewidth, tileheight, margin = 0, spacing = 0):
        count = 0
        for y in range(margin, height , tileheight + spacing):
            for x in range(margin, width, tilewidth + spacing): 
                yield ((x,y, tilewidth, tileheight), count)
                count+=1 
    tiles = dict()
    rect_sequence = _seq(img.get_width(), img.get_height(), tilewidth, tileheight, margin, spacing)
    for i in rect_sequence:
        r = pygame.rect.Rect(i[0])
        tiles[i[1]] = [name, i[0]]
    return tiles
        
def convert(obj, aType = None):
    #print obj, type(obj)
    obj = str(obj)
    
    if len(obj) == 0 and type(obj) == type(''): #a blank
        obj = 0
    #unicode 
    if len(obj) == 0 and type(obj) == type(u''): #a blank
        obj = 0
        
    elif aType != None: 
        obj = aType(obj) #t = type()
            
    elif obj == u'True' or obj == u'False':
        obj = bool(obj)
    
    # "/" is the  tiled path sep marker
    elif obj.find(os.path.sep) != -1 or obj.find("/") != -1: 
        obj = str(obj)
    
    elif obj.find('.') != -1: #floating point number
        obj = float(obj)
        
    elif (obj[0] is '(') and ( obj[len(obj)-1] is ')'):
        tup = []
        count = 0
        for i in obj:
            count+=1
            if len(obj[:count]) % 2 is 0:
                #print i
                tup.append(convert(i))
        obj = tuple(tup)
        
    elif obj[0] == '#': #a color
        #print obj[1:]
        obj = pygame.Color(str(obj))
        
    else:
        try:
            obj = int(obj)
        except:
            obj = str(obj)
            
    return obj
    
