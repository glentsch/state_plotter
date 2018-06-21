class Point(object):
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y
    def __getitem__(self, name):
        return self.__dict__[name]
        