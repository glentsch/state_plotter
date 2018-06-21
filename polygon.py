import numpy as np
from numba import jit
from point import Point
from container import Container

class PolygonContainer(Container):
    def contains(self, config, point):
        config.polygons = filter(lambda x: x.contains(point), config.polygons)

class Polygon:
    def __init__(self, name=None, vertices=[]):
        self.vertices = vertices
        self.name = name 

    @property
    def x(self):
        return [x.x for x in self.vertices]

    @property
    def y(self):
        return [x.y for x in self.vertices]
    
    def _on_segment(self, point, segp1, segp2):
        segx = [segp1.x, segp2.x]
        segy = [segp1.y, segp2.y]
        return (point.x <= np.amax(segx)) and (point.x >= np.amin(segx)) \
            and (point.y <= np.amax(segy)) and (point.y >= np.amin(segy))
    @jit
    def _orientation(self, p, q, r):
        val = (q.y - p.y) * (r.x - q.x) - (q.x - p.x) * (r.y - q.y)
        if val == 0:
            return 0
        return 1 if val > 0 else 2
    @jit
    def _do_intersect(self, seg1p1, seg1p2, seg2p1, seg2p2):
        o1 = self._orientation(seg1p1, seg1p2, seg2p1)
        o2 = self._orientation(seg1p1, seg1p2, seg2p2)
        o3 = self._orientation(seg2p1, seg2p2, seg1p1)
        o4 = self._orientation(seg2p1, seg2p2, seg1p2)
        if(o1 != o2) and (o3 != o4):
            return True
        if (o1 == 0) and (self._on_segment(seg2p1, seg1p1, seg1p2)):
            return True
        if (o2 == 0) and (self._on_segment(seg2p2, seg1p1, seg1p2)):
            return True
        if (o3 == 0) and (self._on_segment(seg1p1, seg2p1, seg2p2)):
            return True
        if (o4 == 0) and (self._on_segment(seg1p2, seg2p1, seg2p2)):
            return True
        return False
    @jit
    def contains(self, point):
        n = len(self.vertices)
        inf = 10000
        if n < 3:
            return False
        extreme = Point(inf, point.y)
        count = 0
        i = 0
        while True:
            next = (i+1) % n
            if self._do_intersect(self.vertices[i], self.vertices[next], point, extreme):
                if self._orientation(self.vertices[i], point, self.vertices[next]) == 0:
                    return self._on_segment(point, self.vertices[i], self.vertices[next])
                count += 1
            i = next
            if i == 0:
                break
        return count & 1

        
            
