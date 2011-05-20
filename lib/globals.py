# -*- coding: utf-8 -*-

import os
import pygame

DATA_DIR = "Data"
RES = object()

def loadres():
    if __RES == Null:
        __RES = Resources()
    return __RES


def load_image(file):
    """ Загрузка изображений. Возвращает surface """
    file = os.path.join(DATA_DIR, file)
    try:
        surface = pygame.image.load(file)
    except pygame.error:
        raise SystemExit, "Could not load image '%s' %s"%(file, pygame.get_error())
    return surface.convert()


class Resources:
    def __init__(self):
        files = os.listdir('.')
        self.resources = files
        return resources
