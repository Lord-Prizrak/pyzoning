# -*- coding: utf-8 -*-

import globals
import pygame
import hex
import pygame.gfxdraw as gfx

class SCRHex:
    """ Класс интерфейса гексагонального поля. """
    hex_col = 9
    hex_row = 8
    hex_size = 60
    hex_dist = 20
    hex_now = (0,0)
    solid = None
    hex2 = (0,0)

    def __init__(self, surface):
        """ Инициализация. """
        self.surface = surface
        self.surface.set_colorkey( (0,0,0), pygame.RLEACCEL )
        #self.rect = self.surface.get_rect()
        self.area = hex.Hex(self.hex_size, self.hex_dist)        

        self.solid = pygame.Surface( (self.area.hex_size+1, self.area.oo_rad*2+1) )
        self.solid_rect = self.solid.get_rect()
        self.solid.set_colorkey( (0,0,0), pygame.RLEACCEL )
        xy = self.area.center( (0,0) )
        points = hex.polygon( xy, self.hex_size-2 )
        gfx.filled_polygon(self.solid, points, (95,95,95))

        font = pygame.font.Font(None, 20)
        for i in xrange(self.hex_col):
            for j in xrange(self.hex_row):
                x, y = self.area.center( (i,j) )
                points = self.area.polygon( (i,j) )
                gfx.aapolygon(self.surface, points, (255,255,255))
                #pygame.draw.polygon(surfmain, (255,255,255), points, 1)
                pygame.draw.line(self.surface, (255,255,255), (x,y), (x,y), 1)#центральная точка
                text = font.render(str(i)+":"+str(j), 1, (250, 250, 250))
                self.surface.blit(text, (x,y))


    def draw(self):
        """ Отрисовка гесополя. Возвращает sarface. """
        ret_surf = self.surface.copy()
        ret_surf.blit( self.solid, self.solid_rect )
        return ret_surf


    def input(self, event):
        if event.type == pygame.MOUSEMOTION:
            point = event.pos
            hex = self.area.index(point)
            if hex == (-1,-1):
                self.solid_rect.center = (-100,-100)
            else:
                xy = self.area.center(hex)
                self.solid_rect.center = xy
