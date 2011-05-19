# -*- coding: utf-8 -*-

import globals
import pygame
import hex
import pygame.gfxdraw

class SCRHex:
    """ Класс интерфейса гексагонального поля. """
    hex_col = 9
    hex_row = 8
    hex_size = 60
    hex_dist = 20
    
    def __init__(self, surface):
        """ Инициализация. """
        self.surface = surface
        self.rect = self.surface.get_rect()
        self.area = hex.Hex(self.hex_size, self.hex_dist)
        
        self.surface.set_colorkey( (0,0,0), pygame.RLEACCEL )

        font = pygame.font.Font(None, 20)
        for i in xrange(self.hex_col):
            for j in xrange(self.hex_row):
                x, y = self.area.center( (i,j) )
                points = self.area.polygon( (i,j) )
                pygame.gfxdraw.aapolygon(self.surface, points, (255,255,255))
                #pygame.draw.polygon(surfmain, (255,255,255), points, 1)
                pygame.draw.line(self.surface, (255,255,255), (x,y), (x,y), 1)#центральная точка
                text = font.render(str(i)+":"+str(j), 1, (250, 250, 250))
                self.surface.blit(text, (x,y))

    def draw(self):
        """ Отрисовка гесополя. Возвращает sarface. """
        
        return self.surface