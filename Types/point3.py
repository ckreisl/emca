from Types.point import Point
from Types.vector3 import Vec3f
import numpy as np


class Point3f(Point):

    """
        Point3f
        Represents a point3 float class
    """

    def __init__(self, x=0, y=0, z=0):
        super(Point3f, self).__init__(np.array([x, y, z], dtype=np.float32))
        self._x = float(x)
        self._y = float(y)
        self._z = float(z)

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

    @property
    def z(self):
        return self._z

    @z.setter
    def z(self, new_z):
        self._z = float(new_z)
        self.data[2] = self._z

    def dir_to(self, dest):
        if dest is None:
            return None
        dir_vec = np.array([dest.x, dest.y, dest.z])-np.array([self.x, self.y, self.z])
        dir_vec_norm = dir_vec/np.linalg.norm(dir_vec)
        return Vec3f(dir_vec_norm[0], dir_vec_norm[1], dir_vec_norm[2])

    def to_string(self):
        return '[{}, {}, {}]'.format(self._x, self._y, self._z)

    def __str__(self):
        return '[{1:.{0}f}, {2:.{0}f}, {3:.{0}f}]'.format(self.decimals,
                                                          self._x,
                                                          self._y,
                                                          self._z)


class Point3i(Point):

    """
        Point3i
        Represents point3 integer class
    """

    def __init__(self, x=0, y=0, z=0):
        super(Point3i, self).__init__(np.array([x, y, z], dtype=np.int32))
        self._x = int(x)
        self._y = int(y)
        self._z = int(z)

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

    @property
    def z(self):
        return self._z

    @z.setter
    def z(self, new_z):
        self._z = int(new_z)
        self.data[2] = self._z

    def to_string(self):
        return '[{}, {}, {}]'.format(self._x, self._y, self._z)

    def __str__(self):
        return '[{1:.{0}f}, {2:.{0}f}, {3:.{0}f}]'.format(self.decimals,
                                                          self._x,
                                                          self._y,
                                                          self._z)
