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
from Core.plot_rgb_base import RGBScatterPlotBase
import numpy as np


class VertexDataPlotRGB(RGBScatterPlotBase):

    def __init__(self, parent=None):
        RGBScatterPlotBase.__init__(self, None)
        self.parent = parent
        self.figure.tight_layout()
        self.highlighter.enable_multi_selection(False)
        self.highlighter.overwrite_pick_event(self.handle_pick)

    def handle_pick(self, event):
        ind = event.ind
        line_ax1 = self.axes[0].lines[0]

        path_idx = self.parent.current_path_index()
        x_data_ax1 = line_ax1.get_xdata()

        tpl = (path_idx, x_data_ax1[ind[0]])
        self.parent.send_select_vertex(tpl)

    def select_vertex(self, tpl):
        line_ax1 = self.axes[0].lines[0]
        line_ax2 = self.axes[1].lines[0]
        line_ax3 = self.axes[2].lines[0]

        y_data_ax1 = line_ax1.get_ydata()
        y_data_ax2 = line_ax2.get_ydata()
        y_data_ax3 = line_ax3.get_ydata()

        x_data_ax1 = line_ax1.get_xdata()
        idx = np.where(x_data_ax1 == tpl[1])[0]

        self._ax1_highlight.set_data(x_data_ax1[idx], y_data_ax1[idx])
        self._ax2_highlight.set_data(x_data_ax1[idx], y_data_ax2[idx])
        self._ax3_highlight.set_data(x_data_ax1[idx], y_data_ax3[idx])
        self.figure.canvas.draw_idle()

    def plot(self, name, values, xmin=None, xmax=None):

        x_list = [x[0] for x in values]
        points = [p[1] for p in values]

        red_list = []
        green_list = []
        blue_list = []

        for p in points:
            tpl = p[0]
            red_list.append(tpl[0])
            green_list.append(tpl[1])
            blue_list.append(tpl[2])

        self.plot_rgb(x_list, red_list, green_list, blue_list, init_highlighter=False)
        for ax in self.axes:
            ax.set_xlabel('path depth', color=self.color_title)
            ax.set_xticks(x_list)
            ax.set_xlim(xmin, xmax)

        self._ax1_highlight, = self.axes[0].plot([], [], 'o', color='yellow')
        self._ax2_highlight, = self.axes[1].plot([], [], 'o', color='yellow')
        self._ax3_highlight, = self.axes[2].plot([], [], 'o', color='yellow')

        self.figure.tight_layout()
        self.figure.canvas.draw_idle()
