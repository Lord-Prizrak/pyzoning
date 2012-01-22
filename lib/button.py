# -*- coding: utf-8 -*-

import os
import pygame

BTN_STATE = { 'normal' : 0, 'active' : 1, 'pressed' : 2 }

class ButtonBox:
    """ Бокс для нескольких кнопок """
    items = []

    def add(self, item):
        """ Добавлеяет кнопку в бокс """
        self.items.append(item)


    def draw(self):
        """ Отрисовка """
        pass


class Button:
    """ Класс кнопки """
    pict = None
    rect = None

    def __init__(self, name):
        """ Создание кнопки """
        self.rect = self.pict.get_rect()


    def setstate(self, state):
        """ Установка состояния кнопки """
        if state in BTN_STATE:
            self.state = BTN_STATE[state]
