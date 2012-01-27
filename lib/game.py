# -*- coding: utf-8 -*-

import pygame
import random
from resources import get_res
import screenhex
import updater
from planet import Planet

## FIXME: Проверить ещё разок здесь всё.

class Game:
    """ основной класс игры. """

    abort = False
    SCREEN_SIZE = (800,600)

    def __init__(self):
        """ Инициализация игры, экрана.
        В классы передаётся "подповерхность" основной поверхности-экрана. 
        Классы на ней отрисовывают всё что им нужно. В конце инициализации 
        поверхность копирутеся в background - "эталонную" поверхность, которой 
        будет затираться основная при каждом кадре. """

        ## Загрузчик ресурсов
        resc = get_res()

        ## Готовим окошко
        pygame.init()
        screen = pygame.display.set_mode(self.SCREEN_SIZE)
        pygame.display.set_caption("Зонирование: Начало.")
        ##pygame.display.set_icon( resc.Image('icon.png') )
        self.bgimage = resc.Image("background.png")
        screen.blit( pygame.transform.scale(self.bgimage, self.SCREEN_SIZE), (0,0) )
        surf = screen.subsurface( screen.get_rect() )
        self.scr_h = screenhex.SCRHex( surf )
        self.background = screen.copy()
        pygame.display.flip()
        self.screen = screen

        self.font = pygame.font.Font(None, 20)

        self.update = updater.Updater(20)

        self.draw_count = 0
        self.update.add_func(self.redraw, 100)
        self.update.add_func(self.getfps, 1000) # А нам чаще и не нужно!
        self.getfps()

        ## Создаём планеты
        planets = {}
        hex_col = self.scr_h.hex_col
        hex_row = self.scr_h.hex_row
        polygon = self.scr_h.area.polygon
        for x in xrange(10):
            i = random.randint(0,hex_col-1)
            j = random.randint(0,hex_row-1)
            p = random.randint(0,5)
            xy = polygon( (i,j) )[p]
            koord = (i,j),p

            planet = Planet()
            planet.set_pos( xy )
            planet.koord = koord
            planets[koord] = planet
        
        ## for i in xrange(hex_col):
            ## for j in xrange(hex_row):
                ## xys = polygon( (i,j) )
                ## for p, xy in enumerate(xys):
                    ## koord = (i,j),p
                    ## planet = Planet()
                    ## planet.set_pos( xy )
                    ## planet.koord = koord
                    ## planets[koord] = planet

        self.scr_h.setplanet(planets)
        self.planets = planets


    def start(self):
        """ Основной цикл. """
        while not self.abort:
            self.checkevent()


    def checkevent(self):
        """ Проверка событий. """
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.USEREVENT:
                self.update.tick()
            elif event.type == pygame.MOUSEBUTTONUP:
                self.scr_h.input(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.scr_h.input(event)
            elif event.type == pygame.MOUSEMOTION:
                self.scr_h.input(event)
            elif (event.type == pygame.KEYDOWN) and (event.key == pygame.K_PRINT):
                self.redraw()
                pygame.image.save(self.screen, "screenshot.png")
                print "MSG: SAVE"
            elif (event.type == pygame.QUIT) or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                print "MSG: QUIT"
                self.abort = True


    def redraw(self):
        """ Перерисовка экрана. """
        self.screen.blit( self.background, (0,0) )
        self.scr_h.draw()

        ## FPS
        ## TODO: Переделать нужно в будующем
        self.screen.blit( self.fpsSurf, (10,10) )
        self.draw_count += 1

        pygame.display.flip()


    def getfps(self):
        self.fpsSurf = self.font.render( str(self.draw_count), 1, (250, 250, 250) )
        self.draw_count = 0
