# -*- coding: utf-8 -*-
from globals import *

class Game:
    map = ""
    state = SCR_RAW
    abort = False

    def __init__(self):
        pygame.init()
        #pygame.display.set_icon(load_image('icon.png'))
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        background = pygame.Surface(self.screen.get_size())
        background = background.convert()
        background.fill((0, 0, 0))
        self.screen.blit(background, (0, 0))
        pygame.display.flip()
        pygame.display.set_caption("Зонирование: Начало.")

    def _loop_input(self):
        for event in pygame.event.get():
            if (event.type == pygame.QUIT) or 
		(event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                sys.exit()
            else:
                pass

    def startMainLoop(self):
        while not self.abort:
            self._loop_input()

