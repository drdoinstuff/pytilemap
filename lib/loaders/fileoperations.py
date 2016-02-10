import pygame
from pygame.locals import *

import os,sys, time, string

import type_cast

def fileatonce(path):
    path = os.path.abspath(path)
    #if os.path.exists(path):
    fd = open(path)
    data = fd.read()
    fd.close()
    return data

def mseek(data, txt_from, txt_to):
    tmp = []
    for l in data:
        if l[0] == txt_from:
            while l[len(l)-1] != txt_to:
                tmp.append(l)
            return tmp

class ConfigReader(object):
        ''' used for configuration'''
        def __init__(self, path):
            self.data = fileatonce(path)
            #remove tabs and newlines
            tmp = self.data.strip('\t')
            tmp = self.data.splitlines()
            tmp_lst = []

            for i in tmp:

                if (len(i) > 0) and ( i[0] != ( u'#' or '#' ) ):
                #iff it's not a comment or empty line
                    ttmp = i.split(' ')
                    #print ttmp
                    if ttmp != []:
                        tmp_lst.append(ttmp)
            self.list = tmp_lst
            #print self.list
            del tmp_lst, tmp
            self.index()
        def __iter__(self):
            start = 0
            while start < len(self.list):
                yield self.list[start]
                start+=1

        def next(self):

                frm = self.place
                to = self.place + self.linelimit
                self.place = self.place + self.linelimit
                return self.data[frm:to]

        def get_doc(self):
            return self.data

        def index(self):
            self.dict ={}
            for t, k, v in self.__iter__():
                #print '+++',v, type(v)
                v = type_cast.convert(t, v) #'True' = False error here
                #print '__',v, type(v)
                self.dict[k] = v

class TextDocument(object):
        def __init__(self, path):
                self.data = fileatonce(path)
                #remove tabs and newlines
                tmp = self.data.strip('\t')
                tmp = self.data.splitlines()
                tmp_lst = []

                for i in tmp:
                    #print '#'
                    #print i
                    #print '#'
                    if (len(i) > 0) and ( i[0] != ( u'#' or '#' ) ): #iff it's not a comment or empty line
                        x = i.split(' ')
                        ttmp = []
                        #split everything into component words
                        for j in x:
                            #if (j != '' ): #ignore empty lines #redundant
                                #print j, type(j)
                                ttmp.append(j)


                        if ttmp != []:
                            tmp_lst.append(ttmp)
                self.list = tmp_lst
                del tmp_lst, tmp

        def __iter__(self):
            start = 0
            while start < len(self.list):
                yield self.list[start]
                start+=1

        def next(self):

                frm = self.place
                to = self.place + self.linelimit
                self.place = self.place + self.linelimit
                return self.data[frm:to]

        def get_doc(self):
            return self.data

        def index(self):
            self.dict ={}
            for t, k, v in self.__iter__():
                #print v
                v = type_cast.convert(t, v)
                self.dict[k] = v

if __name__ == "__main__":
    #path = os.path.join('./','fileoperations.py')
    path = os.path.join('..','..','assets','ui','hud2', 'element.txt')
    t = ConfFile(path)
    #print '###'
    # t.get_doc()
    #print '###'
    #for i in t:
    #    print i
    t.index()
    print t.dict.items()
