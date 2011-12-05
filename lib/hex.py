#!/usr/bin/env python
# -*- coding: utf-8 -*-

from math import sqrt

CENTER  = 1
UP      = 2
DOWN    = 3
LEFT    = 4
RIGHT   = 5

class HexSize:
    """ Класс для хранения настроек гексов 
    hex_size - расстояние между центрами противоположных граней - ширина гекса.
    vrad - радиус вписанного круга.
    orad - радиус описанного круга.
    orad2 - половина радиуса описанного круга.
    str_hgt - полтора orad (высота строки состоящей из гексов).
    dist - расстояние между гексами по умолчанию = 0 """

    def __init__(self, hex_size, dist=1):
        ## TODO: Оформить всё как свойства
        self.vrad  = hex_size / 2.
        self.orad  = self.vrad / ( sqrt(3.)/2. )
        self.orad2 = self.orad / 2.
        self.distx  = float(dist)
        self.dist2 = dist / 2.
        self.disty = sqrt(self.distx**2. - self.dist2**2.)
        self.str_hgt = self.orad + self.orad2
        self.size  = float(hex_size), self.orad*2.


class Hex:
    """ Класс для обслуживания поля из правильных гексагональных ячеек. Ячейки
    могут быть не влотную друг к другу.
    i, j - номер гекса. столбец и строка. Гексы строятся со сдвигом строки
    (каждая нечетная строка сдвинута относительно четной на половину ширины)
    S - размеры для малого гекса (в расчётах почти не используется) (отображается)
    B - размеры для большого гекса (почти вовсех расчётах пользуется) """

    def __init__(self, size, dist=0):
        """ Инициализация.
        size - размер гекса по ширине;
        dist - расстояние между гексами """

        self.S = HexSize(size, dist)
        if dist == 0:
            self.B = self.S
        else:
            self.B = HexSize(size+dist)


    def center(self, hex, Sett=None):
        """ Вычисляет координаты центральной точки.
        hex - индекс гекса """
        ## Центр ВСЕГДА считается по параметрам больших гексов. Либо пользуем
        ## размеры из Sett.
        if Sett:
            sett = Sett
        else:
            sett = self.B

        i,j = hex
        even = (sett.vrad + sett.dist2) * (j % 2)# смещение для чётных эл-ов

        x = i*sett.size[0] + i*sett.distx + sett.vrad + even        
        y = j*sett.str_hgt + j*sett.disty + sett.orad 

        return  x, y


    def polygon(self, hex, bighex=False, Sett=None):
        """ Вычисляет координаты вершин гекса, учитывая размеры.
        hex - индекс гекса """
        ## По умолчанию пользуем размеры малого гекса - он должен отображаться
        ## INFO: Возвращает float числа, что не всегда хорошо.
        if Sett:
            sett = Sett
        elif bighex:
            sett = self.B
        else:
            sett = self.S

        x, y = self.center(hex, Sett)
        ## path  = [[round(x), round(y - sett.orad)]]
        ## path += [[round(x + sett.vrad), round(y - sett.orad2)]]
        ## path += [[round(x + sett.vrad), round(y + sett.orad2)]]
        ## path += [[round(x), round(y + sett.orad)]]
        ## path += [[round(x - sett.vrad), round(y + sett.orad2)]]
        ## path += [[round(x - sett.vrad), round(y - sett.orad2)]]
        
        path  = [[x, y - sett.orad]]
        path += [[x + sett.vrad, y - sett.orad2]]
        path += [[x + sett.vrad, y + sett.orad2]]
        path += [[x, y + sett.orad]]
        path += [[x - sett.vrad, y + sett.orad2]]
        path += [[x - sett.vrad, y - sett.orad2]]

        return path


    def index(self, point, bighex=False, Sett=None):
        """ Вычисляет индекс гекса по координатам точки/
        point - кортеж с координатами (x,y) """
        ## BUG: Нужно переписать более адекватно!
        ## FIX: посмотреть все косявки, и изгнать их.
        if Sett:
            sett = Sett
        else:
            sett = self.S

        x,y = point
        
        y -= sett.disty #смещение, что-бы центр гекса совпадал с центром кваратной ячейки
        
        j = int( y/(sett.str_hgt+sett.disty) )
        i = int( x/(sett.size[0]+sett.distx) -(0.5*(j%2)) )

        if j < 0 or i < 0:
            return -1, -1

        hex = (i, j)
        
        if self.inhex(point, hex, bighex, Sett):
            return hex
        else:
            direct = self.direct(point, hex)
            hex = self.neighbor(hex, direct)
            if (hex[0]<0)or(hex[1]<0):
                return -1,-1
            if self.inhex(point, hex, bighex, Sett):
                return hex

        return -1, -1


    def inhex(self, point, hex, bighex=False, Sett=None):
        """ Определяет принадлежит-ли точка point гексу hex
        В direct заносится направление на соседа, ближайшего к точке
        Возвращает либо True, либо False """
        if Sett:
            sett = Sett
        elif bighex:
            sett = self.B
        else:
            sett = self.S

        x, y = point
        cx, cy = self.center(hex, Sett)
        points = self.polygon(hex, bighex, Sett)

        #определяем попадание в вписанную окружность
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
        ## direct = self.direct(point, hex)
        ## if ( direct[1] == UP ) and ( y>dy ):
            ## return True
        ## if ( direct[1] == DOWN ) and ( y<dy ):
            ## return True
        if ( cy>y ) and ( y>dy ):
            return True
        if ( cy<y ) and ( y<dy ):
            return True

        return False


    def nearestpoint(self, point, center=False, Sett=None):
        """ Определяет координаты ближайшего гекса и его ближайшей вершины 
        к координате point. Если center=True то учитывается  и центр гекса """
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
        print "FROM:",hex, direct
        s = ""
        
        if direct[0] == LEFT:
            i = hex[0]-1*((hex[1]+1)%2)
            s += "L"
        elif direct[0] == RIGHT:
            i = hex[0]+1*( hex[1] % 2 )
            s += "R"
        else:
            i = -1
            s += "?"

        if direct[1] == CENTER:
            j = hex[1]
            
            if direct[0] == LEFT:
                i = hex[0]-1
            elif direct[0] == RIGHT:
                i = hex[0]+1
            s +=  "C"
        elif direct[1] == UP:
            j = hex[1]-1
            s += "U"
        elif  direct[1] == DOWN:
            j = hex[1]+1
            s +=  "D"
        else:
            s += "%"
            j = -1


        print s
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
        """ Возвращает кортеж с направлением на соседний гекс,
        получив точку и начальный гекс"""
        ## BUG: Небольшая погрешность вычислений. Откуда непонятно.
        ## Особенно заметно на больших расстояниях.
        if Sett is None:
            sett = self.S
        elif Sett is HexSize:
            sett = Sett

        cx,cy = self.center(hex)
        x,y = point

        if x > cx:
            dx = RIGHT
        else:
            dx = LEFT

        ## INFO: Через равносторонние треугольники
        deltax = abs( (cx-x)/2. )
        deltay = abs( cy - y )
        if deltay < deltax:
            dy = CENTER
        elif y < cy:
            dy = UP
        elif y > cy:
            dy = DOWN
        else:
            print u"Ошибка в функции direct!!!"
            dy = 0

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


