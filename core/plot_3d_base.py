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
from core.plot_figure_base import FigureBase
from core.plot_3d_highlighter import Highlighter3D
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import logging


class ScatterPlot3DBase(FigureBase):

    def __init__(self, callback):
        figure = plt.figure(figsize=(5, 4))
        axes = figure.add_subplot(111, projection='3d')
        FigureBase.__init__(self, figure, axes)
        self.highlighter = Highlighter3D(figure, axes, callback)
        # set axes here - must be created for mouse rotation
        self.axes = Axes3D(self.figure)
        # theme has to be set again
        self.apply_theme('dark')

    def resize_plot(self):
        # overwrite function to avoid figure.tight_layout() call
        pass

    def plot_3d(self, x, y, z, init_highlighter=True):
        self.axes.plot(x, y, z, 'o', color=self.color_dots, picker=5, alpha=self.alpha_dots)
        if init_highlighter:
            self.highlighter.init_data(x=np.array(x), y=np.array(y), z=np.array(y))
        self.figure.canvas.draw_idle()
