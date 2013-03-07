# -*- coding: utf-8 -*-
""" Класс для обновления объектов через указанный интервал. """

import pygame

# Интревал с которым происходит вызов апдейтера
# Интервал указывается в милисекундах!
interval = 30

list_o = {} # объекты для обновления (вызывается метод .update объекта)
list_f = {} # функции вызываемые с опред. интервалом.

def setinterval(newinterval):
    global interval
    if newinterval:
        interval = newinterval

        if newinterval != interval:
            pygame.time.set_timer(pygame.USEREVENT, interval)

    return interval


def add_obj(obj, interval):
    """ Добавление объекта """
    list_o[obj] = [interval, interval]


def add_func(func, interval):
    """ Добавление функции """
    list_f[func] = [interval, interval]


def rem_obj(obj, interval):
    """ Удаление объекта """
    list_o.remove(obj)


def rem_func(func, interval):
    """ Удаление функции """
    list_f.remove(func)


def tick():
    """ Обновление """
    ## FIX: Здесь простор для оптимизации!
    ## TODO: переписать как генератор.

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


# Инициализируемся
pygame.time.set_timer(pygame.USEREVENT, interval)