def main_tst():
    """ Здесь будет демонстрационный пример работы с библиотекой. """
    HEX_DIST = 30
    HEX_SIZE = 70
    pole = Hex(HEX_SIZE, HEX_DIST)

    import pygame, sys
    from pygame.draw import polygon, line, circle
    from pygame.gfxdraw import rectangle
    import pygame.gfxdraw as gfx

    pygame.init()
    screen = pygame.display.set_mode((640,480))
    pygame.display.set_caption('HEX Library example')
    screen.fill((0, 0, 0))
    font = pygame.font.Font(None, 20)
    
    sett = pole.B
    r = pygame.Rect( (0,0), (sett.size[0]+sett.distx,sett.str_hgt+sett.disty+1) )
    sett = pole.S
    r2 = pygame.Rect( (0,0), (sett.size[0]+sett.distx,sett.str_hgt+sett.disty+1) )

    for i in range(7):
        for j in range(6):
            xy = pole.center( (i,j) )
            points = pole.polygon( (i,j) )
            polygon(screen, (255,255,255), points, 1)
            line(screen, (255,255,0), xy, xy)#центральная точка
            text = font.render(str(i)+":"+str(j), 1, (255, 255, 255))
            screen.blit(text, xy)

            points2 = pole.polygon( (i,j), True)
            polygon(screen, (255,255,255), points2, 1)

            r.center = xy
            #rectangle(screen, r, (0,100,0))

    # Выбранный гекс.
    sett = pole.B
    select = pygame.Surface( (sett.size[0]+1, sett.size[1]+1) )
    select.set_colorkey( (0,0,0), pygame.RLEACCEL )
    select.set_alpha(150, pygame.RLEACCEL)
    points = pole.polygon( (0,0) )
    polygon(select, (165,165,165), points )
    polygon(select, (255,255,255), points, 1)
    select_rect = select.get_rect()

    # Закрашенный гекс подсветки.
    solid = pygame.Surface( (sett.size[0]+1, sett.size[1]+1) )
    solid.set_colorkey( (0,0,0), pygame.RLEACCEL )
    solid.set_alpha(200, pygame.RLEACCEL)
    points = pole.polygon( (0,0) )
    polygon(solid, (195,195,195), points)
    polygon(solid, (255,255,255), points, 1)
    solid_rect = solid.get_rect()
    
    sett = pole.B
    # Закрашенный большой гекс подсветки.
    solid2 = pygame.Surface( (sett.size[0]+1, sett.size[1]+1) )
    solid2.set_colorkey( (0,0,0), pygame.RLEACCEL )
    solid2.set_alpha(200, pygame.RLEACCEL)
    points2 = pole.polygon( (0,0), True )
    polygon(solid2, (195,95,195), points2)
    polygon(solid2, (255,55,255), points2, 1)
    solid_rect2 = solid2.get_rect()

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
                
                if hex in selected:
                    selected.remove(hex)
                else:
                    selected.append(hex)

                ## min = pole.nearestpoint(point,True)
                ## text = font.render(str(point[0])+":"+str(point[1]), 1, (255, 255, 255))
                ## if hex == (-1,-1):
                    ## continue
                ## if hex in selected:
                    ## selected.remove(hex)
                ## else:
                    ## selected.append(hex)

            elif event.type == pygame.MOUSEMOTION:
                point = event.pos
                ## hex = pole.index(point)
                hex2 = pole.index(point, True)
                ## if hex == (-1,-1):
                    ## solid_rect.center = (-100,-100)
                ## else:
                    ## xy = pole.center(hex)
                    ## solid_rect.center = xy
                    
                if selected:
                    f = selected[0]
                    s = pole.neighbor(f,pole.direct(point,f))
                    print "TO:", s


                if hex2 == (-1,-1):
                    solid_rect2.center = (-100,-100)
                else:
                    xy = pole.center(hex2)
                    solid_rect2.center = xy

        for hex in selected:
            xy = pole.center(hex)
            select_rect.center = xy
            screen.blit( select, select_rect )

        screen.blit( solid, solid_rect )
        screen.blit( solid2, solid_rect2 )
        screen.blit(text, (10,10))
        pygame.display.flip()


if __name__ == '__main__':
    main_tst()
