# -*- coding: utf-8 -*-

import os
import pygame
import random

DATA_DIR = "data"
resources = {}
loaded_im = {}

def rndImage(restype=None):
    """ Выдаём случайное изображение """
    if restype == None:
        pas = "data"
    else:
        pas = os.path.join("data", restype)

    random.seed()
    name = random.choice( resources[pas].keys() )
    return Image(name, restype)


def Image(name, restype=None):
    """ Выдаём указанное изображение """
    if restype == None:
        restype = "data"
    else:
        restype = os.path.join("data", restype)

    key = (restype, name)
    try:
        surface = loaded_im[key]
    except KeyError:
        surface = pygame.image.load( os.path.join(restype, name) )
        loaded_im[key] = surface

    return surface.convert()


def scandata(data_dir=None):
    """ Сканирует директорию с ресурсами """
    if data_dir:
        dirs = [data_dir]
    else:
        dirs = [DATA_DIR]
    
    for dirname in dirs:
        files = os.listdir(dirname)
        resources[dirname] = {}

        for name in files:
            if os.path.isfile(os.path.join(dirname,name)):
                resources[dirname][name] = os.path.join(dirname,name)

            if os.path.isdir(os.path.join(dirname,name)):
                dirs.append(os.path.join(dirname,name))


scandata()


#def load_image(file):
    #""" Загрузка изображений. Возвращает surface """
    #file = os.path.join(DATA_DIR, file)
    #try:
        #surface = pygame.image.load(file)
    #except pygame.error:
        #raise SystemExit, "Could not load image '%s' %s"%(file, pygame.get_error())
    #return surface.convert()
