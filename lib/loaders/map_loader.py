import os, string

import pygame
from pygame.locals import *

from image import load_image

from struct import unpack
from simplexml import OpenXML as OpenXML

#from MapLoaderSupport.wrapper_classes import Map, Layer, Tileset, Data
from MapLoaderSupport.wrapper_classes import MapContainer, Layer, Tileset, Data, FormatConstants
from MapLoaderSupport.helper_functions import convert, BuildGIDList, BuildTileRects

class StorageClass(object):
    pass

class ReadMap(OpenXML):
    ''' should be fairly complete '''
    def __init__(self, filepath):
        super(ReadMap, self).__init__(filepath)
        #this doent need to be instanced
        #self.format = FormatConstants()
        self.current_name_space = None
        self.proto_map = None
        self.function_map = {FormatConstants.default: StorageClass,\
                            FormatConstants.data: Data,\
                            FormatConstants.layer : Layer,\
                            FormatConstants.tileset : Tileset,\
                            FormatConstants.map :StorageClass,\
                            FormatConstants.properties : dict,\
                            FormatConstants.tile : dict} # StorageClass

    def iterNodeVars(self, attr, namespace):
        if attr != None :
            for attr in attr.items():
                k = str(attr[0])
                v = convert(attr[1])
                #print 'var', k,v
                vars(namespace)[k] = v

    def iterNodeData(self, attr, namespace):
        k = 'data'
        if attr != None:
            v = string.strip(attr)
            if len(v) is 0:
                pass #print self,':', k, 'is:', v, '''it's len() is:''', len(v), ': This data may have been mangled by the tmx map loader and has not been loaded'
            else:
                vars(namespace)[k] = v

    def parse(self, asset_path):

        self.proto_map = MapContainer()
        self.proto_map.layers = []
        self.proto_map.tilesets = dict()

        print self, ': Reading map data'

        child = self.dom.firstChild
        self.spider(child, self.proto_map, self.proto_map)
        #print dir(self.proto_map.map.layer)
        #exit()
        map = self.post(asset_path)
        return map

    def spider(self, node, namespace, mapobj):
        if node != None:

            SpecialCaseFlag = None

            if node.hasChildNodes():

                name = convert(node.localName)

                print 'in', namespace,' in node:', name #, namespace

                try:
                    obj = self.function_map[name]()
                except KeyError:
                    obj = self.function_map[FormatConstants.default]()

                if name == FormatConstants.layer:
                        mapobj.layers.append(obj)

                elif name == FormatConstants.tileset:
                    mapobj.tilesets[convert(node.getAttribute(FormatConstants.name))] = obj

                #special cases for dicts
                #generalise and combine these two
                elif name == FormatConstants.properties:
                    SpecialCaseFlag = FormatConstants.properties
                    #vars(namespace)[FormatConstants.properties] = obj
                    if hasattr(namespace,FormatConstants.properties):
                        obj = vars(namespace)[FormatConstants.properties]
                    else:
                        vars(namespace)[FormatConstants.properties] = obj

                elif name == FormatConstants.tile:
                    SpecialCaseFlag = FormatConstants.tile
                    #vars(namespace)[FormatConstants.tile] = obj
                    #vars(namespace)[FormatConstants.properties] = obj
                    #vars(namespace)["properties"] = obj
                    if hasattr(namespace,FormatConstants.properties):
                        obj = vars(namespace)[FormatConstants.properties]
                    else:
                        vars(namespace)[FormatConstants.properties] = obj

                else:
                    ## Otherwise
                    ## create a storage class of name [name]
                    vars(namespace)[name] = obj

                if SpecialCaseFlag is None:
                    namespace = obj


            if SpecialCaseFlag is None:
                self.NodeHasChild(node, namespace)

                for child in node.childNodes:
                    self.spider(child, namespace, mapobj)
                    child = child.nextSibling

            ##be very carefull adding spacial cases
            if (SpecialCaseFlag is FormatConstants.tile):
                def get_tile(node, obj):
                    a = node.childNodes[1] #YES!
                    b = a.childNodes[1] #holds nothing
                    c = b.attributes.items() #YES!
                    # print node.attributes.items()
                    # print a
                    # print b
                    # print c
                    id = node.attributes.items()
                    #print id
                    tile_info = StorageClass()
                    tup = []
                    for i in c:
                        tup.append(i[1])
                        if len(tup) is 2:
                            #add to storage class
                            print tup
                            vars(tile_info)[str(tup[0])] = convert(tup[0])
                            tup = []

                    # obj[tile_info] = [convert(id[0][1])]
                    obj[convert(id[0][1])] = tile_info

                get_tile(node, obj)

            elif (SpecialCaseFlag is FormatConstants.properties):
                def get_properties(node):
                    if node.hasChildNodes():
                        for child in node.childNodes:
                            if child.attributes is not None:
                                tup = []
                                for i in child.attributes.items():
                                    #print i
                                    tup.append(i[1])
                                    # attrubutes are in key value pairs so for 1
                                    # key/value pair we need to do 2 iterations
                                    if len(tup) is 2:
                                        yield tup
                        get_properties(node.nextSibling)

                for i in get_properties(node):
                    #print i
                    obj[convert(i[0])] = convert(i[1])
                    #print obj


    def NodeHasChild(self, node, namespace):
        if hasattr(node, FormatConstants.attributes):
            self.iterNodeVars(node.attributes, namespace)
        if hasattr(node, FormatConstants.data):
            self.iterNodeData(node.nodeValue, namespace)

    def post(self, asset_path):
        #postprocess data
        count = 0
        for l in self.proto_map.layers:
            print self, ': Decompressing data in layer'
            l.data.ProcessData()
            #and organise map data
            print self, ': Creating tile map array'

            #print dir(self.proto_map)
            #print self.proto_map.layers
            #print self.proto_map.layers

            l.data.getOrdered(self.proto_map.map.width, self.proto_map.map.height)

        print self, ': Loading tilesets'
        tilesets = self.proto_map.tilesets
        self.proto_map.tiles = StorageClass()
        for t in tilesets.items():
            #print t
            #print(asset_path)
            #print os.path.sep.join(t[1].source[3:].split('/'))
            #exit()
            path = asset_path + os.path.sep + os.path.sep.join(t[1].source[3:].split('/'))
            #path = string.join(path, os.path.sep)
            t[1].image = load_image(path)

            #order is important
            v = ['tileheight', 'tilewidth', 'margin', 'spacing']
            args = []
            for i in v:
                if hasattr(t[1], i):
                    args.append(vars(t[1])[i])
                else:
                    args.append(0)
                #args.append(x)

            t[1].rects = BuildTileRects(t[0], t[1].image, args[0], args[1], args[2], args[3])

        #FIXME - quick work around
        self.proto_map.tiles.tilesets = tilesets
        self.proto_map.tiles.globalID = BuildGIDList(tilesets)
        #print self.proto_map.tiles.globalID.items()[0]

        # #change local property gids to global ones
        # for tileset in tilesets.values():
            # if hasattr(tileset, 'properties'):

            # #print tileset.__dict__
            # count = 0
            # for tile in tileset.rects:
                # gid[tileset.firstgid + count] = tileset.rects[count]

                # count+=1

        # def check_gid(self, map):
            # ret = False
            # #print id
            # #try:
            # tile_id = self.raw.layers[0].data.ordered[id[0],id[1]]
            # print id, tile_id
            # if tile_id > 0:
                # tile_set = self.raw.tiles.globalID[tile_id][0]
                # print tile_set
                # tile_set_obj = self.raw.tiles.tilesets[tile_set]
                # if hasattr(tile_set_obj, 'properties'):
                    # #prop = tile_set_obj.properties
                    # if hasattr( tile_set_obj.properties, keyword):
                        # ret = True



        del self.proto_map.tilesets
        return self.proto_map

