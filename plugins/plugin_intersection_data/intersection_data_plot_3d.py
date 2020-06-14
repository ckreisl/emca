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

from core.plot_3d_base import ScatterPlot3DBase
import numpy as np
import logging


class IntersectionDataPlot3D(ScatterPlot3DBase):

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
        self.parent.send_select_intersection(tpl)

    def select_intersection(self, tpl):
        try:
            line_ax1 = self.axes.lines[0]
        except IndexError:
            return

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
        self.axes.set_title(name, color=self.color_title)
        self.axes.set_xlabel('path depth', color=self.color_title)
        self.axes.set_ylabel('x', color=self.color_title)
        self.axes.set_zlabel('y', color=self.color_title)
        self.axes.set_xticks(x)
        self.highlighter, = self.axes.plot([], [], [], 'o', color='yellow')
        self.figure.canvas.draw_idle()
