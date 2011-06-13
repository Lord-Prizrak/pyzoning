# -*- coding: utf-8 -*-

import pygame
import pygame.gfxdraw as gfx
import hex

C_BLACK = (0,0,0)
C_FILL = (95,95,95)
C_SELECT = (65,65,65)
C_WHITE = (255,255,255)

class SCRHex:
    """ Класс интерфейса гексагонального поля. """
    hex_col = 9
    hex_row = 8
    hex_size = 60
    hex_dist = 20
    hex_now = (0,0)
    solid = None
    select = None
    hex2 = (0,0)
    selected = []

    def __init__(self, surface):
        """ Инициализация. """
        self.surface = surface
        self.surface.set_colorkey( C_BLACK, pygame.RLEACCEL )
        self.rect = self.surface.get_rect()

        self.area = hex.Hex(self.hex_size, self.hex_dist)        

        # Закрашенный гекс подсветки. Надо сделать прозрачность
        self.solid = pygame.Surface( (self.area.hex_size+1, self.area.oo_rad*2+1) )
        self.solid_rect = self.solid.get_rect()
        self.solid.set_colorkey( C_BLACK, pygame.RLEACCEL )
        points = self.area.polygon( (0,0) )
        gfx.filled_polygon(self.solid, points, C_FILL)
        gfx.aapolygon(self.solid, points, C_WHITE)

        # Выбранный гекс. Надо сделать прозрачность
        self.select = pygame.Surface( (self.area.hex_size+1, self.area.oo_rad*2+1) )
        self.select_rect = self.select.get_rect()
        self.select.set_colorkey( C_BLACK, pygame.RLEACCEL )
        points = self.area.polygon( (0,0) )
        gfx.filled_polygon(self.select, points, C_SELECT)
        gfx.aapolygon(self.select, points, C_WHITE)

        # "Задняя" поверхность
        self.back_surf = surface.copy()

        # отрисовка сетки.
        font = pygame.font.Font(None, 20)
        for i in xrange(self.hex_col):
            for j in xrange(self.hex_row):
                x, y = self.area.center( (i,j) )
                points = self.area.polygon( (i,j) )
                gfx.aapolygon(self.surface, points, C_WHITE)
                pygame.draw.line(self.surface, C_WHITE, (x,y), (x,y), 1)#центральная точка
                text = font.render(str(i)+":"+str(j), 1, C_WHITE)
                self.surface.blit(text, (x,y))


    def draw(self):
        """ Отрисовка гесополя. Возвращает surface. """
        ret_surf = self.surface.copy()
        for hex in self.selected:
            xy = self.area.center(hex)
            self.select_rect.center = xy
            ret_surf.blit( self.select, self.select_rect )

        ret_surf.blit( self.solid, self.solid_rect )
        return ret_surf


    def input(self, event):
        """ Обработка событий. """
        if event.type == pygame.MOUSEMOTION:
            point = event.pos
            hex = self.area.index(point)
            if hex == (-1,-1):
                self.solid_rect.center = (-100,-100)
            else:
                xy = self.area.center(hex)
                self.solid_rect.center = xy

        elif event.type == pygame.MOUSEBUTTONUP:
            point = event.pos
            hex = self.area.index(point)
            if hex == (-1,-1):
                return
            if hex in self.selected:
                self.selected.remove(hex)
            else:
                self.selected.append(hex)
