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
import numpy as np
import logging


class Plot2DCanvas(FigureCanvas):

    def __init__(self, parent=None):
        self._parent = parent
        self._fig = Figure((5, 4), dpi=100)
        self._ax1 = self._fig.add_subplot(111)

        # RGBA dark theme
        self._RGBA = '#31363b'
        self._fig.patch.set_facecolor(self._RGBA)

        # plot facecolor dark theme
        plot_facecolor = '#232629'
        self._ax1.set_facecolor(plot_facecolor)

        self._alpha = 0.7

        FigureCanvas.__init__(self, self._fig)
        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

        self._ax1_highlight, = self._ax1.plot([], [], 'o', color='yellow')

        self._fig.tight_layout()
        self._cid = self._fig.canvas.mpl_connect('pick_event', self.handle_pick)

    def resize_plot(self):
        self._fig.tight_layout()
        self._fig.canvas.draw_idle()

    def handle_pick(self, event):
        ind = event.ind
        line_ax1 = self._ax1.lines[0]

        path_idx = self._parent.current_path_index()
        x_data_ax1 = line_ax1.get_xdata()

        tpl = (path_idx, x_data_ax1[ind[0]])
        self._parent.send_select_vertex(tpl)

    def clear_plot(self):
        self._ax1.clear()

    def select_vertex(self, tpl):
        try:
            line_ax1 = self._ax1.lines[0]
        except IndexError as e:
            logging.error("No data available: {}".format(e))
            return None
        x_data_ax1 = line_ax1.get_xdata()
        y_data_ax1 = line_ax1.get_ydata()

        idx = np.where(x_data_ax1 == tpl[1])[0]

        self._ax1_highlight.set_data(x_data_ax1[idx], y_data_ax1[idx])
        self._fig.canvas.draw_idle()

    def plot(self, name, values, xmin=None, xmax=None):

        x_list = [x[0] for x in values]
        y_list = [y[1] for y in values]

        self._ax1.plot(x_list, y_list, 'wo', picker=5, alpha=self._alpha)
        self._ax1.set_xlim(xmin, xmax)
        self._ax1.set_xticks(x_list)
        self._ax1.set_title(name)
        self._ax1.set_ylabel(name)
        self._ax1.set_xlabel('path depth')

        self._ax1_highlight, = self._ax1.plot([], [], 'o', color='yellow')

        self._fig.tight_layout()
        self._fig.canvas.draw_idle()
