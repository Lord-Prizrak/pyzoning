# -*- coding: utf-8 -*-

import pygame
import random
import resources as res
import screenhex
import updater
import eventer
from planet import Planet

## FIXME: Скорость работы крайне низкая! Необходима оптимизация всего!
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

        ## Готовим окошко
        pygame.init()
        screen = pygame.display.set_mode(self.SCREEN_SIZE)
        pygame.display.set_caption("Зонирование: Начало.")
        ##pygame.display.set_icon( res.Image('icon.png') )
        self.bgimage = res.Image("background.png")
        screen.blit( pygame.transform.scale(self.bgimage, self.SCREEN_SIZE), (0,0) )

        ## TODO: Поправить для множества экранов
        surf = screen.subsurface( screen.get_rect() )
        self.scr_h = screenhex.SCRHex( surf )
        self.background = screen.copy()
        pygame.display.flip()
        self.screen = screen

        self.font = pygame.font.Font(None, 20)

        self.create_planet()


    def create_planet(self):
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

        # for i in xrange(hex_col):
        #     for j in xrange(hex_row):
        #         xys = polygon( (i,j) )
        #         for p, xy in enumerate(xys):
        #             koord = (i,j),p
        #             planet = Planet()
        #             planet.set_pos( xy )
        #             planet.koord = koord
        #             planets[koord] = planet

        self.scr_h.setplanet(planets)
        self.planets = planets


    def start(self):
        """ Основной цикл. """

        # eventer.add(pygame.USEREVENT, updater.tick)
        eventer.add(pygame.QUIT, self.quit)
        eventer.add(pygame.KEYDOWN, self.quit)
        eventer.add(pygame.KEYDOWN, self.screenshot)
        eventer.add(pygame.MOUSEMOTION, self.scr_h.input)
        # eventer.add(pygame.MOUSEBUTTONUP, self.scr_h.input)
        # eventer.add(pygame.MOUSEBUTTONDOWN, self.scr_h.input)

        updater.add_func(self.redraw, 100)

        clock = pygame.time.Clock()
        process = eventer.process
        getevent = pygame.event.get
        updatertick = updater.tick

        while not self.abort:
            ms = clock.tick( 100 ) # итераций в секунду

            updatertick(ms)

            events = getevent()
            if len(events) > 0:
                process(events)

            # print "--------------------------------------------------------------------------------"


    def redraw(self):
        """ Перерисовка экрана. """
        self.screen.blit( self.background, (0,0) )
        self.scr_h.draw()

        pygame.display.flip()


    def quit(self, event):
        ## FIXME: Некрасиво!
        if (event.type == pygame.QUIT) or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            print "MSG: QUIT"
            self.abort = True


    def screenshot(self, event):
        """ Создаёт снимок экрана """
        if event.key != pygame.K_PRINT:
            return

        self.redraw()
        pygame.image.save(self.screen, "screenshot.png")
        print "MSG: SAVE"
