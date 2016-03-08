import os, string
from string import join
import pygame

from shared import SharedObjects, Timer
from loaders.fileoperations import ConfigReader
from myEvents.controlers import RenderManager, EventManager

def PathToString(path):
    #return string.join(path, os.path.sep)
    return path

class Paths(object):
    def __init__(self ):
        tmp = os.path.abspath(__file__)
        #remove current dir from path
        #tmp = tmp.split(os.path.sep)
        for i in range(2):
            tmp = (tmp[0:(tmp.rfind(os.path.sep))])
        #tmp = tmp.split()[0]
        print(tmp)
        #tmp = os.path.join(*tmp[:len(tmp) - 2])
        #print(tmp)
        self.base = tmp
        self.config = os.path.join(tmp, 'config')
        self.assets = os.path.join(tmp, 'assets')
        self.save = os.path.join(tmp, 'save')

    def join(self, path, file):
        #return pathstring(os.path.join(path, file))
        return string.join(os.path.join(path, file))


class Timers(object):
    def __init__(self, anim_step):
        self.animation_timer = Timer(anim_step)
        self.framerate = pygame.time.Clock()

class Game(SharedObjects):
    pygame.init()
    def __init__(self):
        super(Game, self).__init__()
        #setup path in a new namespace
        self.paths = Paths()
        print( '%s \t Set Up Paths') %self
        #read variables into this class another way to do this
        self.read_conf(PathToString(os.path.join(self.paths.config, 'config.txt')))
        print( '%s \t Loaded Config File') %self
        self.timers = Timers(self.animstep)
        SharedObjects.setAnimationStep(self.animstep)
        SharedObjects.setScale(self.scale)
        SharedObjects.setDeltaTime(self.deltatime)
        print( '%s \t Set some variables') %self
        self.display = self.init_display(self.res, self.fullscreen)
        print( '%s \t Initialised Display') %self
        #EventManager
        self.eventmanager = EventManager()
        #RenderManager
        self.rendermanager = RenderManager()
        print( '%s \t Setup Event and Render Managers') %self

    def read_conf(self, file):
        conffile = ConfigReader(file)
        for i in conffile.dict.items():
            vars(self)[i[0]] = i[1]

    def init_display(self, res, fullscreen = None):
        display = pygame.display
        if fullscreen != False:
            screen = display.set_mode(self.res, pygame.FULLSCREEN, 32)
        else:
            screen = display.set_mode(self.res, pygame.DOUBLEBUF | pygame.RESIZABLE)
        SharedObjects.setScreen(screen)
        return display

    def get_fps(self):
        return int(self.timers.framerate.get_fps())

    def update(self):
        SharedObjects.update()
        if self.timers.framerate.tick(self.fps):
            #print self.get_fps()
            #tick for animations etc.
            SharedObjects.setAnimationStep(self.timers.animation_timer.Update())
            #loop through events
            self.eventmanager.post()
            #draw stuff
            self.rendermanager.render(self.display, self.getScreen(), self.getFlushColor(), None)
            #self.rendermanager.render(self.display, self.offscreen_surf, self.FlushColor(), None)

    notify = update

# if __name__ == '__main__':
    # g = Game()
    # print dir(g)
    # l = Listener()
    # l2 = Listener()
    # g.update()

    # print l
    # print l.RenderManager
    # print l.EventManager
    # print l2.RenderManager
    # print l2.EventManager
