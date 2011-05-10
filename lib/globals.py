# -*- coding: utf-8 -*-

import os
import sys
import random
import pygame
from pygame import locals

SCREEN_SIZE = (800,600)

DATA_DIR = "Data"

def load_image(file):
    """ Загрузка изображений. Возвращает surface """
    file = os.path.join(DATA_DIR, file)
    try:
        surface = pygame.image.load(file)
    except pygame.error:
        raise SystemExit, "Could not load image '%s' %s"%(file, pygame.get_error())
    return surface.convert()
