#!/usr/bin/env python
# -*- coding: utf-8 -*-

## Сей код получён путем тупого перевода кода на Ruby в код на Python.
## Внизу самом код ВРЕМЕННЫЙ чисто только для отладки, потом будет заменён
## на что-то более адекватное для демонстрации

## self.hex_size= size
## self.vo_rad  = self.hex_size / 2.
## self.oo_rad  = self.vo_rad / ( sqrt(3)/2 )
## self.oo_rad2 = self.oo_rad / 2.
## self.str_hgt = self.oo_rad + self.oo_rad2
## self.distation = dist

from math import sqrt

CENTER  = 1
UP      = 2
DOWN    = 3
LEFT    = 4
RIGHT   = 5

class HexSett:
    """ Класс для хранения настроек гексов """
    def __init__(self, hex_size, dist=1):
        self.vrad  = hex_size / 2.
        self.orad  = self.vrad / ( sqrt(3)/2 )
        self.orad2 = self.orad / 2.
        self.dist  = dist
        self.dist2 = dist / 2.
        self.disty = sqrt(self.dist**2 - self.dist2**2)
        self.str_hgt = self.orad + self.orad2
        self.size  = hex_size, self.orad*2


class Hex:
    """ Класс для обслуживания поля из правильных гексагональных ячеек. Ячейки могут
    быть не влотную друг к другу.
    i, j - номер гекса. столбец и строка. Гексы строятся со сдвигом строки
    (каждая нечетная строка сдвинута относительно четной на половину ширины)
    hex_size - расстояние между центрами противоположных граней - ширина гекса.
    vrad - радиус вписанного круга.
    orad - радиус описанного круга.
    orad2 - половина радиуса описанного круга.
    str_hgt - полтора orad (высота строки состоящей из гексов).
    dist - расстояние между гексами по умолчанию = 0 """

    def __init__(self, size, dist=0):
        """ Инициализация. Принимает размер гекса по ширине size, 
        расстояние между гексами dist"""
        self.S = HexSett(size, dist)
        if dist == 0:
            self.B = self.S
        else:
            self.B = HexSett(size+dist)


    def center(self, hex, Sett=None):
        """ Вычисляет координаты центрального пикселя. Принимает индекс гекса hex. """
        if Sett is None:
            sett = self.S
        elif Sett is HexSett:
            sett = Sett
        else:
            sett = self.B

        i,j = hex
        even = (sett.vrad + sett.dist2) * (j % 2)# смещение для чётных эл-ов

        x = sett.vrad + i*sett.vrad*2  + i*sett.dist + even 
        y = sett.orad + j*sett.str_hgt + j*sett.disty

        return  x, y


    def polygon(self, hex, Sett=None):
        """ Вычисляет координаты вершин гекса, учитывая размеры. Принимает индекс гекса hex."""
        ## INFO: Возвращает float числа, что не всегда хорошо.
        if Sett is None:
            sett = self.S
        elif Sett is HexSett:
            sett = Sett
        else:
            sett = self.B

        x, y = self.center(hex)
        path  = [[round(x), round(y - sett.orad)]]
        path += [[round(x + sett.vrad), round(y - sett.orad2)]]
        path += [[round(x + sett.vrad), round(y + sett.orad2)]]
        path += [[round(x), round(y + sett.orad)]]
        path += [[round(x - sett.vrad), round(y + sett.orad2)]]
        path += [[round(x - sett.vrad), round(y - sett.orad2)]]

        return path


    def index(self, point, Sett=None):
        """ Вычисляет индекс гекса по координатам точки point.
        !!! Нужно переписать более адекватно !!! """
        if Sett is None:
            sett = self.S
        elif Sett is HexSett:
            sett = Sett
        else:
            sett = self.B

        ## INFO: От этих условий надо как-то избавиться. Проблема в том, что если
        ##  -1 < (i или j) < 0, то они становятся 0. Из чего возниакет несколько не очень удобных ситуаций.
        ##  Например когда точка падает рядом с левым нижним углом, обсчёт здесь его берёт как ряд ниже,
        ##  но он сдвинут на пол гекса правее, и номер i становится -0.12, при отбрасывании
        ##  дробной части он становится 0, а не -1
        j = int( point[1] / (sett.str_hgt  + sett.dist) )
        if j >= 0. : j = int( j )
        else: j = -1
        i = point[0] / (sett.vrad*2 + sett.dist) -(0.5*(int(j)%2))
        if i >= 0. : i = int( i )
        else: i = -1

        hex = (i, j)
        if self.inhex(point, hex):
            return hex
        else:
            direct = self.direct(point, hex)
            hex = self.neighbor(hex, direct)
            if self.inhex(point, hex):
                return hex

        return -1, -1


    def inhex(self, point, hex, Sett=None):
        """ Определяет принадлежит-ли точка point гексу hex
        В direct заносится направление на соседа, ближайшего к точке
        Возвращает либо True, либо False"""
        if Sett is None:
            sett = self.S
        elif Sett is HexSett:
            sett = Sett
        else:
            sett = self.B
        x, y = point
        #i, j = hex
        cx, cy = self.center(hex)
        points = self.polygon(hex)

        #определяем попадание в вписанную окружность, дальнейшие проверки не нужны
        if sqrt((cx-x)**2 + (cy-y)**2) <= sett.vrad:
            return True

        #отсекаем лишние точки по краям гекса (справа, слева)
        if (points[5][0] > x) or (x > points[1][0]):
            return False

        #определяем попадание Yка в центральную область гекса
        if points[1][1] < y < points[2][1]:
            return True

        #определяем какие точки брать для уравнения прямой
        pa = [0,0] # "Центральная" точка: 0 или 3 вершины
        pb = [0,0] # "Боковая" точка: одна из двух точек справа или слева от центра (всего 4 точки)
        if y > cy:
            pa = points[3] # "нижняя" вершина
            pb[1] = points[2][1] # Y-координа "нижней" точки (2 или 4)
        else:
            pa = points[0] # верхняя вершина
            pb[1] = points[1][1] # Y-координа "верхней" точки (1 или 5)

        if x > cx:
            pb[0] = points[2][0] # X-координата "правой" точки (1 или 2)
        else:
            pb[0] = points[4][0] # X-координата "левой" точки (4 или 5)

        #отсекаем лишние точки по Yку с помошью уравнения прямой
        dy = abs(abs(x*(pb[1]-pa[1])-pa[0]*pb[1]+pb[0]*pa[1]) / (pb[0]-pa[0]))
        direct = self.direct(point, hex)
        if ( direct[1] == UP ) and ( y>dy ): # 
            return True
        if ( direct[1] == DOWN ) and ( y<dy ):
            return True

        return False


    def nearestpoint(self, point, center=False, Sett=None):
        """ Определяет координаты ближайшего гекса и его ближайшей вершины к координате point.
        Если center=True то учитывается  и центр гекса """
        ## TODO: Написать эту ф-цию. Пока не представляю с какого боку подходить.
        if Sett is None:
            sett = self.B
        else:
            sett = Sett

        hex = self.index(point, sett)
        if hex == (-1,-1):
            print "Ooooopsss!"
            return -1, -1, 0

        points = self.polygon(hex)
        if center:
            points.append(self.center(hex))
        dist = []
        for p in points:
            dist.append(sqrt((p[0]-point[0])**2 + (p[1]-point[1])**2))
        mdist = dist.index(min(dist))
        print dist, mdist

        return hex, mdist


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

        return i,j


    def neighbors(self, hex):
        """ Возвращает ближайших соседей гекса hex """
        ## FIXME: Возвращает всех и даже отрицательных соседей. Наверное не стоит?
        i, j = hex
        if not(j%2):
            return [[i-1, j-1], [i-1, j], [i-1, j+1], [i, j-1], [i, j+1], [i+1, j]]
        else:
            return [[i-1, j], [i, j-1], [i, j+1], [i+1, j-1], [i+1, j], [i+1, j+1]]


    def direct(self, point, hex, Sett=None):
        """ Возвращает кортеж с направлением на соседний гекс, получив точку и начальный гекс"""
        if Sett is None:
            sett = self.S
        elif Sett is HexSett:
            sett = Sett
        else:
            sett = self.B

        cx,cy = self.center(hex)
        x,y = point
        
        if cy-sett.orad2 <= y <= cy+sett.orad2:
            dy = CENTER
        elif y > cy:
            dy = DOWN
        else:
            dy = UP

        if x > cx:
            dx = RIGHT
        else:
            dx = LEFT

        return dx,dy


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
    HEX_DIST = 0
    HEX_SIZE = 70
    pole = Hex(HEX_SIZE, HEX_DIST)
    sett = pole.S

    import pygame, sys
    import pygame.gfxdraw as gfx

    pygame.init()
    screen = pygame.display.set_mode((640,480))
    pygame.display.set_caption('HEX Library example')
    screen.fill((0, 0, 0))
    font = pygame.font.Font(None, 20)
    
    #circle = pygame.draw.circle
    polygon = pygame.draw.polygon
    line = pygame.draw.line


    for i in range(7):
        for j in range(6):
            hex = pole.center( (i,j) )
            hex2 = pole.center( (i,j), pole.B )
            points = pole.polygon( (i,j) )
            polygon(screen, (255,255,255), points, 1)
            line(screen, (255,255,0), hex, hex)#центральная точка
            text = font.render(str(i)+":"+str(j), 1, (255, 255, 255))
            screen.blit(text, hex)

            points2 = pole.polygon( (i,j), pole.B)
            polygon(screen, (155,155,155), points2, 1)
            line(screen, (255,0,0), hex2, hex2)#центральная точка

    # Выбранный гекс.
    select = pygame.Surface( (sett.vrad*2+1, sett.orad*2+1) )
    select.set_colorkey( (0,0,0), pygame.RLEACCEL )
    select.set_alpha(150, pygame.RLEACCEL)
    points = pole.polygon( (0,0) )
    gfx.filled_polygon(select, points, (165,165,165) )
    gfx.aapolygon(select, points, (255,255,255))
    select_rect = select.get_rect()

    # Закрашенный гекс подсветки.
    solid = pygame.Surface( (sett.vrad*2+1, sett.orad*2+1) )
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
    text = font.render("0:0", 1, (255, 255, 255))
    while 1:
        screen.blit(back, (0,0))
        for event in pygame.event.get(): # Перебор в списке событий
            if event.type == pygame.QUIT: # Обрабатываем событие шечка по крестику закрытия окна
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONUP:
                point = event.pos
                hex = pole.index(point)
                min = pole.nearestpoint(point,True)
                print "Min dist", min
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
