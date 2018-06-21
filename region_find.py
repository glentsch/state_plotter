import os
import json
from polygon import PolygonContainer
from boundingbox import Bounding_Box
from point import Point
import copy
import configfile
from threading import Lock
try:
    import cPickle as pickle
except ImportError:
    import pickle

class Region_Find(object):
    def __init__(self, config_file=None):
        f = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'config', 'conf.pkl')
        config = None
        if not os.path.exists(f):
            if not config_file or not os.path.exists(config_file):
                f = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'config', 'states.json')
                if not os.path.exists(f):
                    raise IOError("No configuration file can be found")
            else:
                f = config_file
        self.config_gen = self._gen_config(f)
        self.containers = [Bounding_Box(), PolygonContainer()]
        self.lock = Lock()
    
    def find(self, point):
        with self.lock:
            config = copy.deepcopy(self.config_gen)
        for container in self.containers:
            container.contains(config, point)
        return config.polygons

    def _gen_config(self, file):
        cf_dict = {'.pkl':'PickledConfigFile', '.json':'JsonConfigFile'}
        _,extension = os.path.splitext(file)
        if extension in cf_dict:
            c = configfile.ConfigFileFactory.create_config(cf_dict[extension])
            c.generate(file)
            return c
        return NotImplementedError("This configuration: {} cannot be parsed, at present only support for {} exist".format(file, ",".join(cf_dict.keys())))
