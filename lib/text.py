import pygame
from pygame.locals import *

import baseobjects

from effects.surface import scale as scale_surf

import mymath

def list_fonts():
    font = pygame.font.get_fonts()
    return font
    
def find_installed_font(name, bold = 0, Italic = 0):
    file = pygame.font.match_font(name, bold, italic)
    

def font_to_bitmap(text, text_size, text_color, gb_color, font_file = None, anti_alias = False): #antialias setting not working
    #fix newline characters and carrage returns to stay on the surface
    font = pygame.font.Font(font_file, text_size)
    textrender = font.render(text , anti_alias, text_color, gb_color)
    return textrender

class ImageInfo(object):
    def __init__(self):
        pass
        
class Text(baseobjects.ObjectBase):
    def __init__(self, x, y, size, text, alignment = 'topleft'):
        #we want the centre location, in case the image is rotated
        self.x = x 
        self.y = y
        self.text = text
        self.size = size
        self.foregroundcolor = (0,0,0)
        self.backgroundcolor = (255,255,255)
        self.antialias = False
        
        self.alpha = 255
        
        self.font = None
        self.alignment = alignment
        
    def _rotate_(self, image, angle):
        print "rotated", image, angle
        pass
        # old_width = image.get_width()
        # old_height = image.get_height()
        
        # self.x =  self.x - (image.get_width()/2)
        # self.y =  self.y - (image.get_height()/2)
        
        # image_rotated = pygame.transform.rotate(image, angle)
        
        # new_width = pygame.get_width()
        # new_height = pygame.get_height()
        
        # new_width = (old_width/2) - (new_width/2)
        # new_height = (old_height/2) - (new_height/2)
        
    def move(self, x = 0, y = 0):
        self.x+=x
        self.y+=y
        
    def fade(self, valpha):
        x = self.alpha + valpha
        if x > 255:
            x = 255
        self.alpha = x
    def _check_text_alignment(self, w, h):
        if self.alignment == 'centre':
            yield -w/2
            yield -h/2
            
        elif self.alignment == 'topleft':
            yield 0
            yield 0
        elif self.alignment == 'topright':
            pass
        elif self.alignment == 'bottomleft':
            pass
        elif self.alignment == 'bottomright':
            pass
    def get_rendered_size(self):
        scale = self.get_scale()
        txt = font_to_bitmap( str(self.text) , self.size , self.foregroundcolor, self.backgroundcolor, self.font, self.antialias)
        txt = pygame.transform.scale(txt, (txt.get_width() * scale , txt.get_height() * scale))
        return (txt.get_width(), txt.get_height())
        
    def _render_(self):
        #here we render the text to a surface
        scale = self.get_scale()
        txt = font_to_bitmap( str(self.text) , self.size , self.foregroundcolor, self.backgroundcolor, self.font, self.antialias)
        
        
        width, height = txt.get_width() * scale, txt.get_height() * scale
        
        ##scale
        txt = pygame.transform.scale(txt, (width , height))
        
        txt.set_colorkey(self.backgroundcolor)
        txt.set_alpha(self.alpha)
        
        x,y = self._check_text_alignment(width, height)
        blit_x, blit_y = self.x +x, self.y+y
        
        #if surf == None:
        self.get_screen().blit(txt, (blit_x, blit_y))
            
    def update(self ):
        self._render_()
  
class Text(baseobjects.ObjectBase):
    ''' very simple hud'''
        
    def __init__(self, text, x , y , size, fg, bg, font = None,\
                antialias = False, gettext = None):
        
        self.text = text
        
        self.x = x
        self.y = y
        
        self.font_size = size
        
        #convert from string to color?
        self.fg = fg
        self.bg = bg
        
        self.font = font
        self.antialias = antialias
        
        self.gettext = gettext
        
        
    def get_text(self):
        self.text = self.gettext()
    
    def set_text(self, text):
        self.text = text
        
    @classmethod
    def set_style(self, size, fg, bg, font = None, antialias = False):
        self.font_size = size
        
        #convert from string to color?
        self.fg = fg
        self.bg = bg
        
        self.font = font
        self.antialias = antialias
            
    def draw(self, surf = None):
        txt = scale_surf(font_to_bitmap( str(self.text) , \
        self.font_size , self.fg, self.bg, self.font, \
        self.antialias), self.get_scale())
        
        txt.set_colorkey(self.bg)
        
        if surf == None:
            self.get_screen().blit(txt, (self.x,self.y))

class TextBox(baseobjects.AllBase):
    def __init__(self, text, topleft, max_words = 5, decorations = None):
    
        self.decorations = decorations #dict of 'topleft', etc and images
        self.topleft = topleft
        self.text = text
        self.words_per_line = max_words
    
    def reflow(self, wpl):
        self.words_per_line = wpl
        
    def draw(self):
        wo = self.get_worldoffset()
        scale = self.get_scale()
        
        cx = 0 
        cy = 0
        wc = 0
        txt_size = self.font_size
        txt = self.text.split()
        
        for i in txt:  
            a = font_to_bitmap(i+' ', txt_size,(0,0,0),(255,255,255))
            a = scale_surf(a, self.get_scale())
            location =  ((self.topleft[0]* scale) + cx + wo[0], (self.topleft[1]* scale) + cy + wo[1])
            self.get_screen().blit(a, location)
            
            if wc < self.words_per_line:
                cx = cx+ a.get_width()
                wc +=1
            else:
                wc=0
                cx = 0
                cy = cy+a.get_height()

                
if __name__ == "__main__":
    
    import os, sys

    import pygame
    from pygame.locals import *
    from baseobjects import *

    pygame.init()

    #res = (480, 400)
    res = (800, 640)
    #res = (1440, 900)
    scale = 2
    game = Game()

    display = Game.init_display(game, res)
    screen = display[1]
    display = display[0]
    AllBase.set_scale(scale)
    display = pygame.display
    screen = pygame.display.set_mode(res)
    
    clock = pygame.time.Clock()
    
    ##NEW TEST CLASS
    
    fontsize = 20
    txt = 'Test text'
    scale = baseobjects.ObjectBase.get_scale()
    testtext = SimpleText( 10, 10, fontsize, txt )
    #print 'text:', 'Test text'
    #print 'font size:', fontsize
    #print 'scale:',  scale
    #
    #print 'rendered size?', fontsize * scale
    #
    #h = fontsize * scale
    #w = len(txt) * (fontsize * scale)
    #
    #print 'height:', h
    #print 'width:', w
    #
    #print 'actual rendered sizes...'
    #print testtext.get_text_surface_size()
    #exit()
    
    while True:
        game.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    exit()
            
                elif event.dict['key'] == K_x:
                        scale+=1
                elif event.dict['key'] ==  K_z:
                        scale-=1
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pass
                
            elif event.type == pygame.MOUSEBUTTONUP:
                pass
                
            elif event.type == pygame.MOUSEMOTION:
                pass
        
        AllBase.set_scale(scale)
        wo = AllBase.get_worldoffset()
        screen.fill((255,255,255))
        
        testtext.update()
        
        display.update()
