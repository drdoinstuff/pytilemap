#!/usr/bin/env python

import math, weakref

class AStar(object):
    ''' this is not a 'correct' a* routine 
    but it will always pick a reasonably 
    short path, just not always the shortest'''
    
    def __init__(self, raw):
        self.raw = raw #weakref.proxy(raw)
        self.search_layer = 0
        self.nodemap = raw.getLayer(self.search_layer).data.ordered
        
        
        self.nodesize = raw.getMapTileWidth() * raw.getMapTileHeight()
        orth =  self.nodesize
        diag = math.sqrt((raw.getMapTileWidth() + raw.getMapTileHeight())^2)*2
        self.cost = {'orth': orth, 'diag': diag}
        
        self.lastpath = None
        
    def pop(self):
        if self.lastpath != None and len(self.lastpath) >= 1:
            step = self.lastpath.pop()
        else:
            step = None
        return step
        
    def search(self, start, target):
        open = [start,]
        closed = []
        
        G = {start: self.g_score(start, target)}
        H = {start: self.h_score(start, target, self.cost)}
        F = {start: self.g_score(start, target) + self.h_score(start, target, self.cost)}
        
        camefrom = {start:None} #we remove this later so do we need it?
        
        #check target first, if you cant walk on it, dont try to find it
        #early abort
        #is the target within our map?
        if 0 <= target[1] < len(self.nodemap) and 0 <= target[0] < len(self.nodemap[target[1]]):
            if self.check_gid(target[0], target[1], self.search_layer,  'walkable') is not True:
                open.remove(start)
        else:
            open.remove(start)

        last_x = None 
        while len(open) != 0:
            #get lowest f            
            #http://desk.stinkpot.org:8080/tricks/index.php/2006/10/find-the-key-for-the-minimum-or-maximum-value-in-a-python-dictionary/
            b = dict(map(lambda item: (item[1],item[0]),F.items()))
            lowest = b[min(b.keys())]
            
            #a new way?
            #max(d,key = lambda a: d.get(a))
            
            x = lowest
            
            #print 'lowest', x, G[x], H[x], F[x]
            #print 'next...'
            #remove from G,H,F
            G.__delitem__(x)
            H.__delitem__(x)
            F.__delitem__(x)
            
            if x == target:
                #return camefrom
                step = target
                path = [step,] #sometimes steps into an unwalkable tile, does it?
                while step != None:
                    step = camefrom[step]
                    path.append(step)
                path.pop() #remove None item
                
                if start == path[0]:
                    path.reverse() #from - to order
                
                self.lastpath = path
                
                return path
                
            open.remove(x)
            closed.append(x)
            
            neighbors = self.get_neighbors(x)
            
            for y in neighbors:
                eval = False                
                if y not in closed:
                    # if 0 < tile_id[0] < len(self.nodemap):
                        # if 0 < tile_id[1] < len(self.nodemap[tile_id[0]]):
                            # print tile_id
                    eval = self.check_gid(y[0], y[1], self.search_layer, 'walkable')
                    #print '!',type(eval)
                                #check other layers for blocking tiles
                                #for layer in self.raw.layer_order:
                                    #print layer, y
                                    #for i in self.raw.query_tile(y, layer):
                                    #print z
                                     #   if 'blocking' in i:
                                     #       eval = False
                                    
                tentative_g_score = self.g_score(start, x) + self.g_score(x,y)
                
                if eval == True:
                    if y not in open:
                        open.append(y)
                        tentative_is_better = True
                    elif tentative_g_score < G[y]:
                        tentative_is_better = True
                    else:
                        tentative_is_better = False 
                    
                    if tentative_is_better == True:
                        camefrom[y] = x
                        G[y] = tentative_g_score
                        H[y] = self.h_score(y, target, self.cost)
                        F[y] = tentative_g_score + self.h_score(y, target, self.cost)
                        #print y, G[y], H[y], F[y]
            last_x = x
        return last_x #failed
                    
    def check_gid(self, y, x, layer_idx, keyword):
        #ret = False
        #testing
        
        ret = False
        tile_id = self.raw.getLayer(layer_idx).data.ordered[y][x]
        #does the tile exist? ie 
        #ie is the location at y,x have a tile id of something other than 0
        try: #testing
            tile_set_name = self.raw.getTileByGID(tile_id)[0]
            #print 'tile set name: ', tile_set_name
        except:
            return False
        #print tile_set_name, tile_id
        #does the tile
        #try:
        properties = self.raw.getTileProperties(tile_id)
        #except:
        #    properties = []
        # print properties
        #if keyword in properties:#.items():
        if hasattr(properties, keyword):#.items():
            ret = True
            
        return ret
                
        
    def get_neighbors(self, n):
            y = n[0]
            x = n[1]
            
            #FIXME!
            #i dont want diagonal movement
            diagonals = [(y-1, x-1), (y-1, x+1), (y+1, x-1),(y+1, x+1)]
            tmp = [(y,x-1), (y, x+1),(y-1, x), (y+1, x)] + diagonals
            nodelist = []
            for i in tmp:
                if 0 <= i[0] < len(self.nodemap) and 0 <= i[1] < len(self.nodemap[i[0]]):
                    nodelist.append(i)
            return nodelist
            
    def g_score(self, start, target):
        g = abs(start[1] - target[1]) + abs(start[0] - target[0])
        #print 'g',g 
        return g
        
    def h_score(self, start, target, cost):
        #h(n) = D * (abs(n.x-goal.x) + abs(n.y-goal.y))
        h = cost['orth'] * abs(start[1] - target[1]) + abs(start[0] - target[0])
        return h
        
##################################################################
##################################################################
##################################################################

if __name__ == '__main__':

    import os, sys

    import pygame
    from pygame.locals import *
    
    import loaders.tmxloader_ng  as tmx
    import loaders.image

    import simple_tiler_rc  as tlr
    
    import pygame
    from pygame.locals import *

    pygame.init()

    res = (200,200)
    fps = 30

    display = pygame.display
    screen = pygame.display.set_mode(res)
    
    
    filepath = os.path.join(os.path.join(".", "loaders", "test.tmx"))

    tmap = tmx.OpenTMX(filepath)
    mapobj = tmap.parse_map()
    
    start = (7,0)
    target = (8,7)
    
    #nodemap = mapobj.layers[mapobj.layer_order[0]].data.ordered
    path =  AStar(mapobj)
    #print 'finished', path[1]
    #print 'start...'
    #for i in path.search(start, target):
    #    print i
    
    #print '...done!'
     
    #open = [] #possible squares
    #closed = [] #path to endpoint

    #1. add all points around the start point (A) that are walkable
    #   all of these squares have A as their 'parent'

    #2. remove A from the open list , add it to closed
    
    #3. chose the lowest F (f = g+h)
    #   drop it from the open list
    #   add to closed list
    #   add all nodes around it that are walkable and not on the open list
    
    #4 if the G cost is lower for a node that is already on the list, replace or keep it
    # if you replace it, recalculate the f,g,h 
    
    #5#  Add the target square to the closed list, 
    #in which case the path has been found (see note below), or
    # Fail to find the target square, and the open list is empty.
    #In this case, there is no path.
