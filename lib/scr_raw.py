# -*- coding: utf-8 -*-

import globals

class SCR_Hex:
    state = SCR_KOS
    abort = False

    def __init__(self, surface, size):
        self.m_surf = surface

        background = pygame.Surface(self.screen.get_size())
        background = background.convert()
        background.fill((0, 0, 0))
        self.screen.blit(background, (0, 0))
        pygame.display.flip()


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
