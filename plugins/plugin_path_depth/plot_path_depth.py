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

from core.plot_2d_base import ScatterPlot2DBase
import numpy as np


class PlotPathDepth(ScatterPlot2DBase):

    def __init__(self, callback=None):
        ScatterPlot2DBase.__init__(self, callback)

    def select_path(self, index):
        self.highlighter.update(np.array([index]))

    def mark_values(self, indices):
        self.highlighter.update(indices)

    def plot(self, x_list, y_list):
        self.plot_2d(x_list, y_list)
        self.axes.set_ylabel('path depth', color=self.color_title)
        self.axes.set_xlabel('paths', color=self.color_title)
        self.figure.tight_layout()
