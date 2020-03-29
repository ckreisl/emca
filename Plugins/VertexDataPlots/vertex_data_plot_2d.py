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
import logging


class VertexDataPlot2D(ScatterPlot2DBase):

    def __init__(self, parent=None):
        ScatterPlot2DBase.__init__(self, None)
        self.parent = parent
        # overwrite pick event since we work on vertices not on paths
        self.highlighter.overwrite_pick_event(self.handle_pick)
        self.highlighter.enable_multi_selection(False)
        self.figure.tight_layout()

    def handle_pick(self, event):
        ind = event.ind
        line_ax1 = self.axes.lines[0]

        path_idx = self.parent.current_path_index()
        x_data_ax1 = line_ax1.get_xdata()

        tpl = (path_idx, x_data_ax1[ind[0]])
        self.parent.send_select_vertex(tpl)

    def select_vertex(self, tpl):
        try:
            line_ax1 = self.axes.lines[0]
        except IndexError as e:
            logging.error("No data available: {}".format(e))
            return None
        x_data_ax1 = line_ax1.get_xdata()
        y_data_ax1 = line_ax1.get_ydata()

        idx = np.where(x_data_ax1 == tpl[1])[0]

        self.highlighter.set_data(x_data_ax1[idx], y_data_ax1[idx])
        self.figure.canvas.draw_idle()

    def plot(self, name, values, xmin=None, xmax=None):

        x_list = [x[0] for x in values]
        y_list = [y[1] for y in values]

        self.plot_2d(x_list, y_list, init_highlighter=False)
        if xmin is not None and xmax is not None:
            self.axes.set_xlim(xmin, xmax)
        self.axes.set_xticks(x_list)
        self.axes.set_title(name, color=self.color_title)
        self.axes.set_ylabel(name, color=self.color_title)
        self.axes.set_xlabel('path depth', color=self.color_title)

        self.highlighter, = self.axes.plot([], [], 'o', color='yellow')

        self.figure.tight_layout()
        self.figure.canvas.draw_idle()
