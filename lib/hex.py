#!/usr/bin/env python
# -*- coding: utf-8 -*-

## Сей код получён путем тупого перевода кода на Ruby в код на Python.
## Внизу самом код ВРЕМЕННЫЙ чисто только для отладки, потом будет заменён
## на что-то более адекватное для демонстрации

from math import cos, pi, sqrt

CENTER  = 1
UP      = 2
DOWN    = 3
LEFT    = 4
RIGHT   = 5


class Hex:
    """ Класс для обслуживания поля из гексагональных ячеек. Ячейки могут
    быть не влотную друг к другу.
    i, j - номер гекса. столбец и строка. Гексы строятся со сдвигом строки
    (каждая нечетная строка сдвинута относительно четной на половину ширины)
    hex_size - расстояние между центрами противоположных граней - ширина гекса.
    vo_rad - радиус вписанного круга.
    oo_rad - радиус описанного круга.
    str_hgt - полтора self.oo_rad (высота строки состоящей из гексов).
    oo_rad2 - половина радиуса описанного круга.
    distation - расстояние между гексами по умолчанию = 0 """


    def __init__(self, size, dist=0):
        """ Инициализация. Принимает размер гекса по ширине size, 
        расстояние между гексами dist"""
        self.hex_size= size
        self.vo_rad  = self.hex_size / 2.
        self.oo_rad  = self.vo_rad / ( sqrt(3)/2 )
        self.oo_rad2 = self.oo_rad / 2.
        self.str_hgt = self.oo_rad + self.oo_rad2
        self.distation = dist


    def center(self, hex):
        """ Вычисляет координаты центрального пикселя. Принимает индекс гекса hex. """
        x = self.vo_rad+ hex[0]*self.hex_size +(self.vo_rad+self.distation/2)*(hex[1]%2) +self.distation*hex[0]
        y = self.oo_rad+ hex[1]*self.str_hgt +self.distation*hex[1]
        
        ## FIXME: Некрасивая конструкция в возврате.
        return  ( int(round(x)), int(round(y)) )


    def polygon(self, hex):
        """ Вычисляет координаты вершин гекса, учитывая размеры. Принимает индекс гекса hex."""
        ## INFO: Возвращает float числа, что не всегда хорошо.
        x, y = self.center(hex)
        path  = [[round(x), round(y - self.oo_rad)]]
        path += [[round(x + self.vo_rad), round(y - self.oo_rad2)]]
        path += [[round(x + self.vo_rad), round(y + self.oo_rad2)]]
        path += [[round(x), round(y + self.oo_rad)]]
        path += [[round(x - self.vo_rad), round(y + self.oo_rad2)]]
        path += [[round(x - self.vo_rad), round(y - self.oo_rad2)]]
        
        return path


    def index(self, point):
        """ Вычисляет индекс гекса по координатам точки point.
        !!! Нужно переписать более адекватно !!! """

        ## INFO: От этих условий надо как-то избавиться. Проблема в том, что если
        ##  -1 < i или j < 0, то они становятся 0. Из чего возниакет несколько не очень удобных ситуаций.
        ##  Например когда точка падает рядом с левым нижним углом, обсчёт здесь его берёт как ряд ниже,
        ##  но он сдвинут на пол гекса правее, и номер i становится -0.12, при отбрасывании
        ##  дробной части он становится 0, а не -1
        ## j = int( point[1] / (self.str_hgt  + self.distation) )
        ## if (j <= 0.) : j -= 1
        ## i = int( point[0] / (self.vo_rad*2 + self.distation) -(0.5*(int(j)%2)) )
        ## if (i <= 0.) : i -= 1

        j = int( point[1] / (self.str_hgt  + self.distation) )
        if (j >= 0.) : j = int( j )
        else: j = -1
        i = point[0] / (self.vo_rad*2 + self.distation) -(0.5*(int(j)%2))
        if (i >= 0.) : i = int( i )
        else: i = -1


        hex = (i, j)
        direct = []
        if self.inhex(point, hex, direct):
            return hex
        else:
            hex = self.neighbor(hex, direct)
            if self.inhex(point, hex):
                return hex

        return (-1, -1)


    def index_circle(self, point, delta = 0):
        """ Вычисляет индекс окружности по координатам точки point."""
        ## TODO: Написать эту ф-цию. Пока не представляю с какого боку подходить.
        return (-1, -1)


    def inhex(self, point, hex, direct=[]):
        """ Определяет принадлежит-ли точка point гексу hex
        В direct заносится направление на соседа, ближайшего к точке
        Возвращает либо True, либо False"""
        x, y = point
        i, j = hex
        cx, cy = self.center(hex)
        points = self.polygon(hex)
        dist = sqrt( (cx-x)**2 + (cy-y)**2 )

        del direct[:]
        direct.append(0)
        direct.append(0)

        #определяем четверть гекса в которою попала точка
        pa = [0,0]
        pb = [0,0]

        if ( y>=cy-self.oo_rad2 )and( y<=cy+self.oo_rad2 ):
            direct[1] = CENTER
        elif y > cy:
            direct[1] = DOWN
            pa = points[3]
            pb[1] = points[2][1]
        else:
            direct[1] = UP
            pa = points[0]
            pb[1] = points[1][1]

        if x > cx:
            direct[0] = RIGHT
            pb[0] = points[2][0]
        else:
            direct[0] = LEFT
            pb[0] = points[4][0]

        #определяем попадание в вписанную окружность, дальнейшие проверки не нужны
        if dist <= self.vo_rad:
            return True

        #отсекаем лишние точки по краям гекса (справа, слева)
        if (x < points[5][0]) or (x > points[1][0]):
            return False

        #отсекаем лишние точки по Yку с помошью уравнения прямой
        dy = abs( abs(x*(pb[1]-pa[1])-pa[0]*pb[1]+pb[0]*pa[1]) / (pb[0]-pa[0]) )
        if ( direct[1] == UP ) and ( y>dy ):
            return True
        if ( direct[1] == DOWN ) and ( y<dy ):
            return True

        return False


    def inhex_circle(self, point, hex, delta=0):
        """ Определяет попадает-ли точка point в описанный радиус гекса hex, 
        используя допуск delta
        Возвращает либо True, либо False """
        if delta:
            delta /= 2
        x, y = point
        cx, cy = self.center(hex)
        dist = sqrt( (cx-x)**2 + (cy-y)**2 )
        if dist <= (self.oo_rad + delta):
            return True
        return False


    def nearestpoint(self, point, hex, center = False):
        """ Определяет координаты ближайшей вершины гекса hex к координате point.
        Если center = True то учитывается  и центр гекса """
        ## TODO: Написать эту ф-цию. Пока не представляю с какого боку подходить.
        return (-1, -1, 0)


    def neighbor(self, hex, direct):
        """ Возвращает индекс ближайшего соседа гекса hex, по направлению direct """
        if direct[1] == UP:
            j = hex[1]-1
        elif direct[1] == CENTER:
            j = hex[1]
        else:
            j = hex[1]+1

        if direct[0] == LEFT:
            i = hex[0]-1*(hex[1]%2)
        else:
            i = hex[0]+1*(hex[1]%2)

        return (i,j)


    def neighbors(self, hex):
        """ Возвращает ближайших соседей гекса hex """
        ## FIXME: Возвращает всех и даже отрицательных соседей. Наверное не стоит?
        i, j = hex
        if not(j%2):
            return [[i-1, j-1], [i-1, j], [i-1, j+1], [i, j-1], [i, j+1], [i+1, j]]
        else:
            return [[i-1, j], [i, j-1],[i, j+1], [i+1, j-1], [i+1, j], [i+1, j+1]]


    def direct(self, hex, point)
        """ Возвращает кортеж с направлением на соседний гекс получив точку и начальный гекс"""
        direct = []
        points = self.polygon(hex)
        cx,cy = self.center(hex)
        x,y = point
        
        if ( y>=cy-self.oo_rad2 )and( y<=cy+self.oo_rad2 ):
            dy = CENTER
        elif y > cy:
            dy = DOWN
        else:
            dy = UP

        if x > cx:
            dx = RIGHT
        else:
            dx = LEFT

        return (dx,dy)


    def distance(self, hex1, hex2):
        """ принимает два гекса и считает расстояние между ними. В методе
        неверно обсчитывается случай соседства гексов 4,4 и 5,5 к примеру,
        так как считается манхэттенское расстояние """
        ## BUG: Переделать.
        i1, j1 = hex1
        j2, j2 = hex2

        return abs(j1-j2) + abs(j1 - j2)


    def path_no_barriers(self, hex1, hex2):
        """ Ищет путь. Без учёта препятствий """
        ## INFO: Код чужой непонятный. Разобраццо.
        i1, j1 = hex1
        i2, j2 = hex2

        di = i2 - i1
        dj = j2 - j1
        path = []
        x = 0

        while di != 0 or dj != 0:
            x += 1
            if dj == 0:
                if di > 0:
                    next_i, next_j = i1 + 1, j1
                else:
                    next_i, next_j = i1 - 1, j1

            elif dj > 0:
                if di > 0:
                    next_i = i1 + (j1 + 2) % 2
                    next_j = j1 + 1
                elif di < 0:
                    next_i = i1 - (j1 + 3) % 2
                    next_j = j1 + 1
                else:
                    next_i = i1
                    next_j = j1 + 1

            else:
                if di > 0:
                    next_i = i1 + (j1 + 2) % 2
                    next_j = j1 - 1
                elif di < 0:
                    next_i = i1 - (j1 + 3) % 2
                    next_j = j1 - 1
                else:
                    next_i = i1
                    next_j = j1 - 1

            i1, j1 = next_i, next_j
            path += [[i1, j1]]
            di = i2 - i1
            dj = j2 - j1

        return path


