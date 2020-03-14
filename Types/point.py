"""
    This file is part of EMCA, an explorer of Monte-Carlo based Algorithms.
    Copyright (c) 2019-2020 by Christoph Kreisl and others.
    EMCA is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License Version 3
    as published by the Free Software Foundation.
    EMCA is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
    GNU General Public License for more details.
    You should have received a copy of the GNU General Public License
    along with this program. If not, see <http://www.gnu.org/licenses/>.
"""

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
