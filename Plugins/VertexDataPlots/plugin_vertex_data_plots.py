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

from Core.plugin import Plugin

from PyQt5 import uic
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QListWidgetItem
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolBar

from Plugins.VertexDataPlots.hist_list_item import HistListItem
from Plugins.VertexDataPlots.vertex_data_plot_2d import VertexDataPlot2D
from Plugins.VertexDataPlots.vertex_data_plot_3d import VertexDataPlot3D
from Plugins.VertexDataPlots.vertex_data_plot_rgb import VertexDataPlotRGB
import logging


class PathListItem(QListWidgetItem):

    def __init__(self, idx, name, layout):
        super().__init__(name, layout)
        self._idx = idx

    @property
    def idx(self):
        return self._idx


class VertexDataPlots(Plugin):

    def __init__(self):
        Plugin.__init__(
            self,
            name='Vertex Data Plots',
            flag=27)
        uic.loadUi('Plugins/VertexDataPlots/ui/plugin_plots.ui', self)

        self._vertex_data_plot_2d = VertexDataPlot2D(self)
        self._vertex_data_plot_3d = VertexDataPlot3D(self)
        self._vertex_data_plot_rgb = VertexDataPlotRGB(self)
        self._plots = [self._vertex_data_plot_2d,
                       self._vertex_data_plot_3d,
                       self._vertex_data_plot_rgb]
        self._render_data = None
        self._cur_path_tpl = None
        self._last_hist_item = ""

        layout_2d = QVBoxLayout(self.hist2D)
        layout_2d.addWidget(self._vertex_data_plot_2d)
        layout_2d.addWidget(self._vertex_data_plot_2d.create_navigation_toolbar(self.hist2D))

        layout_3d = QVBoxLayout(self.hist3D)
        layout_3d.addWidget(self._vertex_data_plot_3d)
        layout_3d.addWidget(NavigationToolBar(self._vertex_data_plot_3d, self.hist3D))

        layout_color = QVBoxLayout(self.histColor)
        layout_color.addWidget(self._vertex_data_plot_rgb)
        layout_color.addWidget(self._vertex_data_plot_rgb.create_navigation_toolbar(self.histColor))

        self.listPaths.itemClicked.connect(self.apply_path_index_update)
        self.listPaths.currentItemChanged.connect(self.update_hist_path)
        self.listHistNames.currentRowChanged.connect(self.update_hist)

    def current_path_index(self):
        if self.listPaths.count() > 0:
            item = self.listPaths.currentItem()
            return item.idx
        return -1

    def resizeEvent(self, event):
        for plot in self._plots:
            plot.resize_plot()
        super().resizeEvent(event)

    def apply_theme(self, theme):
        for plot in self._plots:
            plot.apply_theme(theme)

    def init_render_data(self, render_data):
        self._render_data = render_data

    def prepare_new_data(self):
        self._cur_path_tpl = None
        self._last_hist_item = ""
        self.clear_plots()
        self.listPaths.clear()
        self.listHistNames.clear()

    def update_path_indices(self, indices):
        self.prepare_new_data()
        for i in indices:
            PathListItem(i, 'Path ({})'.format(i), self.listPaths)

    def update_vertex_indices(self, tpl_list):
        pass

    def select_path(self, index):
        items = self.listPaths.findItems('Path ({})'.format(index), Qt.MatchCaseSensitive)
        if items:
            self.listPaths.setCurrentItem(items[0])

    def select_vertex(self, tpl):
        if self._render_data:
            self._cur_path_tpl = tpl
            stacked_idx = self.stackedHists.currentIndex()
            if stacked_idx == 0:
                self._vertex_data_plot_2d.select_vertex(tpl)
            elif stacked_idx == 1:
                self._vertex_data_plot_3d.select_vertex(tpl)
            elif stacked_idx == 2:
                self._vertex_data_plot_rgb.select_vertex(tpl)

    @pyqtSlot(QListWidgetItem, name='apply_path_index_update')
    def apply_path_index_update(self, item):
        self.send_select_path(item.idx)

    @pyqtSlot(QListWidgetItem, name='update_hist_path')
    def update_hist_path(self, item):
        self.listHistNames.clear()
        if not item:
            return
        paths = self._render_data.dict_paths
        path_data = paths.get(item.idx, None)

        if path_data:
            vertex_dict = path_data.dict_vertices
            plot_2d_dict = {}
            plot_3d_dict = {}
            plot_color_dict = {}
            for vertex_idx, vertex in vertex_dict.items():
                self.insert_plot_data(vertex.dict_bool, plot_2d_dict, vertex_idx)
                self.insert_plot_data(vertex.dict_float, plot_2d_dict, vertex_idx)
                self.insert_plot_data(vertex.dict_double, plot_2d_dict, vertex_idx)
                self.insert_plot_data(vertex.dict_int, plot_2d_dict, vertex_idx)
                self.insert_plot_data(vertex.dict_point2i, plot_3d_dict, vertex_idx)
                self.insert_plot_data(vertex.dict_point2f, plot_3d_dict, vertex_idx)
                self.insert_plot_data(vertex.dict_color3f, plot_color_dict, vertex_idx)

            for name in plot_2d_dict:
                HistListItem(name, self.listHistNames, plot_2d_dict, 0.75, path_data.path_depth+0.25, self._vertex_data_plot_2d, 0)

            for name in plot_3d_dict:
                HistListItem(name, self.listHistNames, plot_3d_dict, 0.75, path_data.path_depth+0.25, self._vertex_data_plot_3d, 1)

            for name in plot_color_dict:
                HistListItem(name, self.listHistNames, plot_color_dict, 0.75, path_data.path_depth+0.25, self._vertex_data_plot_rgb, 2)

            if self._last_hist_item == "":
                self.listHistNames.setCurrentRow(0)
            else:
                self.clear_plots()
                items_list = self.listHistNames.findItems(self._last_hist_item, Qt.MatchCaseSensitive)
                if len(items_list) > 0:
                    item = items_list[0]
                    if self.stackedHists.currentIndex() != item.widget_idx:
                        self.stackedHists.setCurrentIndex(item.widget_idx)
                    item.setSelected(True)
                    item.plot_canvas.plot(item.name, item.plot_data[item.name], item.xmin, item.xmax)
                else:
                    self.listHistNames.setCurrentRow(0)

    def update_hist(self, row_idx):
        self.clear_plots()

        item = self.listHistNames.item(row_idx)
        if not item:
            return None

        self._last_hist_item = item.name

        if self.stackedHists.currentIndex() != item.widget_idx:
            self.stackedHists.setCurrentIndex(item.widget_idx)

        item.setSelected(True)
        item.plot_canvas.plot(item.name, item.plot_data[item.name], item.xmin, item.xmax)

        if self._cur_path_tpl:
            item.plot_canvas.select_vertex(self._cur_path_tpl)

    def clear_plots(self):
        for plot in self._plots:
            plot.clear()

    @staticmethod
    def insert_plot_data(source_dict, target_dict, vertex_idx):
        for name, value in source_dict.items():
            if target_dict.get(name, None):
                target_dict[name].append((vertex_idx, value))
            else:
                target_dict[name] = [(vertex_idx, value)]

    def serialize(self, stream):
        # nothing to-do here since we work directly on render data
        pass

    def deserialize(self, stream):
        # nothing to-do here since we work directly on render data
        pass

    def update_view(self):
        # nothing to-do here since we work directly on render data
        pass
