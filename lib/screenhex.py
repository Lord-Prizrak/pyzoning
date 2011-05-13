# -*- coding: utf-8 -*-

import globals
import pygame
import hex

class SCRHex:
    """ Класс интерфейса гексагонального поля. """
    hex_col = 5
    hex_row = 5
    hex_size = 60
    hex_dist = 20
    
    def __init__(self, surface):
        """ Инициализация. """
        self.surface = surface
        self.rect = self.surface.get_rect()
        self.area = hex.Hex(hex_size, hex_dist)


    def draw(self):
        """ Отрисовка гесополя. Возвращает sarface. """
        for i in range(hex_col):
            for j in range(hex_row):
                x, y = pole.center( (i,j) )
                points = pole.polygon( (i,j) )
                pygame.draw.polygon(surfmain, (255,255,255), points, 1)
                pygame.draw.line(surfmain, (255,255,255), (x,y), (x,y), 1)#центральная точка
                text = font.render(str(i)+":"+str(j), 1, (250, 250, 250))
                surfmain.blit(text, (x,y))

        return self.surface
