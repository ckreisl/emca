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

import matplotlib.pyplot as plt
import numpy as np
from Core.plot_figure_base import FigureBase
from Core.plot_2d_highlighter import Highlighter2D


class ScatterPlot2DBase(FigureBase):

    def __init__(self, callback):
        figure, axes = plt.subplots(figsize=(5, 5), nrows=1)
        FigureBase.__init__(self, figure, axes)
        self.highlighter = Highlighter2D(figure, axes, callback)
        self.figure.tight_layout()

    def plot_2d(self, x, y, init_highlighter=True):
        self.axes.plot(x, y, 'o', color=self.color_dots, picker=5, alpha=self.alpha_dots)
        if init_highlighter:
            self.highlighter.init_dataset(x=np.array(x), s1=np.array(y))
        self.figure.canvas.draw_idle()
