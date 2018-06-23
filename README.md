# state_plotter
Find the region (state) from a state

Requires Python 2.7. It is untested on Python 3.x

To use:
```
from region_find import Region_Find
from point import Point

rf = Region_Find(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'states.json'))
states = rf.find(Point(longitude, latitude))
```

Currently, the states.json is expected to be in an improper json format, for a specific use, such as
```
{"state": "Washington", "border": [[-122.402015, 48.225216], [-117.032049, 48.999931], [-116.919132, 45.995175], [-124.079107, 46.267259], [-124.717175, 48.377557], [-122.92315, 47.047963], [-122.402015, 48.225216]]}
{"state": "Montana", "border": [[-111.475425, 44.702162], [-114.560924, 45.54874], [-116.063531, 48.99995], [-104.062991, 49.000026], [-104.043072, 44.997805], [-111.475425, 44.702162]]}
...
```

Each line is a region with a border.

the find function will return a list of regions (can be used for countries, states, counties,...)