if __name__ == "__main__":
    import pygame
    from pygame.locals import *


    pygame.init()

    res = (200,200)
    fps = 30

    display = pygame.display
    screen = pygame.display.set_mode(res)

    clock = pygame.time.Clock()

    #map = ReadMap(os.path.join('''F:\\src\\py_src\\pygame\\rp\\assets\\maps\\test_property_test.tmx'''))
    map = ReadMap(os.path.join('''F:\\src\\py_src\\pygame\\rp\\assets\\maps\\test_pathfinding.tmx'''))
    #print map, map.__dict__
    obj = map.parse(string.split('F:\\src\\py_src\\pygame\\rp\\assets', '\\'))

    #obj
    #    map obj
    #   tiles
    #       globalID list
    #       tilesets dict
    #           tileset obj
    #    layers list
    #        layer obj
    print 'map container'
    print dir(obj)#.__dict__ #ERROR
    print 'container.map'
    print dir(obj.map)#.__dict__ #ERROR
    #print obj.tiles.globalID
    print obj.map.__dict__
    print 'container.layers'
    print obj.layers#.__dict__
    for i in obj.layers:#.values()
        #print i.getVisible()
        if hasattr(i, 'visible'):
            print i.visible
        else:
            print 'visible not found, default shold be visible'
    print 'container.tiles'
    print dir(obj.tiles)
    print obj.tiles.tilesets.items()[0][1].properties
    #print obj.tiles.globalID


