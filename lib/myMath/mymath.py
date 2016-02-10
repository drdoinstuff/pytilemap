import math

import pygame
from pygame.locals import *

def tan_rotate( surface, p1, p2):#, surface = None):
    ''' works well if the two points are far apart \
points close together give crazy angles!'''


    #print 'p1',p1
    #print 'p2', p2
    
    ## source
    ## Nikwin
    ## http://stackoverflow.com/questions/650646/rotation-based-on-end-points

    angle = math.atan2(-(p1[1] - p2[1]) ,p1[0] - p2[0])

    ## Note that in pygame y=0 represents the top of the screen
    ## So it is necessary to invert the y coordinate when using math
    #print 'rads', angle
    
    angle = math.degrees(angle) -90 #-90 so the image point toward the mouse

    #print 'deg', angle
    #angle = angle -90
    #print 'deg -90', angle
   ### end
    
    #old_center = surface.get_rect().center
    if surface != None:
        surface= pygame.transform.rotate(surface, angle)
        return surface
    else:
        return angle
    #self.rect = self.surface.get_rect(center=old_center)


def cos_rotate(surface, p1, p2):
    #errors out with float and domain errors,
    # fix select for quadrant and dont divide by zero
    #B dot B = cos theta
    #A.B = cos(theta)
    #acos(A.B) = theta
    ''' my own interpretation of the formula above '''
    
    A = p1
    B = p2
 
    angle = math.acos( A[1] * B[2] + A[2] * b[2] )
    angle = math.degrees(angle)
    
    surface= pygame.transform.rotate(surface, angle)

    return surface



# add an argument and select behavior based on the side A/B/C or angle theta

def magnitude(p1, p2):
    magnitude = (p1[0] - p2[0] + p1[1] - p2[1])
    return math.sqrt(magnitude)

def sqrt_length(p1, p2):
    length = math.sqrt((p1[0] - p2[0] + p1[1] - p2[1]))
    return length

def sin_hyp_length(angle, p1, p2):
    #sin theta = o/h
    #h = o / sin theta
    angle = math.sin(angle)
    if angle == 0:
        angle = 1
    lenght = (p1[0]-p2[0]+ p1[1] - p2[1]) / angle
    
    return length


def point_intersect(p1, p2):
    #y = mx + b
    pass
    

def cast_vect(angle, distance):
    deg = angle
    rad = math.radians(angle)
    dx = deg * math.cos(rad)
    dy = deg* math.cos(rad) * -y

    return (dx, dy)
    
