# -*- coding: utf-8 -*-

from globals import *

class Game:
    state = SCR_HEX
    abort = False

    def load_image(self,file):
        "loads an image, prepares it for play"
        file = os.path.join('data', file)
        try:
            surface = pygame.image.load(file)
        except pygame.error:
            raise SystemExit, 'Could not load image "%s" %s'%(file, pygame.get_error())
        return surface.convert()


    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_icon(self.load_image('icon.png'))
        pygame.display.set_caption("Зонирование: Начало.")
        background = pygame.Surface(self.screen.get_size())
        background = background.convert()
        background.fill((0, 0, 0))
        self.screen.blit(background, (0, 0))
        pygame.display.flip()


    def _loop_input(self):
        for event in pygame.event.get():
            if (event.type == pygame.QUIT) or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                sys.exit()
            else:
                pass


    def start(self):
        while not self.abort:
            self._loop_input()
