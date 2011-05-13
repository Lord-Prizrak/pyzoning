# -*- coding: utf-8 -*-

from globals import *
import screenhex

class Game:
    """ основной класс игры. """
    
    abort = False
    SCREEN_SIZE = (800,600)

    def __init__(self):
        """ Инициализация. """
        pygame.init()
        self.screen = pygame.display.set_mode(self.SCREEN_SIZE)
        pygame.display.set_icon(load_image('icon.png'))
        pygame.display.set_caption("Зонирование: Начало.")

        self.bgimage = load_image("background.png")
        self.background = pygame.transform.scale(self.bgimage, self.SCREEN_SIZE)
        self.screen.blit(self.background, (0, 0))

        surf = pygame.Surface(self.screen.get_size())
        self.scrh = screenhex.SCRHex( surf )
        pygame.clock = pygame.time.Clock()

        pygame.display.flip()


    def start(self):
        """ Основной цикл. """
        while not self.abort:
            pygame.clock.tick( 60 )
            self.checkevent()
            self.redraw()


    def checkevent(self):
        """ Проверка событий. """
        for event in pygame.event.get():
            #print event
            if (event.type == pygame.QUIT) or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.abort = True
            else:
                pass


    def redraw(self):
        """ Перерисовка экрана. """
        self.screen.blit( self.background, (0,0) )
        self.screen.blit( self.scrh.draw(), (0, 0) )
