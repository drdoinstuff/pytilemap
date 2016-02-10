#http://stackoverflow.com/questions/677978/weakref-list-in-python

import weakref

class WeakRefList(object):
    def __init__(self, *args):
        self.__list__ = list(args)
    
    def __repr__(self):
        return "WeakList(%r)" % list(self)
    
    def __getitem__(self, idx):
        return self.__list__[idx]()
        
    def __iter__(self):
        for i in self.__list__:               
            yield i
    def __len__(self):
        return len(self.__list__)
    
    def __delitem__(self, idx):
        del self.__list__[idx]
    
    def callback(self):
        list = self.__list__
        def delete_item(item):
            #try:
                list.remove(item)
            #except ValueError, exept:
                #print self, 'Cought %s trying to remove
        return delete_item
        
    def append(self, obj):
        self.__list__.append(weakref.ref(obj, self.callback()))
    
    def count(self, obj):
        return list(self).count(obj)

    def extend(self, items):
        for x in items: self.append(x)

    def index(self, obj):
        return list(self).index(obj)

    def insert(self, idx, obj):
        self.__list__.insert(idx, weakref.ref(obj, self.callback()))
        
    def pop(self):
        return self.__list__.pop()

    def push(self, obj):
        proxy = weakref.ref(obj, self.callback())

        self.__list__ = [proxy,] + self.__list__

    def remove(self, element):
        #do what I want not what I say
        try:
            self.__list__.remove(element)
        except ValueError:
            for i in self.__list__:
                if i() == element:
                    #print '!'
                    self.__list__.remove(i)

    
    def reverse(self):
        self.__list__.reverse()
        #return self.__list__
        
    def sort(self, cmp=None, key=None, reverse=False):
        if self.__list__: self.flush()
        if key is not None:
            key = lambda x,key=key: key(x())
        else:
            key = apply
        self.__list__.sort(cmp=cmp, key=key, reverse=reverse)

    def __add__(self, other):
        l = WeakList(self)
        l.extend(other)
        return l

    def __iadd__(self, other):
        self.extend(other)
        return self

    def __contains__(self, obj):
        return obj in list(self)

    def __mul__(self, n):
        return WeakList(list(self)*n)

    def __imul__(self, n):
        self.__list__ *= n
        return self

if __name__ == '__main__':
    weaklist = WeakRefList()
    stronglist = list()
    
    class Temp(object):
        count = 0
    
    z = Temp()
    z.count = 111111
    weaklist.append(z)
    
    for i in range(10):
        t = Temp()
        t.count = i
        stronglist.append(t)
        weaklist.append(t)
        
    print weaklist
    print stronglist
    
    print '!!!'
    for i in weaklist:
        if i() is z:
            weaklist.remove(i)
            #del z -- cant do this
            ## still alive
            print i, z
        print i(), i().count
    
    #z not alive at this point
    print '!!!'
    for i in weaklist:
        print i(), i().count
    
    del stronglist
    
    print '!!!'
    for i in weaklist:
        print i(), i().count