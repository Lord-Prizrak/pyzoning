# -*- coding: utf-8 -*-

import pygame

MainUpdater = None

def get_updater():
    global MainUpdater
    if MainUpdater == None:
        MainUpdater = Updater()
    return MainUpdater


class Updater(object):
    """ Класс для обновления объектов через указанный интервал. """

    list_o = {}
    list_f = {}
    
    def __init__(self, interval=100):
        """ Инициализация """
        pygame.time.set_timer(pygame.USEREVENT, interval)
        self.interval = interval


    def add_obj(self, obj, interval):
        """ Добавление объекта """
        list_o[obj] = [interval, interval]


    def add_func(self, func, interval):
        """ Добавление функции """
        list_func[func] = [interval, interval]


    def rem_obj(self, obj, interval):
        """ Удаление объекта """
        list_o.remove(obj)


    def rem_func(self, func, interval):
        """ Удаление функции """
        list_func.remove(func)


    def tick(self):
        """ Обновление """
        interval = self.interval
        for obj in list_o:
            if list_o[obj][1] <= 0:
                list_o[obj][1] = list_o[obj][0]
                obj.tick()
            else:
                list_o[obj][1] -= interval

        for func in list_f:
            if list_f[func][1] <= 0:
                list_f[func][1] = list_f[func][0]
                func()
            else:
                list_f[func][1] -= interval
