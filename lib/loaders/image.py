import pygame
from pygame.locals import *

import os,sys, time

def load_image(filename, rect = None, colorkey = None, scale = 0, set_alpha = True):
    try:
        image = pygame.image.load(filename)
        
    except pygame.error, message:
        raise SystemExit, message
        
        image = image.convert()
        
    if scale != 0 and scale != None:
        image = pygame.transform.scale(image,(image.get_width()*scale, \
                                                image.get_height()*scale))
        
    if set_alpha == True: #prefer alpha values from image!
    
##    Surface.get_masks
##
##      the bitmasks needed to convert between a color and a mapped integer
##      Surface.get_masks(): return (R, G, B, A)
    
        alpha = image.get_masks()[3]
        
        if alpha != 0:
            image = image.convert_alpha()

    else:
        if colorkey != None: #set a provided colorkey
            image.set_colorkey(colorkey)
        elif colorkey == True: #use the top left pixel to set colorkey
            colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey)
    
    if rect != None:
        image = image.subsurface(rect)
    return image
    

def load_images(directory, file_type,  scale = None, colorkey = None): #yay!
    import os, dircache
    if os.path.exists(directory):
        file_list = dircache.listdir(directory)
        #tile_list = []
        tile_list = dict()
        for i in file_list:
            ext = i.split('.')
            #print len(ext)
            if ((len(ext) >= 2) and (ext[1] == (file_type))): #check different file names
                print 'load_images loaded: ', ext
                tile_list[ext[0]] = load_image(os.path.join(directory, i), colorkey, scale)
        return tile_list
    else:
        print 'error opening', directory
        

def load_chipsheet(path, chipset, scale = None, color_key = None):
        #data sheet format
        #[[image],[],...]
        #very similar to load images
        
        data_sheet = chipset.split('.')[0]
        data_sheet = os.path.join(''.join([path, data_sheet, '_data.txt']))
        chipset = os.path.join(''.join([path, chipset]))
        
        chipset = load_image(chipset, colorkey = color_key)

        fd = open(data_sheet)
        data = []
        
        for line in fd:
            if line[0] != '#': #commented out
               
                #line = line.strip(' ')
                line = line.strip('\n')
                line = line.split(' = ')[1]
                #line = line.strip('(')
                #line = line.strip(')')
                
                #tuple(int(s) for s in '(1,2,3,4)'[1:-1].split(','))
                line = eval(line) #replace this
                data.append(line)
        fd.close()
        
        tileset = []
        
        for entry in data:
            #print entry
            #newsurface
            #dict[tile] = name
            surf = pygame.transform.scale(chipset.subsurface(entry), (entry[1][0] *scale, entry[1][1] *scale)).convert()
            tileset.append(surf)
             
        return tileset
    
