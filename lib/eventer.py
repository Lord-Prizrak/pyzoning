# -*- coding: utf-8 -*-

import pygame

MainEventer = None

def get_eventer():
    global MainEventer
    if MainEventer == None:
        MainEventer = Eventer()
    return MainEventer


class Eventer(object):
    """ Объект занимающийся обработкой событий """
    list_event = {"ALL":[]}

    def add(self, event, func):
        """ Добавление функции """
        self.list_event[event] += [func]


    def remove(self, event, func):
        """ Удаление функции """
        self.list_event[event].remove(func)


    def event(self, event):
        if not(event in list_event):
            return

        for func in list_event[event]:
            func()
