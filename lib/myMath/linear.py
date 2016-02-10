#!/usr/bin/env python

#import pygame
#from pygame.locals import *

# def Quadratic(step, a, b, param):
    # #   f(x) = ax2 + bx + c
    # ax = a[0]
    # bx = b[0]

    # ay = a[1]
    # by = b[1]

    # c = param

    # def function():
        # pass
    # return function

def LinearInterpolate(steps, a, b):
   #y = mx + b
    ax = a[0]
    bx = b[0]
    ay = a[1]
    by = b[1]
    
    x_diff = bx-ax
    y_diff = by-ay
    x_step = x_diff/float(steps)
    y_step = y_diff/float(steps)
    
    def function(ax, ay, bx, by):
        for iter in range(steps):
            ax+=x_step
            ay+=y_step
            yield (ax,ay)
    return function(ax, ay, bx, by)

# class Linear(object):
    # def __init__(self, steps, a, b):
        # self.ax = a[0]
        # self.ay = a[1]
        
        # self.bx = b[0]
        # self.by = b[1]
        
        # self.abx = self.bx - self.ax
        # self.aby = self.by - self.ay 
        
        # self.xstep = self.abx/steps
        # self.ystep = self.aby/steps
        
        # self.x = self.ax
        # self.y = self.ay
        
        # print self.abx, self.aby, self.xstep, self.ystep
        
    # def interpolate(self):
        # lst = []
        # while (self.x < self.bx) or (self.y < self.by):
            # self.x+=self.xstep
            # self.y+=self.ystep
            # yield (self.x, self.y)
            # #lst.append((self.x, self.y))
            
        # #return None
if __name__ == "__main__":
    
    print "testing linear"
    
    #l = Linear(20, (0,0), (10,2))
    #for i in l.interpolate():
    #    print i
    lin = LinearInterpolate(20, (4, 0), (-4, 0))
    #lin = LinearInterpolate(10, (0, 0), (10, 0))
    i = lin.next()
    print i
    print '#'
    for i in lin:
        print i
    print '@'  
    for i in lin:
        print type(i)
    print lin.next()
