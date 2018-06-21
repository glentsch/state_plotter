from region_find import Region_Find
from point import Point


rf = Region_Find('states.json')
print rf.find(Point(-121.036133, 40.513799))
