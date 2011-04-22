#!python
# -*- coding: utf-8 -*-

## i, j - номер гекса. столбец и строка. Гексы строятся со сдвигом строки
## (каждая нечетная строка сдвинута относительно четной на половину ширины)
## hex_size - расстояние между центрами противоположных граней - ширина гекса.
## vo_rad - радиус вписанного круга.
## oo_rad - радиус описанного круга.
## str_hgt - полтора self.oo_rad (высота строки состоящей из гексов).
## oo_rad2 - половина радиуса описанного круга.

## Сей код получён путем тупого перевода кода на Ruby в код на Python.
## Внизу самом код ВРЕМЕННЫЙ чисто только для отладки, потом будет заменён на что-то более адекватное.

from math import cos, pi, sqrt

CENTER  = 1
UP      = 2
DOWN    = 3
LEFT    = 4
RIGHT   = 5

class Hex:
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

        return  (x, y)


    def polygon(self, hex):
        """ Вычисляет координаты вершин гекса, учитывая размеры.
        Принимает индекс гекса hex."""
        x, y = self.center(hex)
        path  = [[x, y - self.oo_rad]]
        path += [[x + self.vo_rad, y - self.oo_rad2]]
        path += [[x + self.vo_rad, y + self.oo_rad2]]
        path += [[x, y + self.oo_rad]]
        path += [[x - self.vo_rad, y + self.oo_rad2]]
        path += [[x - self.vo_rad, y - self.oo_rad2]]

        return path


    def index(self, point):
        """ Вычисляет индекс гекса по координатам точки point.
        !!! Нужно переписать более адекватно !!! """
        print "------------------------------------------------------"
        j = int( point[1] / (self.str_hgt + self.distation) )
        i = int( point[0] / (self.vo_rad*2 + self.distation) -(0.5*(int(j)%2)) )
        hex = (i, j)

        direct = []
        if self.inhex(point, hex, direct):
            print "OK 1"
            return hex
        else:
            print hex, direct, point
            hex = self.neighbor(hex, direct)
            print hex
            if self.inhex(point, hex):
                print "OK 2"
                return hex
            else: 
                print "NOT 2"
                return (-1, -1)
        
        print "NOT"
        return (-1, -1)
    
    
    def inhex(self, point, hex, direct=[]):
        """ Определяет принадлежит-ли точка point гексу hex
        В direct заносится направление на соседа, ближайшего к точке
        Возвращает либо True, либо False"""
        x, y = point
        i, j = hex
        cx, cy = self.center(point)
        points = self.polygon(hex)
        dist = sqrt( (cx-x)**2 + (cy-y)**2 )

        del direct[:]
        direct.append(0)
        direct.append(0)

        #определяем четверть гекса в которою попала точка
        pa = [0,0]
        pb = [0,0]
        if y > cy:
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
            if (y>=points[1][1])and(y<=points[2][1]):
                direct[1] = CENTER
            return True

        #отсекаем лишние точки по краям гекса (справа, слева)
        if (x <= points[5][0]) or (x >= points[1][0]):
            if (y>=points[1][1])and(y<=points[2][1]):
                direct[1] = CENTER
            return False

        #отсекаем лишние точки по Yку с помошью уравнения прямой
        dy = abs( abs(x*(pb[1]-pa[1])-pa[0]*pb[1]+pb[0]*pa[1]) / (pb[0]-pa[0]) )
        if (direct[1] == UP)and(y>dy):
            return True
        if (direct[1] == DOWN)and(y<dy):
            return True

        return False


    def neighbor(self, hex, direct):
        """ Возвращает индекс ближайшего соседа гекса hex, по направлению direct
        """
        nhex = [0,0]
        if direct[1] == UP:
            nhex[1] = hex[1]-1
        elif direct[1] == CENTER:
            nhex[1] = hex[1]
        else:
            nhex[1] = hex[1]+1

        if direct[0] == LEFT:
            nhex[0] = nhex[0]-1*(hex[0]%2)
        else:
            nhex[0] = nhex[0]+1*(hex[0]%2)

        return nhex


    def neighbors(self, hex):
        """ Возвращает ближайших соседей гекса hex """
        i, j = hex
        if not(j%2):
            neighbors = [[i-1, j-1], [i-1, j], [i-1, j+1], [i, j-1], [i, j+1], [i+1, j]]
        else:
            neighbors = [[i-1, j], [i, j-1],[i, j+1], [i+1, j-1], [i+1, j], [i+1, j+1]]

        return neighbors#.find_all {|hex| hex[0]>=0 and hex[1]>=0}


    def distance(self, hex1, hex2):
        """ принимает два гекса и считает расстояние между ними. В методе
        неверно обсчитывается случай соседства гексов 4,4 и 5,5 к примеру,
        так как считается манхэттенское расстояние. Мне для алгоритма А*
        больше и не нужно."""
        i1, j1 = hex1
        j2, j2 = hex2
        return (j1-j2).abs + (j1 - j2).abs


    ## def field_size(self, hex_in_row, hex_in_column):
        ## """ считает размер поля в пикселях. """
        ## return (self.hex_size*hex_in_row+self.hex_size/2+5, self.str_hgt*hex_in_column+self.oo_rad2+5)

   ## def path(self, hex1, hex2, barriers, map_size):
        ## """ Ищет путь. С учетом препятствий(А*). """
        ## find_path(hex1, hex2, barriers, map_size)
    ## end

    ## def path_no_barriers(self, hex1, hex2):
        ## """ Ищет путь. Без учёта препятствий """
        ## i1, j1 = *hex1
        ## i2, j2 = *hex2

        ## di = i2 - i1
        ## dj = j2 - j1
        ## path = Array.new
        ## until di.zero? and dj.zero?
            ## if dj == 0
                ## if di > 0
                    ## next_i, next_j = i1 + 1, j1
                ## else
                    ## next_i, next_j = i1 - 1, j1
                ## end
            ## else
                ## if dj > 0
                    ## if di > 0
                        ## next_i = i1 + (j1 + 2) % 2
                        ## next_j = j1 + 1
                    ## else
                        ## if di < 0
                            ## next_i = i1 - (j1 + 3) % 2
                            ## next_j = j1 + 1
                        ## else
                            ## next_i = i1
                            ## next_j = j1 + 1
                        ## end
                    ## end
                ## else
                    ## if di > 0
                        ## next_i = i1 + (j1 + 2) % 2
                        ## next_j = j1 - 1
                    ## else
                        ## if di < 0
                            ## next_i = i1 - (j1 + 3) % 2
                            ## next_j = j1 - 1
                        ## else
                            ## next_i = i1
                            ## next_j = j1-1
                        ## end
                    ## end
                ## end
            ## end
            ## i1, j1 = next_i, next_j
            ## path += [[i1, j1]]
            ## di = i2 - i1
            ## dj = j2 - j1
        ## end
        ## return path
    ## end
