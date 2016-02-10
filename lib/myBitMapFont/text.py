import pygame
from pygame.locals import *

from ..lib.loaders.load_little_assets import ImageSets
from ..lib.loaders.tilesheet import *

def load_font(path, ref):
    assets = ImageSets(path)
    img = assets.spider()
    rects = assets.split(ref, 1, (8,8))
    
    rects = rects.values()
    
    ##pack num_d
    bold_rects = rects[106:202]
    bold_num = bold_rects[0:10]
    num_d = {}
    
    for i in range(len(bold_num)-1):
        num_d[i] = bold_num[i]
    #print num_d
        
    #pack lower_alph_d
    lower_l = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    bold_alph_lower = bold_rects[30:59] #??
    lower_alph_d = {}

    for i in range(len(lower_l)):
        #print i, lower_l[i]
        try:
            lower_alph_d[lower_l[i]] = img[ref].subsurface(bold_alph_lower[i])
        except:
            print i, 'outside surface area'
    
    # #pack upper_alph_d
    # upper_l = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    # bold_alph_upper = bold_rects[57:]
    # upper_alph_d = {}
    # for i in range(len(lower_l)):
        # #print i, upper_l[i]
        # upper_alph_d[upper_l[i]] = bold_alph_upper[i]
    
    rects = bold_num
    return (lower_alph_d)