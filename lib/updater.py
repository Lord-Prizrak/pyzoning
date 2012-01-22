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
        self.list_o[obj] = [interval, interval]


    def add_func(self, func, interval):
        """ Добавление функции """
        self.list_f[func] = [interval, interval]


    def rem_obj(self, obj, interval):
        """ Удаление объекта """
        self.list_o.remove(obj)


    def rem_func(self, func, interval):
        """ Удаление функции """
        self.list_f.remove(func)


    def tick(self):
        """ Обновление """
        interval = self.interval
        list_o = self.list_o
        list_f = self.list_f

        for obj in list_o:
            if list_o[obj][1] <= 0:
                list_o[obj][1] = list_o[obj][0]
                obj.tick()
            list_o[obj][1] -= interval

        for func in list_f:
            if list_f[func][1] <= 0:
                list_f[func][1] = list_f[func][0]
                func()
            list_f[func][1] -= interval
