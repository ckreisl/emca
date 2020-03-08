import numpy as np
import abc


class Point(object):

    """
        Point
        Base class for all point classes
    """

    def __init__(self, data):
        self.data = data
        self.decimals = 2

    @property
    def digits(self):
        return self.decimals

    @digits.setter
    def digits(self, new_digits):
        self.decimals = new_digits

    @abc.abstractmethod
    def to_string(self):
        pass

    def __add__(self, other):
        if isinstance(other, Point):
            return Point(self.data + other.data)
        return Point(self.data + other)

    def __radd__(self, other):
        return Point(other + self.data)

    def __sub__(self, other):
        if isinstance(other, Point):
            return Point(self.data - other.data)
        return Point(self.data - other)

    def __rsub__(self, other):
        return Point(other - self.data)

    def __mul__(self, other):
        if isinstance(other, Point):
            return Point(self.data * other.data)
        return Point(self.data * other)

    def __rmul__(self, other):
        return Point(other * self.data)

    def __truediv__(self, other):
        if isinstance(other, Point):
            return Point(self.data / other.data)
        return Point(self.data / other)

    def __rdiv__(self, other):
        return Point(other / self.data)

    def __neg__(self):
        return Point(-self.data)

    def __pos__(self):
        return Point(+self.data)

    def __eq__(self, other):
        return np.array_equal(self.data, other.data)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return self.__str__()

    def __getitem__(self, item):
        return self.data[item]
