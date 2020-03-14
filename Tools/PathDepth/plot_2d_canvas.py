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

from Tools.PathDepth.highlighter import Highlighter
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QSizePolicy
import matplotlib.pyplot as plt
import numpy as np
import logging


class PlotPathDepth(FigureCanvas):

    def __init__(self, callback=None):
        self._callback = callback
        self._fig, self._axes = plt.subplots(figsize=(5, 5), nrows=1)

        FigureCanvas.__init__(self, self._fig)
        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

        self._highlighter = Highlighter(self._fig, self._axes, callback)
        self._fig.tight_layout()

    def resize_plot(self):
        self._fig.tight_layout()
        self._fig.canvas.draw_idle()

    def select_path(self, index):
        self._highlighter.update(np.array([index]))

    def mark_values(self, indices):
        self._highlighter.update(indices)

    def clear_plot(self):
        self._axes.clear()

    def plot(self, x_list, y_list):
        self._axes.plot(x_list, y_list, 'bo', picker=5)
        self._axes.set_ylabel('path depth')
        self._axes.set_xlabel('paths')
        self._highlighter.init_dataset(np.array(x_list),
                                       np.array(y_list))
        self._fig.canvas.draw_idle()
        self._fig.tight_layout()
