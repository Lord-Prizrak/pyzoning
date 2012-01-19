# -*- coding: utf-8 -*-

from resources import *
import screenhex
import updater


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
