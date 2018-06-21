from __future__ import generators
import os
import json
try:
    import cPickle as pickle
except ImportError:
    import pickle
from point import Point
from polygon import Polygon
from boundingbox import Bounding_Box


class ConfigFileFactory:
    factories = {}
    def add_factory(id, config_factory):
        ConfigFileFactory.factories.put[id] = config_factory
    add_factory = staticmethod(add_factory)

    def create_config(id):
        if not ConfigFileFactory.factories.has_key(id):
            ConfigFileFactory.factories[id] = eval(id + '.Factory()')
        return ConfigFileFactory.factories[id].create()
    create_config = staticmethod(create_config)

class ConfigFile(object):
    def __init__(self):
        self.polygons = []
        self.x_min = -1
        self.x_max = 10000
        self.y_min = -1
        self.y_max = 10000
    def generate(self, f):
        raise NotImplementedError()

class PickledConfigFile(ConfigFile):
    class Factory:
        def create(self): return PickledConfigFile()
    def generate(self, f):
        if os.path.exists(f):
            with open(f, 'rb') as in_file:
                (self.polygons, self.x_min, self.x_max, self.y_min, self.y_max) = pickle.load(in_file)
        else:
            raise IOError("{} does not exist".format(f))

class JsonConfigFile(ConfigFile):
    class Factory:
        def create(self): return JsonConfigFile()
    def generate(self, f):
        polygons = []
        if os.path.exists(f):
            with open(f) as in_file:
                for line in in_file:
                    o = json.loads(line)
                    points = [Point(x[0], x[1]) for x in o['border']]
                    polygons.append(Polygon(o['state'], points))
            bb = Bounding_Box()
            (self.x_min, self.x_max) = bb.get_min_max(polygons, 'x')
            (self.y_min, self.y_max) = bb.get_min_max(polygons, 'y')
            self.polygons = polygons
            self._pickle_config_file(self.polygons, self.x_min, self.x_max, self.y_min, self.y_max)
        else:
            raise IOError("{} does not exist".format(f))
    def _pickle_config_file(self, polygons, x_min, x_max, y_min, y_max):
        with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'config', 'states.pkl'), 'wb') as out_file:
            pickle.dump((polygons, x_min, x_max, y_min, y_max), out_file)
            
    