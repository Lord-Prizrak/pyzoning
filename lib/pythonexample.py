#Example usage:
from test_python import *

c = [(832,1093),(810,1121),(787,1156),(827,1173),(838,1167),(858,1157),(873,1132),(873,1107),(832,1093)]
p = []

for coord in c:
   point = Point(coord[0],coord[1])
   p.append(point)
   
poly = Contour(p)

centroidPoint= poly.centroid()

print centroidPoint.x
print centroidPoint.y

print poly.area()