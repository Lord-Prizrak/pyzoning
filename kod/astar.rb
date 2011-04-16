class Node

  attr_accessor :i, :j, :parent, :f, :g, :h
  
  def initialize(index, parent, start_node, target_node, map_size)
    @start = start_node
    @target = target_node
    @i, @j = *index
    @parent = parent
    @map_size = map_size
    calculate_cost
  end
  def index
    [@i, @j]
  end
  def calculate_cost
    @g = @parent ? @parent.g + 1 : 0
    @h = distance([@i, @j], @target)
    @f = @g + @h
  end
  
  def neighbors
    @j.even? ? [
      [@i-1, @j-1],
      [@i-1, @j],
      [@i-1, @j+1],
      [@i, @j-1],
      [@i, @j+1],
      [@i+1, @j]].find_all { |hex| hex[0]>=0 and hex[1]>=0 and hex[0] < @map_size[0] and hex[1] < @map_size[1] } \
    : [
      [@i-1, @j],
      [@i, @j-1],
      [@i, @j+1],
      [@i+1, @j-1],
      [@i+1, @j],
      [@i+1, @j+1]].find_all { |hex| hex[0]>=0 and hex[1]>=0 and hex[0] < @map_size[0] and hex[1] < @map_size[1]}
  end

  def ==(index)
    @i == index[0] and @j == index[1]
  end
  def is_start?
    @i == @start[0] and @j == @start[1]
  end
  def is_target?
    @i == @target[0] and @j == @target[1]
  end
end

def distance(hex1, hex2)
  (hex2[0] - hex1[0]).abs + (hex2[1] - hex1[1]).abs
end

def find_path(start_index, end_index, barriers, map_size)
  start = start_index
  target = end_index
  open_list = []
  while barriers.include?(target)
    target = Node.new(target, nil, start, target, map_size).neighbors.min_by { |node| distance(start, node) }
  end
  open_list = [Node.new(start, nil, start, target, map_size)]
  closed_list = []
  until open_list.include?(target)
    current = open_list.min_by { |node| node.f }
    closed_list.push(current)
    open_list-=[current]

    current.neighbors.each { |neighbor|
      open_list.push(Node.new(neighbor, current, start, target, map_size)) unless (barriers.include?(neighbor) or closed_list.include?(neighbor)) or open_list.include?(neighbor)
    }
    break if open_list.empty?
  end
  unless open_list.empty?
    path_end_node = open_list.find_all{|node|node.is_target?}[0]
    path = [target]
    while path_end_node = path_end_node.parent
      path.push(path_end_node.index)
    end
  else
    path = []
  end
  path.reverse
end
