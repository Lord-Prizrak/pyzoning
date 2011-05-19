# -*- coding: utf-8 -*-

import os
import pygame

DATA_DIR = "Data"

def check_res():
    files = os.listdir('.')
    resources = files
    return resources

def load_image(file):
    """ Загрузка изображений. Возвращает surface """
    file = os.path.join(DATA_DIR, file)
    try:
        surface = pygame.image.load(file)
    except pygame.error:
        raise SystemExit, "Could not load image '%s' %s"%(file, pygame.get_error())
    return surface.convert()
