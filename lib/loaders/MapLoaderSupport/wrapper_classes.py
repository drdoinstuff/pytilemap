import base64, gzip, StringIO
#from .image import load_image
from ..type_cast import convert

class FormatConstants(object):
    default = 'default'
    #a minimum set of contants that make it easy to read the format
    map = 'map'
    tile = 'tile'
    tileset = 'tileset'
    layer = 'layer'
    name = 'name'
    data = 'data' #  is equiv to node.nodeValue???
    attributes = 'attributes'
    properties = 'properties'
    name = 'name'
    value = 'value'
    visible = 'visible'
    
class Data(object):
    ''' decode base64, unzip, read 4 byts at a time'''
    def getOrdered(self, width, height ):
        def _gen_(width):
            for i in range(0, len(self.data), width):
                yield i  
        ordered =[]
        part = _gen_(width)
        for i in part:
            ordered.append(self.data[i:i+width])
        self.ordered = ordered
        return ordered
        
    def ProcessData(self):
        self.raw_data = self.data
        z = self._decode_data(self.data)
        self.data = self._decompress_data(z)
        return self.data
    
    def _iter_nodes(self, nodes, name):
        for node in nodes:
            if node.nodeType == node.ELEMENT_NODE and node.nodeName == name:
                yield node #call with .next()
                
    def _decode_data(self, data):
        return base64.b64decode(data)
    
    def _decompress_data(self, b64_dec):
        stream = StringIO.StringIO(b64_dec)
        gzipper = gzip.GzipFile(fileobj=stream)
        s = gzipper.read()
        #rewrite stolen code - cheers dude!
        decoded_content = []
        for idx in xrange(0, len(s), 4):
            val = ord(str(s[idx])) | (ord(str(s[idx + 1])) << 8) | \
                 (ord(str(s[idx + 2])) << 16) | (ord(str(s[idx + 3])) << 24)
            decoded_content.append(val)
        self.data =  decoded_content
        return self.data

class MapContainer(object):
    def getLayer(self, l):
        return self.layers[l]
    def getLayers(self):
        for i in self.layers:
            yield i
    # def setTileByIndex(self, x, y):
        # pass
    def getTileProperties(self, gid):
        tile_set = self.tiles.tilesets[ self.getTileByGID(gid)[0] ]
        local_gid = gid - tile_set.firstgid
        #print tile_set.properties
        #if local_gid in tile_set.properties: #.keys()
        for i in tile_set.properties: #.keys()
            #print i
            if i == local_gid:
            #print dir(tile_set.properties[local_gid])
                return tile_set.properties[local_gid]
    def getTileByIndex(self, x, y, layer):
        try:
            tile_id = layer.data.ordered[y][x]
        except IndexError:
            tile_id = 0
        return tile_id
    def getTileSurface(self, tile_name, rect):
        return self.getTileset(tile_name).image.subsurface(rect)
    def getTileset(self, name):
        return self.tiles.tilesets[name]
    def getTileByGID(self, tile_id):
        try:
            tid = self.tiles.globalID[tile_id]
        except KeyError:
            tid = None
        return tid
    def getMapTileWidth(self):
        return self.map.tilewidth
    def getMapTileHeight(self):
        return self.map.tileheight
    def getMapWidth(self):
        return self.map.width
    def getMapHeight(self):
        return self.map.height
        
class Layer(object):
    def getVisible(self):
        # try:
            # return convert(self.visible)
        # except:
            # return 1
        if hasattr(self, FormatConstants.visible):
            return self.visible
        else:
            return 1
    def getOpacity(self):
        try:
            opacity = 255 - int(255 * self.opacity)
        except AttributeError:
            opacity = 255
        return opacity

class Tileset(object):
    pass