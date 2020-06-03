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

from Types.color import Color
import numpy as np


class Color3f(Color):

    """
        Color3f
        Represents a red, green, blue, alpha color class
    """

    def __init__(self, r=0, g=0, b=0, alpha=0):
        super(Color3f, self).__init__(np.array([r, g, b], dtype=np.float32))
        self._r = float(r)
        self._g = float(g)
        self._b = float(b)
        self._alpha = float(alpha)

    @property
    def red(self):
        return self._r

    @red.setter
    def red(self, new_red):
        self._r = float(new_red)
        self.data[0] = self._r

    @property
    def green(self):
        return self._g

    @green.setter
    def green(self, new_green):
        self._g = float(new_green)
        self.data[1] = self._g

    @property
    def blue(self):
        return self._b

    @blue.setter
    def blue(self, new_blue):
        self._b = float(new_blue)
        self.data[2] = self._b

    @property
    def alpha(self):
        return self._alpha

    @alpha.setter
    def alpha(self, new_alpha):
        self._alpha = new_alpha

    @property
    def mean(self):
        return (self._r + self._g + self._b) / 3.0

    def to_list(self):
        return [self._r, self._g, self._b, self._alpha]

    def to_list_rgb(self):
        return [self._r, self._g, self._b]

    def to_string(self):
        return '[{}, {}, {}, {}]'.format(self.data[0],
                                         self.data[1],
                                         self.data[2],
                                         self.alpha)

    def __str__(self):
        return '[{1:.{0}f}, {2:.{0}f}, {3:.{0}f}]'.format(self.decimals,
                                                          self.data[0],
                                                          self.data[1],
                                                          self.data[2])

    def __getitem__(self, item):
        if item == 3:
            return self._alpha
        return self.data[item]


