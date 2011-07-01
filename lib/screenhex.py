# -*- coding: utf-8 -*-

import random
import pygame
import pygame.gfxdraw as gfx
import hex

C_BLACK = (0,0,0)
C_FILL = (195,195,195)
C_SELECT = (165,165,165)
C_WHITE = (255,255,255)

class SCRHex:
    """ Класс интерфейса гексагонального поля. """
    hex_col = 6
    hex_row = 5
    hex_size = 80
    hex_dist = 40
    hex_now = (0,0)
    solid = None
    select = None
    hex2 = (0,0)
    selected = []
    sel_planet = None
    
    h1 = (-1,-1)

    def __init__(self, surface):
        """ Инициализация. """
        self.surface = surface
        self.surface.set_colorkey( C_BLACK, pygame.RLEACCEL )
        self.rect = self.surface.get_rect()

        self.area = hex.Hex(self.hex_size, self.hex_dist)        

        # Закрашенный гекс подсветки.
        self.solid = pygame.Surface( (self.area.hex_size+1, self.area.oo_rad*2+1) )
        self.solid_rect = self.solid.get_rect()
        self.solid.set_colorkey( C_BLACK, pygame.RLEACCEL )
        self.solid.set_alpha(200, pygame.RLEACCEL)
        points = self.area.polygon( (0,0) )
        gfx.filled_polygon(self.solid, points, C_FILL)
        gfx.aapolygon(self.solid, points, C_WHITE)

        # Выбранный гекс.
        self.select = pygame.Surface( (self.area.hex_size+1, self.area.oo_rad*2+1) )
        self.select_rect = self.select.get_rect()
        self.select.set_colorkey( C_BLACK, pygame.RLEACCEL )
        self.select.set_alpha(150, pygame.RLEACCEL)
        points = self.area.polygon( (0,0) )
        gfx.filled_polygon(self.select, points, C_SELECT)
        gfx.aapolygon(self.select, points, C_WHITE)

        # отрисовка задника
        font = pygame.font.Font(None, 20)
        for i in xrange(self.hex_col):
            for j in xrange(self.hex_row):
                x, y = self.area.center( (i,j) )
                points = self.area.polygon( (i,j) )
                gfx.aapolygon(surface, points, C_WHITE)
                pygame.draw.line(surface, C_WHITE, (x,y), (x,y), 1)#центральная точка
                text = font.render(str(i)+":"+str(j), 1, C_WHITE)
                surface.blit(text, (x,y))
                pygame.draw.circle(surface, C_WHITE, (x,y), int(self.area.oo_rad+15), 1)


    def draw(self, surf = None):
        """ Отрисовка экрана с гексополем. 
        Может приянть поверхность на которй будет рисовать. 
        Возвращает переданную поверхность или None. """
        if surf == None:
            surf_blit = self.surface.blit
        else:
            surf_blit = surf.blit
            
        selected = self.select
        sel_rect = self.select_rect 

        for hex in self.selected:
            xy = self.area.center(hex)
            sel_rect.center = xy
            surf_blit( selected, sel_rect )

        surf_blit( self.solid, self.solid_rect )
        
        planets = self.planets.values()
        for planet in planets:
            planet.update()
            surf_blit( planet.image, planet.rect )

        return surf


    def input(self, event):
        """ Обработка событий. """
        hex, hec_c = 0, 0
        if event.type == pygame.MOUSEMOTION:
            point = event.pos
            hex = self.area.index(point)

            if hex == (-1,-1):
                self.solid_rect.center = (-100,-100)
            else:
                xy = self.area.center(hex)
                self.solid_rect.center = xy

            ## TODO: Может этот код всё-же лучше?
            ## m_rect = pygame.Rect(point, (1,1))
            ## cr = m_rect.colliderect
            ## pls = self.planets.values()
            ## for pl in pls:
                ## pl.select = False
                ## if cr(pl.rect):
                    ## pl.select = True

            hex_c = self.area.index_circle(point, 30)
            if self.area.inhex_circle(point, hex_c, 30):
                pos = self.area.nearestpoint(point, hex)
                if pos in self.planets:
                    self.planets[pos].select = True
                    self.sel_planet = self.planets[pos]
            else:
                if self.sel_planet is not None:
                    self.sel_planet.select = False


        elif event.type == pygame.MOUSEBUTTONUP:
            point = event.pos
            hex = self.area.index(point)
            ## if hex == (-1,-1):
                ## return
            ## if hex in self.selected:
                ## self.selected.remove(hex)
            ## else:
                ## self.selected.append(hex)

            if self.h1 == (-1,-1):
                self.h1 = hex
            else:
                path = self.area.path_no_barriers(self.h1,hex)
                self.h1 = (-1,-1)
                self.selected = path


    def setplanet(self, planets):
        self.planets = planets
