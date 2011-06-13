# -*- coding: utf-8 -*-

MainUpdater = None


class Singleton(object):
  def __new__(cls, *args, **kw):
      if not hasattr(cls, '_instance'):
        orig = super(Singleton, cls)
        cls._instance = orig.__new__(cls, *args, **kw)
      return cls._instance


class Updater(object):
    """ Класс для обновления объектов через указанный интервал. """

    list_o = {}
    list_f = {}
    
    def __init__(self, interval=100, newupdater=False):
        """ Инициализация """
        global MainUpdater

        print "mainUpdater:", MainUpdater

        if newupdater:
            print "NEW"

        if MainUpdater == None:
            print "Created"
            MainUpdater = self
        else:
            print "Not created"
            return None


    def add_obj(self, obj, interval):
        """ Добавление объекта """
        list_o[obj] = [interval, interval]


    def add_func(self, func, interval):
        """ Добавление функции """
        list_func[func] = [interval, interval]


    def tick(self):
        """ Обновление """
        for obj in list_o:
            if list_o[obj][1] == 0:
                list_o[obj][1] = list_o[obj][0]
                obj.tick()
            else:
                list_o[obj][1] -= 1

        for func in list_f:
            if list_f[func][1] == 0:
                list_f[func][1] = list_f[func][0]
                func()
            else:
                list_f[func][1] -= 1
