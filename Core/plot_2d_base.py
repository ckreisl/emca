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
