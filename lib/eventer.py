# -*- coding: utf-8 -*-
""" Модуль для обработки событий """

import pygame


list_event = {}


def add(event, func):
    """ Добавление функции """
    if not event in list_event:
        list_event[event] = []

    list_event[event].append(func)


def remove(event, func):
    """ Удаление функции """
    list_event[event].remove(func)


def procevent(event):
    for func in list_event[event.type]:
        func(event)


def process(events):
    """ Обработка событий. """
    for event in events:
        if event.type in list_event:
            procevent(event)
