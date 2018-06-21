import numpy as np
from container import Container
class Bounding_Box(Container):
    def get_min_max(self, polygons, axis):
        axis_points = [[x[axis] for x in a.vertices] for a in polygons]
        minimums = np.array([np.amin(x) for x in axis_points])
        maximums = np.array([np.amax(x) for x in axis_points])
        return (minimums, maximums)
    def _contains_axis(self, point, axis, minimums, maximums):
        return np.where((point[axis] >= minimums) & (point[axis] <= maximums))
    def contains(self, config, point):
        axis_dict = {'x': (config.x_min, config.x_max), 'y':(config.y_min, config.y_max)}
        axis = []
        for k,v in axis_dict.iteritems():
            axis.append(self._contains_axis(point, k, *axis_dict[k]))
        config.polygons = [config.polygons[i] for i in np.intersect1d(*axis)]

    
