# -*- coding: utf-8 -*-

import globals

class SCR_Hex:
    def __init__(self, surface, size):
        self.m_surf = surface
        background = pygame.Surface(self.screen.get_size())
        background = background.convert()
        background.fill((0, 0, 0))
        self.screen.blit(background, (0, 0))
