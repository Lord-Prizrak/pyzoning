# -*- coding: utf-8 -*-

import random
import pygame
import pygame.gfxdraw as gfx
import hex

## FIXME: Внимательно пересмотреть ВСЁ здесь.

C_BLACK = (0,0,0)
C_FILL = (195,195,195)
C_SELECT = (165,165,165)
C_WHITE = (255,255,255)

class SCRHex:
    """ Класс интерфейса гексагонального поля. """
    hex_col = 6
    hex_row = 5
    hex_size = 70
    hex_dist = 50
    hex_now = (0,0)
    solid = None
    select = None
    hex2 = (0,0)
    selected = []
    sel_planet = None

    h1 = (-1,-1)

    def __init__(self, surface):
        """ Инициализация. 
        surface - поверхность на которой будем рисовать """
        self.surface = surface
        self.surface.set_colorkey( C_BLACK, pygame.RLEACCEL )
        self.rect = self.surface.get_rect()

        self.area = hex.Hex(self.hex_size, self.hex_dist)        

        # Закрашенный гекс подсветки.
        self.solid = pygame.Surface( (self.area.S.size[0]+1, self.area.S.size[1]+1) )
        self.solid.set_colorkey( C_BLACK, pygame.RLEACCEL )
        self.solid.set_alpha(200, pygame.RLEACCEL)
        self.solid_rect = self.solid.get_rect()
        self.solid_rect.center = (-100,-100)
        points = self.area.polygon( (0,0) )
        gfx.filled_polygon(self.solid, points, C_FILL)
        gfx.aapolygon(self.solid, points, C_WHITE)
        # Выбранный гекс.
        self.select = self.solid.copy()
        self.select_rect = self.select.get_rect()
        points = self.area.polygon( (0,0) )
        gfx.filled_polygon(self.select, points, C_SELECT)
        gfx.aapolygon(self.select, points, C_WHITE)

        # отрисовка задника
        line = pygame.draw.line
        font = pygame.font.Font(None, 20)
        for i in xrange(self.hex_col):
            for j in xrange(self.hex_row):
                x, y = self.area.center( (i,j) )
                points = self.area.polygon( (i,j) )
                gfx.aapolygon(surface, points, C_WHITE)
                line(surface, C_WHITE, (x,y), (x,y), 1)#центральная точка
                text = font.render(str(i)+":"+str(j), 1, C_WHITE)
                surface.blit(text, (x,y))


    def draw(self, surf = None):
        """ Отрисовка экрана с гексополем.
        surf -  поверхность на которой нужно рисовать,
        Возвращает переданную поверхность или None. """
        if surf is None:
            surf_blit = self.surface.blit
        else:
            surf_blit = surf.blit

        ## Выделенные гексы. 
        selected = self.select
        sel_rect = self.select_rect
        for hex in self.selected: 
            xy = self.area.center(hex)
            sel_rect.center = xy
            surf_blit( selected, sel_rect )

        ## подсвеченный гекс
        surf_blit( self.solid, self.solid_rect )

        ## Рисуем планеты
        planets = self.planets.values()
        for planet in planets:
            planet.update()
            surf_blit( planet.image, planet.rect )

        return surf


    def input(self, event):
        """ Обработка событий. """
        point = event.pos
        hex = self.area.index(point)
        if event.type == pygame.MOUSEMOTION:
            # Гекс подсветки
            # if hex == (-1,-1):
            #     self.solid_rect.center = (-100,-100)
            # else:
            #     xy = self.area.center(hex)
            #     self.solid_rect.center = xy

            ## Ближайшая планета
            pos = self.area.nearestpoint(point, hex)
            ## INFO: Тут константа!
            if pos[0] and (pos[:2] in self.planets) and (pos[2] < 15):
                if self.sel_planet is not None:
                    self.sel_planet.select = False
                self.sel_planet = self.planets[pos[:2]]
                self.sel_planet.select = True

            elif self.sel_planet is not None:
                self.sel_planet.select = False
                self.sel_planet = None

        # elif event.type == pygame.MOUSEBUTTONUP:
        #     # Выделенные гексы
        #     if hex == (-1,-1):
        #         return
        #     if hex in self.selected:
        #         self.selected.remove(hex)
        #     else:
        #         self.selected.append(hex)

        #     # Поиск пути
        #     if self.h1 == (-1,-1):
        #         self.h1 = hex
        #     else:
        #         path = self.area.path_no_barriers(self.h1,hex)
        #         self.h1 = (-1,-1)
        #         self.selected = path


    def setplanet(self, planets):
        self.planets = planets
