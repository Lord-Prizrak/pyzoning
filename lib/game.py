# -*- coding: utf-8 -*-

from resources import *
import screenhex
import updater

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
        resc = loadres()

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

        self.clock = pygame.time.Clock()
        self.update = updater.Updater(50)

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
            self.clock.tick( 60 )
            self.checkevent()
            self.redraw()
            pygame.display.flip()


    def checkevent(self):
        """ Проверка событий. """
        for event in pygame.event.get():
            #print event
            if (event.type == pygame.QUIT) or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.abort = True
            elif event.type == pygame.USEREVENT:
                self.update.update()
            elif event.type == pygame.MOUSEBUTTONUP:
                self.scr_h.input(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.scr_h.input(event)
            elif event.type == pygame.MOUSEMOTION:
                self.scr_h.input(event)
            elif (event.type == pygame.QUIT) or (event.type == pygame.KEYDOWN and event.key == pygame.K_PRINT):
                self.redraw()
                pygame.image.save(self.screen, "screeshot.png")
                print "Save"


    def redraw(self):
        """ Перерисовка экрана. """
        self.screen.blit( self.background, (0,0) )
        self.scr_h.draw()

        ## FPS
        font = pygame.font.Font(None, 20)
        text = font.render( str(self.clock.get_fps())+" "+str(self.clock.get_time()), 1, (250, 250, 250) )
        self.screen.blit(text, (10,self.SCREEN_SIZE[1]-20))


class Planet:
    """ Клас планеты. """
    
    select = False
    
    def __init__(self):
        """ Инициализируемся. """
        resc = loadres()
        image = resc.rndImage("planet")
        self.image = pygame.transform.scale(image, (30,30) )
        self.image.set_colorkey( (0,0,0), pygame.RLEACCEL )
        self.rect = self.image.get_rect()
        
    def set_pos(self, pos):
        """ Устанавливаем позицию. В координатах основной поверхности! """
        self.rect.center = pos
        
    def update(self):
        """ Обновляем объект. """
        if self.select:
            if self.image.get_alpha() is None:
                self.image.set_alpha(100)
        else:
            if self.image.get_alpha() is not None:
                self.image.set_alpha()


class Siur:
    """ Класс сиура. Т.е. энерго-объединения планет в блоки по шесть. """
    def __init__(self):
        pass
