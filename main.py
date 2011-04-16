#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import glob
from random import randint, randrange

#~ import pygame
#~ from pygame.locals import *

from lib.globals import *
from lib.game import *

def main():
    g=Game()

    if not "--map" in sys.argv:
        g.map = "Data\Back For Revenge - Allied.h3m"
    else:
        i = 0
        for arg in sys.argv:
            if arg == '--map':
                g.map(str(sys.argv[i + 1]))
            i += 1
    g.startMainLoop()
    return 0

if __name__ == '__main__':
    main()
