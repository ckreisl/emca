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
import abc


class Color(object):

    """
        Color
        Represents the base class of the color type classes
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
        if isinstance(other, Color):
            return Color(self.data + other.data)
        return Color(self.data + other)

    def __radd__(self, other):
        return Color(other + self.data)

    def __sub__(self, other):
        if isinstance(other, Color):
            return Color(self.data - other.data)
        return Color(self.data - other)

    def __rsub__(self, other):
        return Color(other - self.data)

    def __mul__(self, other):
        if isinstance(other, Color):
            return Color(self.data * other.data)
        return Color(self.data * other)

    def __rmul__(self, other):
        return Color(other * self.data)

    def __truediv__(self, other):
        if isinstance(other, Color):
            return Color(self.data / other.data)
        return Color(self.data / other)

    def __rdiv__(self, other):
        return Color(other / self.data)

    def __neg__(self):
        return Color(-self.data)

    def __pos__(self):
        return Color(+self.data)

    def __eq__(self, other):
        return np.array_equal(self.data, other.data)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return self.__str__()
