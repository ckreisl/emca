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

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QSizePolicy
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D
import logging


class Plot3DCanvas(FigureCanvas):

    def __init__(self, parent=None):
        self._parent = parent
        self._fig = Figure((5, 4), dpi=100)

        FigureCanvas.__init__(self, self._fig)
        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

        self._ax1 = Axes3D(self._fig)
        # RGBA dark theme
        self._RGBA = '#31363b'
        self._fig.patch.set_facecolor(self._RGBA)

        # plot facecolor dark theme
        self._plot_facecolor = '#232629'
        self._ax1.set_facecolor(self._plot_facecolor)

        self._alpha = 0.7
        self._color = '#eff0f1'

        # self._ax1_highlight, = self._ax1.plot([], [], 'o', color='yellow')

        # self._fig.tight_layout()
        self._cid = self._fig.canvas.mpl_connect('pick_event', self.handle_pick)

    def apply_theme(self, theme):
        if theme == 'light':
            self._color = '#000000'
            self._RGBA = '#EFF0F1'
            self._plot_facecolor = '#EFF0F1'
        self._fig.patch.set_facecolor(self._RGBA)
        self._ax1.set_facecolor(self._plot_facecolor)
        self._ax1.tick_params(axis='x', colors=self._color)
        self._ax1.tick_params(axis='y', colors=self._color)
        for border in ['left', 'right', 'bottom', 'top']:
            self._ax1.spines[border].set_color(self._color)

    def resize_plot(self):
        #self._fig.tight_layout()
        self._fig.canvas.draw_idle()

    def handle_pick(self, event):
        # todo check if picking and highlighting with idx is possible in 3d plot
        pass

    def clear_plot(self):
        self._ax1.clear()

    def select_vertex(self, tpl):
        # todo check if picking and highlighting with idx is possible in 3d plot
        pass

    def plot(self, name, values, xmin=None, xmax=None):

        x_list = [x[0] for x in values]
        points = [p[1] for p in values]

        y_list = []
        z_list = []

        for p in points:
            tpl = p[0]
            y_list.append(tpl[0])
            z_list.append(tpl[1])

        self._ax1.plot(x_list, y_list, z_list, 'wo', picker=5, alpha=self._alpha)
        self._ax1.set_title(name)
        self._ax1.set_xlabel('path depth')
        self._ax1.set_ylabel('x', color=self._color)
        self._ax1.set_zlabel('y', color=self._color)
        self._ax1.set_xticks(x_list)
        self._ax1.set_xlim(xmin, xmax)

        #self._fig.tight_layout()
        self._fig.canvas.draw_idle()