def main():
    """ Здесь будет демонстрационный пример работы с библиотекой. """
    ## INFO: Здеся далжон быдь нармальный примерчег. Неленизь дапишы.
    HEX_DIST = 20
    HEX_SIZE = 70
    HEX_SIZE2 = HEX_SIZE/2.
    HEX_OO = HEX_SIZE2 / (sqrt(3)/2)
    pole = Hex(HEX_SIZE, HEX_DIST)

    import pygame, sys
    import pygame.gfxdraw as gfx

    pygame.init()
    screen = pygame.display.set_mode((640,480))
    pygame.display.set_caption('HEX Library example')
    screen.fill((0, 0, 0))
    font = pygame.font.Font(None, 20)
    
    circle = pygame.draw.circle
    polygon = pygame.draw.polygon
    line = pygame.draw.line


    for i in range(7):
        for j in range(6):
            hex = pole.center( (i,j) )
            points = pole.polygon( (i,j) )
            #circle(screen, (255,255,255), hex, int(HEX_SIZE2), 1)
            polygon(screen, (155,155,155), points, 1)
            line(screen, (255,255,255), hex, hex, 1)#центральная точка
            text = font.render(str(i)+":"+str(j), 1, (255, 255, 255))
            screen.blit(text, hex)

    # Выбранный гекс.
    select = pygame.Surface( (pole.hex_size+1, pole.oo_rad*2+1) )
    select.set_colorkey( (0,0,0), pygame.RLEACCEL )
    select.set_alpha(150, pygame.RLEACCEL)
    points = pole.polygon( (0,0) )
    gfx.filled_polygon(select, points, (165,165,165) )
    gfx.aapolygon(select, points, (255,255,255))
    select_rect = select.get_rect()

    # Закрашенный гекс подсветки.
    solid = pygame.Surface( (pole.hex_size+1, pole.oo_rad*2+1) )
    solid_rect = solid.get_rect()
    solid.set_colorkey( (0,0,0), pygame.RLEACCEL )
    solid.set_alpha(200, pygame.RLEACCEL)
    points = pole.polygon( (0,0) )
    gfx.filled_polygon(solid, points, (195,195,195))
    gfx.aapolygon(solid, points, (255,255,255))

    screen.blit(screen, (0,0))
    pygame.display.flip()
    
    back = screen.copy()

    selected = []
    while 1:
        screen.blit(back, (0,0))
        for event in pygame.event.get(): # Перебор в списке событий
            if event.type == pygame.QUIT: # Обрабатываем событие шечка по крестику закрытия окна
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONUP:
                point = event.pos
                hex = pole.index(point)
                text = font.render(str(point[0])+":"+str(point[1]), 1, (255, 255, 255))
                if hex == (-1,-1):
                    continue
                if hex in selected:
                    selected.remove(hex)
                else:
                    selected.append(hex)

            elif event.type == pygame.MOUSEMOTION:
                point = event.pos
                hex = pole.index(point)
                if hex == (-1,-1):
                    solid_rect.center = (-100,-100)
                else:
                    xy = pole.center(hex)
                    solid_rect.center = xy

        for hex in selected:
            xy = pole.center(hex)
            select_rect.center = xy
            screen.blit( select, select_rect )

        screen.blit( solid, solid_rect )
        screen.blit(text, (10,10))
        pygame.display.flip()


if __name__ == '__main__':
    main()
