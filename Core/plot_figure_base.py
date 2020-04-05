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
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolBar
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtCore import Qt
import numpy as np
import logging

white = 'white'
params = {'ytick.color': white,
          'xtick.color': white,
          'axes.labelcolor': white,
          'axes.edgecolor': white}
plt.rcParams.update(params)


class FigureBase(FigureCanvas):

    def __init__(self, figure, axes):
        FigureCanvas.__init__(self, figure)
        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.RGBA = '#31363b'
        self.plot_facecolor = '#232629'
        self.figure.patch.set_facecolor(self.RGBA)
        self.axes = axes
        self.setFocusPolicy(Qt.ClickFocus)
        self.setFocus()

        if isinstance(self.axes, np.ndarray):
            for ax in self.axes:
                ax.set_facecolor(self.plot_facecolor)
        else:
            self.axes.set_facecolor(self.plot_facecolor)

        self.alpha_dots = 0.7
        self.color_dots = '#eff0f1'
        self.color_title = 'white'
        self.color_axes = 'white'

    def create_navigation_toolbar(self, parent=None):
        return NavigationToolBar(self, parent)

    def resize_plot(self):
        self.figure.tight_layout()
        self.figure.canvas.draw_idle()

    def apply_theme(self, theme):
        if theme == 'light':
            self.RGBA = '#EFF0F1'
            self.plot_facecolor = '#EFF0F1'
            self.color_axes = 'black'
            self.color_title = 'black'
            self.color_dots = 'blue'
        else:
            self.RGBA = '#31363b'
            self.plot_facecolor = '#232629'
            self.color_axes = 'white'
            self.color_title = 'white'
            self.color_dots = '#eff0f1'
        self.figure.patch.set_facecolor(self.RGBA)
        if isinstance(self.axes, np.ndarray):
            for ax in self.axes:
                ax.set_facecolor(self.plot_facecolor)
                ax.tick_params(axis='x', colors=self.color_axes)
                ax.tick_params(axis='y', colors=self.color_axes)
                for spine in ['left', 'right', 'bottom', 'top']:
                    ax.spines[spine].set_color(self.color_axes)
        else:
            self.axes.set_facecolor(self.plot_facecolor)
            self.axes.tick_params(axis='x', colors=self.color_axes)
            self.axes.tick_params(axis='y', colors=self.color_axes)
            for spine in ['left', 'right', 'bottom', 'top']:
                self.axes.spines[spine].set_color(self.color_axes)
        self.figure.canvas.draw_idle()

    def clear(self):
        if isinstance(self.axes, np.ndarray):
            for ax in self.axes:
                ax.clear()
        else:
            self.axes.clear()
        self.figure.canvas.draw_idle()
