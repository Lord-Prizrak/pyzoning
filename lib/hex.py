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

class Hex:  
    def __init__(self, size, pust=0):
        """ Инициализация. """
        self.hex_size= size
        self.vo_rad  = self.hex_size / 2.
        self.oo_rad  = self.vo_rad / ( sqrt(3)/2 )
        self.oo_rad2 = self.oo_rad / 2.
        self.str_hgt = self.oo_rad + self.oo_rad2
        self.pust = pust
        print self.hex_size, self.vo_rad, self.oo_rad, self.oo_rad2, self.str_hgt

    def field_size(self, hex_in_row, hex_in_column):
        """ считает размер поля в пикселях. """
        return (self.hex_size*hex_in_row+self.hex_size/2+5, self.str_hgt*hex_in_column+self.oo_rad2+5)
  
    def center(self, i, j):
        """ принимает индекс гекса и высчитывает центральный пиксель 
        - пересечение диагоналей. """
        x = self.vo_rad+ i*self.hex_size +(self.vo_rad+self.pust/2)*(j%2) +self.pust*i
        y = self.oo_rad+ j*self.str_hgt +self.pust*j
        #print u"Смещ:", j%2
        #print u"Цент:", (x, y)
        return  (x, y)
        #return  (int((self.vo_rad%2)*(i%2)  +self.hex_size*i +self.vo_rad), int(self.oo_rad+j*self.str_hgt))

    def polygon(self, i, j):
        """ принимает индексы гекса и выдает массив пикселей(вершины), 
        образующих шестиугольник. Учитывает размеры гекса. """
        #print u"Поли:", i, j
        x, y = self.center(i, j)
        path  = [[x, y - self.oo_rad]]
        path += [[x + self.vo_rad, y - self.oo_rad2]]
        path += [[x + self.vo_rad, y + self.oo_rad2]]
        path += [[x, y + self.oo_rad]]
        path += [[x - self.vo_rad, y + self.oo_rad2]]
        path += [[x - self.vo_rad, y - self.oo_rad2]]
        #print u"Коор:", path
        return path
  
    def index(self, x, y):
        """ принимает в качестве аргумента координату пикселя, и выдает, 
        к какому гексу она относится. """
        j = int( y / (self.str_hgt + self.pust) )
        i = int( x / (self.vo_rad*2 + self.pust) -(0.5*(int(j)%2)) )
        hx, hy = self.center(i,j)
        dist = sqrt( (hx-x)**2 + (hy-y)**2 )

        print "-------------------------------------"
        print "Inde:", i, j
        print "Cent:", hx, hy
        print "VO_RAD2:", self.vo_rad, "      OO_RAD2:", self.oo_rad, " L:", dist
        if dist < (self.vo_rad):
            print "V"
            return (i, j)
        else:
            if dist < (self.oo_rad): print "O"
            else:
                if dist > (self.oo_rad): 
                    print "NOT_HEX"
                    return (-1, -1)
                else: print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
        return ( int(i), int(j) )
#        x = self.vo_rad+ i*self.hex_size +(self.vo_rad)*(j%2)
#        y = self.oo_rad+ j*self.str_hgt


    def distance(self, hex1, hex2):
        """ принимает два гекса и считает расстояние между ними. В методе 
        неверно обсчитывается случай соседства гексов 4,4 и 5,5 к примеру, 
        так как считается манхэттенское расстояние. Мне для алгоритма А* 
        больше и не нужно."""
        i1, j1 = hex1
        j2, j2 = hex2
        (j1-j2).abs + (j1 - j2).abs    

    ## def neighbors(self, hex):
        ## """ возвращает соседей заданного поля. """
        ## i, j = *hex
        ## j.even? 
            ## neighbors = [[i-1, j-1], [i-1, j], [i-1, j+1], [i, j-1], [i, j+1], [i+1, j]]
        ## else
            ## neighbors = [[i-1, j], [i, j-1],[i, j+1], [i+1, j-1], [i+1, j], [i+1, j+1]]
        ## neighbors.find_all {|hex| hex[0]>=0 and hex[1]>=0}

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

print  "!START!"
import pygame, sys
pygame.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption('example')
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((0, 0, 0))
screen.blit(background, (0,0))
font = pygame.font.Font(None, 20)

HEX_DIST = 10
HEX_SIZE = 120
HEX_SIZE2 = HEX_SIZE/2.
HEX_OO = HEX_SIZE2 / (sqrt(3)/2)

pole = Hex(HEX_SIZE, HEX_DIST)
for i in range(3):
    for j in range(3):
        x, y = pole.center(i,j)
        rx = int( round(x) )
        ry = int( round(y) )
        print pole.polygon(i,j)
        print rx, ry
        pygame.draw.polygon(screen, (255,255,255), pole.polygon(i,j), 1)
        pygame.draw.circle(screen, (255,0,255), (rx,ry), int( round(HEX_SIZE2) ),1)
        pygame.draw.circle(screen, (0,255,0), (rx,ry), int( round(HEX_OO) ), 1)
        pygame.draw.line(screen, (255,255,255), (x,y), (x,y), 1)
        
        text = font.render(str(i)+":"+str(j), 1, (250, 250, 250))
        screen.blit(text, (x,y))
        #print "------------------------------------------------------------------------------"
pygame.display.flip()
        
while 1:
    for i in pygame.event.get(): # Перебор в списке событий
        if i.type == pygame.QUIT: # Обрабатываем событие шечка по крестику закрытия окна
            sys.exit()
        if i.type == pygame.MOUSEBUTTONDOWN:
            x, y = i.pos
            i, j = pole.index(x,y)
            
            print x, y, " - ", i, j
            pygame.draw.polygon(screen, (255,15,105), pole.polygon(i,j), 2)
            pygame.display.flip()
            #print i #pos, rel, buttons


print  "!END!"



