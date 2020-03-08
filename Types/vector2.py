from Types.vector import Vec
import numpy as np


class Vec2f(Vec):

    """
        Vec2f
        Represents a vec2 float class
    """

    def __init__(self, x=0, y=0):
        super(Vec2f, self).__init__(np.array([x, y], dtype=np.float32))
        self._x = float(x)
        self._y = float(y)

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, new_x):
        self._x = float(new_x)
        self.data[0] = self._x

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, new_y):
        self._y = float(new_y)
        self.data[1] = self._y

    def to_string(self):
        return '[{1:.{0}f}, {2:.{0}f}]'.format(self.decimals,
                                               self._x,
                                               self._y)

    def __str__(self):
        return '[{}, {}]'.format(self._x, self._y)


class Vec2i(Vec):

    """
        Vec2i
        Represents a vec2 integer class
    """

    def __init__(self, x, y):
        self._x = int(x)
        self._y = int(y)
        super(Vec2i, self).__init__(np.array([x, y], dtype=np.int32))

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, new_x):
        self._x = int(new_x)
        self.data[0] = self._x

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, new_y):
        self._y = int(new_y)
        self.data[1] = self._y

    def to_string(self):
        return '[{}, {}]'.format(self._x, self._y)

    def __str__(self):
        return '[{1:.{0}f}, {2:.{0}f}]'.format(self.decimals,
                                               self._x,
                                               self._y)
