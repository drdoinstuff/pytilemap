import pygame
from pygame.locals import *

def scale(image, scale):
    return pygame.transform.scale(image,(image.get_width()*scale, image.get_height()*scale))
    #return pygame.transform.rotozoom(image, 0.0, float(scale))
