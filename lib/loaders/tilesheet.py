import os , string

import pygame
from pygame.locals import *

from image import load_image

class SheetInfo(object):
    size = (int(), int())
    offset = (int(), int())
    
    tile_width = int()
    tile_height = int()
    
    margin = 0
    spacing = 0
    
    surface = None
    
    
class SpriteSheet(object):
    tiles = dict()
    surface = None
    
class TileSet(object):
    gid = dict()
    
    def __init__(self, free_gid, sheets):
       
        self.gid = free_gid
        self.tiles = []
        self.sheets = sheets

        
    def get_tiles(self):
        
        r = self.make_rects()
        ts = SpriteSheet
        ts.tiles = r
        ts.surface = self.sheets[0].surface
        return ts
                
    def _seq(self, offset, size, tilewidth, tileheight, margin , spacing , count):
            
            limit_x = size[0]+ offset[0]
            limit_y = size[1] + offset[1]
            for y in range(offset[1] + margin, limit_y, tilewidth + spacing):
                for x in range(offset[0] + margin,limit_x, tileheight + spacing): 
                    print ((x,y, tilewidth, tileheight), count)
                    yield ((y,x, tilewidth, tileheight), count)
                    count+=1
                    
            # for y in range(offset[1] + margin, height , tileheight + spacing):
                # for x in range(offset[0] + margin, width, tilewidth + spacing): 
                    # yield ((x,y, tilewidth, tileheight), count)
                    # count+=1
                    
    def make_rects(self):
        gid = self.gid
        tiles = self.tiles
        sheets = self.sheets
        id = 0
        for i in sheets:
            tiles = dict()
            rect_sequence = self._seq(i.offset ,i.size, i.tile_width, i.tile_height, i.margin, i.spacing, (gid + id))
            for i in rect_sequence:
                r = pygame.rect.Rect(i[0])
                tiles[i[1]] = i[0]
        return tiles
        
if __name__ == "__main__":
    import os
    import pygame
    from pygame.locals import *

    pygame.init()

    res = (200,200)
    fps = 30

    display = pygame.display
    screen = pygame.display.set_mode(res)


    clock = pygame.time.Clock()
    
    path = os.path.join('..', '..', 'assets', '_no_ownership', 'oryx_lofi_1.2', 'oryx_lofi_1.1', 'lofi_char_a.png')
    img = pygame.image.load(path)
    spritedata = []
    #1
    a = SheetInfo()
    a.size = (128,128)
    a.offset = (0,0)
    a.tile_width = 8
    a.tile_height = 8
    a.margin = 0
    a.spacing = 0
    a.surface = img
    spritedata.append(a)

    #2
    #a = SheetInfo()
    #a.size = (128,49)
    #a.offset = (0,128)
    #a.tile_width = 16
    #a.tile_height = 16
    #a.margin = 0
    #a.spacing = 0
    #a.surface = img
    
    #spritedata.append(a)
    tiles = TileSet(0, spritedata)
    tiles = tiles.get_tiles()
    
    print tiles.tiles
    
    
    
    

