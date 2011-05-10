# -*- coding: utf-8 -*-

from globals import *

class Game:
    abort = False

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_icon(load_image('icon.png'))
        pygame.display.set_caption("Зонирование: Начало.")
        background = pygame.Surface(self.screen.get_size())
        background = background.convert()
        background.fill((0, 0, 0))
        self.screen.blit(background, (0, 0))
        pygame.display.flip()
        
        pygame.clock = pygame.time.Clock()


    def _checkinput(self):
        for event in pygame.event.get():
            if (event.type == pygame.QUIT) or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.abort = True
            else:
                pass


    def start(self):
        while not self.abort:
            pygame.clock.tick( 60 )
            self._checkinput()
