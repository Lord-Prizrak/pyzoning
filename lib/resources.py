# -*- coding: utf-8 -*-

import os
import pygame
import random

DATA_DIR = "data"
RES = None

def loadres():
    global RES
    if RES == None:
        RES = Resources()
    return RES


class Resources:
    """ Класс для работы с ресурсами """

    resources = {}

    def __init__(self):
        """ Инициализируем """
        random.seed()
        self.scandata()


    def rndImage(self, restype=None):
        """ Выдаём случайное изображение """
        if restype == None:
            pas = "data"
        else:
            pas = os.path.join("data", restype)

        name = random.choice( self.resources[pas].keys() )
        return self.Image(name, restype)


    def Image(self, name, restype=None):
        """ Выдаём указанное изображение """
        if restype == None:
            restype = "data"
        else:
            restype = os.path.join("data", restype)

        surface = pygame.image.load( os.path.join(restype, name) )
        return surface.convert()


    def scandata(self):
        """ Сканируем директорию с ресурсами """
        dirs = [DATA_DIR]
        for dirname in dirs:
            files = os.listdir(dirname)
            self.resources[dirname] = {}

            for name in files:
                if os.path.isfile(os.path.join(dirname,name)):
                    self.resources[dirname][name] = os.path.join(dirname,name)

                if os.path.isdir(os.path.join(dirname,name)):
                    dirs.append(os.path.join(dirname,name))


#def load_image(file):
    #""" Загрузка изображений. Возвращает surface """
    #file = os.path.join(DATA_DIR, file)
    #try:
        #surface = pygame.image.load(file)
    #except pygame.error:
        #raise SystemExit, "Could not load image '%s' %s"%(file, pygame.get_error())
    #return surface.convert()
