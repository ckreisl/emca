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


