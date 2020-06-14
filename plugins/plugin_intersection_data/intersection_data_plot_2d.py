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

from core.plot_2d_base import ScatterPlot2DBase
import numpy as np
import logging


class IntersectionDataPlot2D(ScatterPlot2DBase):

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
        except IndexError:
            return

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
