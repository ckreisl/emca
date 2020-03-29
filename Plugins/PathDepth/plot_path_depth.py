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

from Core.plot_2d_base import ScatterPlot2DBase
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
