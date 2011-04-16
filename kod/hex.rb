# -*- coding: utf-8 -*-
## i, j - номер гекса. столбец и строка. Гексы строятся со сдвигом строки
## (каждая нечетная строка сдвинута относительно четной на половину ширины)

## size, w - расстояние между центрами соседних гексов, оно же ширина гекса.
## r - радиус вписанного круга.
## s - радиус описанного круга.
## h - полтора s (высота строки состоящей из гексов)

## методы:
## center - принимает индекс гекса и высчитывает центральный пиксель -
## пересечение диагоналей.
## polygon - принимает индексы гекса и выдает массив пикселей(вершины), 
## образующих шестиугольник. Учитывает размеры гекса.
## index - принимает в качестве аргумента координату пикселя, и выдает, 
## к какому гексу она относится.
## статический метод distance - принимает два гекса и считает расстояние
## между ними. В методе неверно обсчитывается случай соседства 
## гексов 4,4 и 5,5 к примеру, так как считается манхэттенское расстояние. 
## Мне для алгоритма А* больше и не нужно.
## field_size - считает размер поля в пикселях.
## статический метод neighbors - возвращает соседей заданного поля.
## ну и два path-а, которые находят путь между гексами. Один с 
## учетом препятствий(А*), второй - нет.

class Hex
  
  attr_reader :w, :s, :l, :h, :r
  
  def initialize(size)
    @w = size
    @r = @w / 2
    @s = @r / Math.cos(Math::PI / 6.0)
    @l = @s / 2.0
    @s = @s
    @h = @s + @l
  end
  
  def polygon(i, j)
    x, y = *center(i, j)
    path  = [[x, y - @s]]
    path += [[x + @r, y - @l]]
    path += [[x + @r, y + @l]]
    path += [[x, y + @s]]
    path += [[x - @r, y + @l]]
    path += [[x - @r, y - @l]]
  end
  
  def center(i, j)
    c = j.even? ? [@w/2+@w*i, @s+j*@h] : [@w*(i+1), @h*j+@s ]
    c.map{|elem|elem.round}
  end
   
  def index(x, y)
    a = @w.round
    b = (2*@s).round
    h = @l.round
    r = @r.round
    s = @s.round
    m = h.to_f / r
    
    sectx = x / (2*r)
    secty = y / (h+s)
    
    sectpxlx = x % (2*r)
    sectpxly = y % (h+s)    
    if (secty % 2).zero? then
      if sectpxly < (h - sectpxlx*m)
        secty -= 1
        sectx -= 1
      end
      if sectpxly< (-h + sectpxlx*m)
        secty -=1
      end


    else
      if sectpxlx >= r
        if sectpxly < (2*h - sectpxlx*m)
          secty-=1
        end
      end
      if sectpxlx < r
        if sectpxly < (sectpxlx*m)
          secty-=1
        else
          sectx-=1
        end
      end
    end
    [sectx, secty]
  end

  def self.distance(hex1, hex2)
    i1, j1 = *hex1
    j2, j2 = *hex2
    (j1-j2).abs + (j1 - j2).abs    
  end

  def field_size(hex_in_row, hex_in_column)
    [@w*hex_in_row+@w/2+5, @h*hex_in_column+@l+5]
  end
  
  def self.path(hex1, hex2, barriers, map_size)
    find_path(hex1, hex2, barriers, map_size)
  end
  
  def self.path_no_barriers(hex1, hex2)
    i1, j1 = *hex1
    i2, j2 = *hex2

    di = i2 - i1
    dj = j2 - j1
    path = Array.new
    until di.zero? and dj.zero?
      if dj == 0
        if di > 0
          next_i, next_j = i1 + 1, j1
        else
          next_i, next_j = i1 - 1, j1
        end
      else
        if dj > 0
          if di > 0
            next_i = i1 + (j1 + 2) % 2
            next_j = j1 + 1
          else
            if di < 0
              next_i = i1 - (j1 + 3) % 2
              next_j = j1 + 1
            else
             next_i = i1
             next_j = j1 + 1
            end
          end
        else
          if di > 0
            next_i = i1 + (j1 + 2) % 2
            next_j = j1 - 1
          else
            if di < 0
              next_i = i1 - (j1 + 3) % 2
              next_j = j1 - 1
            else
              next_i = i1
              next_j = j1-1
            end
          end
        end
      end
      i1, j1 = next_i, next_j
      path += [[i1, j1]]
      di = i2 - i1
      dj = j2 - j1
    end
    return path    
  end

  def self.neighbors(hex)
    i, j = *hex
    j.even? 
      neighbors = [[i-1, j-1], [i-1, j], [i-1, j+1], [i, j-1], [i, j+1], [i+1, j]]
    else
      neighbors = [[i-1, j], [i, j-1],[i, j+1], [i+1, j-1], [i+1, j], [i+1, j+1]]
    end
    neighbors.find_all {|hex| hex[0]>=0 and hex[1]>=0}
  end
end
