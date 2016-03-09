import os, dircache, time
from image import load_image

class ImageSets(object):
    def __init__(self, basepath):
        self.time = time.time()
        self.basepath = basepath
        self.imageset = self.spider()
        self.rects = dict()
        self.last_gid = 0
        self.bind = dict()

    def retrieve(self, name, rect):
        sheet = self.imageset[name]
        return sheet.subsurface(rect)
        
    def get_gid(self, gid):
        lst = []
        for i in self.imageset.values():
            img = i[gid].subsurf(self.rects)
            lst.append(i[gid])
        return lst
    
    def spider(self):
        directory = self.basepath
        file_type = 'png'
        colorkey = None
        scale = 1
        if os.path.exists(directory):
            file_list = dircache.listdir(directory)
            tile_list = dict()
            for i in file_list:
                ext = i.split('.')
                if ((len(ext) >= 2) and (ext[1] == (file_type))):
                    #print 'LOADED: ', ext[0]
                    tile_list[ext[0]] = load_image(os.path.join(directory, i), colorkey, scale)
            self.imageset = tile_list
            return tile_list
            
        else:
            print 'error opening', directory
    
    def split(self, name, start_gid, size, start = None, finish  = None ):
        #start--|
        #|      |
        #|      |
        #|____fin
        
        #print dir(sheet)
        sheet = self.imageset[name]
        if type(start) != tuple():
            start = (0,0)
            print 'no starting pos given starting at (0,0)'
        if type(finish) != tuple():
            finish = sheet.get_size()
            print 'no finish pos given finishing at ', finish
        gid = self.last_gid
        data = {}
        for y in range(start[1], finish[1] + size[1], size[1]):
            for x in range(start[0], finish[0] + size[0], size[0]):
                ## CHECK FOR ALPHA COLOR
                # alpha_check = False
                # ac_x = x+1
                # while (alpha_check is False):
                    # pygame.surface.Surface.get_at(ac                
                data[gid] = ((x,y),(size)) #((left, top), (width, height))
                #check size against sprite sheet
                gid+=1
        self.bind[name] = data
        self.last_gid = gid
        return data