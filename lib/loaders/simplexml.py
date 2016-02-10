#!/usr/bin/env python

import os
from xml.dom import minidom, Node

class OpenXML(object):
    def __init__(self, fp):
        self.filepath = os.path.abspath(fp)
        #print self.filepath
        self.dom = minidom.parse(fp)
        
    def get_string(self):
        return self.dom.toxml()
        
    def get_nodes(self, tagname):
        return self.dom.getElementsByTagName(tagname)
        
    def _iter_nodes(self, nodes, name):
        for node in nodes:
            if node.nodeType == node.ELEMENT_NODE and node.nodeName == name:
                yield node #call with .next()
                
    def close(self):
        self.dom.unlink()
        
    unlink = close
    
class WriteableXML(object):
    ''' simple functions to create a document and create a minidom\
    implementation and write to file'''
    def __init__(self, path):
        self.filepath = os.path.abspath(path)        
        self.dom = minidom.getDOMImplementation()

    def newDocument(self, NameSpaceURI, QualifiedName, DocType):
        doc = self.dom.createDocument(NameSpaceURI, QualifiedName, DocType)
        return doc
        
    def Close(self):
        self.dom.unlink()
        
    def Write(self, doc):
        # if os.path.isfile(path) != True:
            # fd = open(path, 'w')
            # fd.write('')
            # fd.close()
            
        fileobj = open(self.filepath, 'w')
        fileobj.write(doc.toxml())
        fileobj.close()
        
if __name__ == "__main__":
    impref = WriteableXML("test.xml")
    doc = impref.newDocument(None, "test", None)
    el2 = doc.documentElement
    el2.elementTag('hi')
    #el2 = doc.createElement("test")
    text = doc.createTextNode("hahdasdhasdh")
    el2.appendChild(text)
    print doc.toxml()
    impref.Write(doc)
        