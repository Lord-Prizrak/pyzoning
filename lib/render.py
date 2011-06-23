# -*- coding: utf-8 -*-

class Render:
    """ Класс управления отрисовкой.
    Отрисовка начинается с 0 эл-та, т.е. 0 эл-т самый нижний, остальные поверх него. """
    sprites = {}

    def __init__(self, screen):
        """ Инициализация """
        self.screen = screen
        pass


    def add_obj(self, obj, lvl=5):
        """ Добавляем объект """
        if not lvl in sprites:
            sprites[lvl] = []
        sprites[lvl].append( {'surf':obj} )


    def add_surf(self, surf, point, lvl=5):
        """ Добавляем поверхность """
        if not lvl in sprites:
            sprites[lvl] = []
        sprites[lvl].append( {'surf':obj, 'point':point} )


    def render(self, surface):
        """ Отрисовываем """
        sprites.sort()
        blit = surface.blit
        for level in sprites:
            for sprite in level:
                if "point" in sprite:
                    blit( sprite["surf"], sprite["point"] )
                else:
                    surf = sprite["surf"].draw()
                    blit( surf, sprite["point"] )
