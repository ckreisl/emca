"""
    MIT License

    Copyright (c) 2020 Christoph Kreisl

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
"""

import numpy as np
import random
import abc


class Vec(object):

    """
        Vec
        Base class for all vector types
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
        if isinstance(other, Vec):
            return Vec(self.data + other.data)
        return Vec(self.data + other)

    def __radd__(self, other):
        return Vec(other + self.data)

    def __sub__(self, other):
        if isinstance(other, Vec):
            return Vec(self.data - other.data)
        return Vec(self.data - other)

    def __rsub__(self, other):
        return Vec(other - self.data)

    def __mul__(self, other):
        if isinstance(other, Vec):
            return Vec(self.data * other.data)
        return Vec(self.data * other)

    def __rmul__(self, other):
        return Vec(other * self.data)

    def __truediv__(self, other):
        if isinstance(other, Vec):
            return Vec(self.data / other.data)
        return Vec(self.data / other)

    def __rdiv__(self, other):
        return Vec(other / self.data)

    def __neg__(self):
        return Vec(-self.data)

    def __pos__(self):
        return Vec(+self.data)

    def __eq__(self, other):
        return np.array_equal(self.data, other.data)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        return self.square_length() < other.square_length()

    def __le__(self, other):
        return self.square_length() <= other.square_length()

    def __gt__(self, other):
        return self.square_length() > other.square_length()

    def __ge__(self, other):
        return self.square_length() >= other.square_length()

    def __repr__(self):
        return self.__str__()

    def __getitem__(self, item):
        return self.data[item]

    def ceil(self):
        return Vec(np.ceil(self.data))

    def floor(self):
        return Vec(np.floor(self.data))

    def get_data(self):
        return self.data

    def inverse(self):
        return Vec(1.0/self.data)

    def length(self):
        return float(np.linalg.norm(self.data))

    def normalize(self):
        length = self.length()
        if length == 0.0:
            return Vec(np.zeros(self.data.shape()))
        return Vec(self.data/length)

    def round(self, decimal=0):
        return Vec(np.round(self.data, decimal))

    def square_length(self):
        return float(np.sum(np.square(self.data)))

    @classmethod
    def distance(cls, a, b):
        c = b - a
        return c.length()

    @classmethod
    def dot(self, a, b):
        return Vec(np.dot(a.data, b.data))

    @classmethod
    def equals(cls, a, b, tolerance=0.0):
        diffs = np.fabs((a - b).data)
        pairs = zip(list(np.fabs(a.data)), list(np.fabs(b.data)))
        tolerance_calcs = [tolerance * max(1, a_val, b_val) for (a_val, b_val) in pairs]
        tests = [d <= t for (d, t) in zip(diffs, tolerance_calcs)]
        return all(tests)

    @classmethod
    def max_components(cls, a, b):
        return Vec(np.maximum(a.data, b.data))

    @classmethod
    def min_components(cls, a, b):
        return Vec(np.minimum(a.data, b.data))

    @classmethod
    def mix(cls, a, b, t):
        return a*(1-t) + b*t

    @classmethod
    def random(cls, n):
        x = random.random()
        y = random.random()
        return Vec(np.random.rand((n)))

    @classmethod
    def square_distance(cls, a, b):
        c = b - a
        return c.square_length()




