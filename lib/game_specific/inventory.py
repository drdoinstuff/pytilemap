#!/usr/env python

import time, logging
#from ..baseobjects import AllBase.write() as write()
#@gimel's answer is correct if you can guarantee the package hierarchy he mentions.
# If you can't -- if your real need is as you expressed it, exclusively tied to 
# directories and without any necessary relationship to packaging -- then you 
# need to work on __file__ to find out the parent directory (a couple of 
# os.path.dirname calls will do;-), then (if that directory is not already on 
# sys.path) prepend temporarily insert said dir at the very start of 
# sys.path, __import__, remove said dir again -- messy work indeed, but, 
# "when you must, you must" (and Pyhon strives to never stop the programmer from
#  doing what must be done -- just like the ISO C standard says in the 
#"Spirit of C" section in its preface!-).

class Inventory(object):
    def __init__(self, size):#, config):
    
        self.size = size[0] * size[1] #stand in for grid inventory
        self.dict = {}
        self.default_attributes = {'callable': lambda x: x, 'size': 0, 'uses' : 0}
        
        
    def Get(self, key):
        #print self.dict.items()
        try:
            return self.dict[key]
        except:
            ret = self.default_attributes.copy()
            return ret
    
    def List(self):
        return self.dict.keys()
        
    def Free(self):
        return self.size - len(self.dict)
        
    def Add(self, item, callable, attributes):
        if len(self.dict) < self.size:
        
            self.dict[item] = callable
            if type(attributes) !=type(dict()):
                raise TypeError("attributes needs to be a dict")
            
            newdict = {}
            for a in self.default_attributes.items():
                newdict[a[0]] = a[1]
            for a in attributes.items():
                newdict[a[0]] = a[1]
            newdict['callable'] = callable
                
            self.dict[item] = newdict
            return True
        return False
        
    def Remove(self, item):
        self.dict.__delitem__(item)
        
    def Use(self, item):
        if item in self.dict:
            ret = self.dict[item]['callable']
            
            if 'uses' in self.dict[item]:
                if self.dict[item]['uses'] != None:
                    self.dict[item]['uses'] = self.dict[item]['uses']-1
                if self.dict[item]['uses'] == 0:
                    self.Remove(item)                    
            return ret
        #logging.warning("@ %s %s : Couldn't find a %s for %s" % (time.ctime(), str(self), 'callable', item ) )
        print("%s : Couldn't find a %s for %s" % (str(self), 'callable', item ) )
        return self.default_attributes['callable']

if __name__ == '__main__':

    inv = Inventory((1,5) )
    
    def potion(x):
        return x+1
        
    def poison(x):
        return int(x-2)
    
    print(inv, 'free spaces',inv.Free())    
    inv.Add('health', potion, {'size': 1, 'uses':4}) #, 'effects':['freeze', 'burn']})
    print(inv, 'free spaces',inv.Free())
    inv.Add('acid', poison, {'size': 1,'uses':3})
    print(inv, 'free spaces',inv.Free())
    inv.Add('poison', poison, {'size': 1, 'uses':3})
    print(inv, 'free spaces',inv.Free())
    

    print(inv, 'content', inv.List())
        
    hp = 10
    
    for i in inv.List():
        ##returns a function that takes an int 'hp'
        hp = inv.Use(i)(hp)
        #print 'info', inv.Get(i)
        print i, 'used,',inv.Get(i)['uses'],'uses left, hp now', hp
    
    inv.Use('polt')
    print '#', hp
    for i in inv.List():
        hp = inv.Use(i)(hp)
        #print 'info', inv.Get(i)
        print i, 'used,',inv.Get(i)['uses'],'uses left, hp now', hp
        
    print '#', hp
    for i in inv.List():
        hp = inv.Use(i)(hp)
        #print 'info', inv.Get(i)
        print i, 'used,',inv.Get(i)['uses'],'uses left, hp now', hp
        
    print '#', hp
    for i in inv.List():
        hp = inv.Use(i)(hp)
        #print 'info', inv.Get(i)
        print i, 'used,',inv.Get(i)['uses'],'uses left, hp now', hp
        
    print '#', hp
    for i in inv.List():
        hp = inv.Use(i)(hp)
        #print 'info', inv.Get(i)
        print i, 'used,',inv.Get(i)['uses'],'uses left, hp now', hp
    print '#', hp
    for i in inv.List():
        hp = inv.Use(i)(hp)
        #print 'info', inv.Get(i)
        print i, 'used,',inv.Get(i)['uses'],'uses left, hp now', hp
        
        
    #error example - not buffered?
    #print inv.Use('temp')(a) 