## end


if __name__ == '__main__':
    import pygame, sys
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption('example')
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 0, 0))
    screen.blit(background, (0,0))
    font = pygame.font.Font(None, 20)
    
    HEX_DIST = 20
    HEX_SIZE = 120
    HEX_SIZE2 = HEX_SIZE/2.
    HEX_OO = HEX_SIZE2 / (sqrt(3)/2)
    
    pole = Hex(HEX_SIZE, HEX_DIST)
    for i in range(3):
        for j in range(3):
            x, y = pole.center( (i,j) )
            points = pole.polygon( (i,j) )
            pygame.draw.polygon(screen, (255,255,255), points, 1)
            pygame.draw.line(screen, (255,255,255), (x,y), (x,y), 1)#центральная точка
            text = font.render(str(i)+":"+str(j), 1, (250, 250, 250))
            screen.blit(text, (x,y))

            ## rx = int( round(x) )
            ## ry = int( round(y) )
            ## pygame.draw.circle(screen, (255,0,255), (rx,ry), int( round(HEX_SIZE2) ),1)
            ## pygame.draw.circle(screen, (0,255,0), (rx,ry), int( round(HEX_OO) ), 1)

    pygame.display.flip()
    
    while 1:
        for i in pygame.event.get(): # Перебор в списке событий
            if i.type == pygame.QUIT: # Обрабатываем событие шечка по крестику закрытия окна
                sys.exit()
            if i.type == pygame.MOUSEBUTTONDOWN:
                point = i.pos
                hex = pole.index(point)
                poligon = pole.polygon(hex)
    
                pygame.draw.polygon(screen, (255,15,105), poligon, 2)
                pygame.draw.line(screen, (255,255,255), point, point, 1)
    
                for pol in poligon:
                    text = font.render(str(int(pol[0]))+":"+str(int(pol[1])), 0, (250, 250, 250))
                    screen.blit(text, pol)
    
                pygame.display.flip()
