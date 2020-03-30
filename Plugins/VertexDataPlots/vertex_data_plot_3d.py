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
from Core.plot_3d_base import ScatterPlot3DBase
import numpy as np
import logging


class VertexDataPlot3D(ScatterPlot3DBase):

    def __init__(self, parent=None):
        ScatterPlot3DBase.__init__(self, None)
        self.parent = parent
        # overwrite pick event since we work on vertices not on paths
        self.highlighter.overwrite_pick_event(self.handle_pick)
        self.highlighter.enable_multi_selection(False)

    def handle_pick(self, event):
        ind = event.ind
        x, y, z = self.axes.lines[0].get_data_3d()

        path_idx = self.parent.current_path_index()
        x_index = x[ind[0]]

        tpl = (path_idx, x_index)
        self.parent.send_select_vertex(tpl)

    def select_vertex(self, tpl):
        try:
            line_ax1 = self.axes.lines[0]
        except IndexError as e:
            logging.error("No data available: {}".format(e))
            return None

        x_data, y_data, z_data = line_ax1.get_data_3d()
        idx = np.where(x_data == tpl[1])[0]

        self.highlighter.set_data_3d(x_data[idx], y_data[idx], z_data[idx])
        self.figure.canvas.draw_idle()

    def prepare_plot_data(self, values):
        x_list = [x[0] for x in values]
        points = [p[1] for p in values]

        y_list = []
        z_list = []

        for p in points:
            tpl = p[0]
            y_list.append(tpl[0])
            z_list.append(tpl[1])
        return x_list, y_list, z_list

    def plot(self, name, values, xmin=None, xmax=None):
        x, y, z = self.prepare_plot_data(values)
        self.plot_3d(x, y, z, init_highlighter=False)
        if xmin is not None and xmax is not None:
            self.axes.set_xlim(xmin, xmax)
        self.axes.set_title(name, color=self.color_dots)
        self.axes.set_xlabel('path depth', color=self.color_title)
        self.axes.set_ylabel('x', color=self.color_dots)
        self.axes.set_zlabel('y', color=self.color_dots)
        self.axes.set_xticks(x)
        self.highlighter, = self.axes.plot([], [], [], 'o', color='yellow')
        self.figure.canvas.draw_idle()
