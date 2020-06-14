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

from core.plugin import Plugin

from core.pyside2_uic import loadUi
from PySide2.QtWidgets import QVBoxLayout
from PySide2.QtWidgets import QListWidgetItem
from PySide2.QtCore import Slot
from PySide2.QtCore import Qt
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolBar

from plugins.plugin_intersection_data.hist_list_item import HistListItem
from plugins.plugin_intersection_data.intersection_data_plot_2d import IntersectionDataPlot2D
from plugins.plugin_intersection_data.intersection_data_plot_3d import IntersectionDataPlot3D
from plugins.plugin_intersection_data.intersection_data_plot_rgb import IntersectionDataPlotRGB
import os
import logging


class PathListItem(QListWidgetItem):

    def __init__(self, idx, name, layout):
        super().__init__(name, layout)
        self._idx = idx

    @property
    def idx(self):
        return self._idx


class IntersectionData(Plugin):

    def __init__(self):
        Plugin.__init__(
            self,
            name='IntersectionData',
            flag=27)
        ui_filepath = os.path.abspath(os.path.join(os.path.dirname(__file__), 'ui', 'plugin_plots.ui'))
        loadUi(ui_filepath, self)

        self._vertex_data_plot_2d = IntersectionDataPlot2D(self)
        self._vertex_data_plot_3d = IntersectionDataPlot3D(self)
        self._vertex_data_plot_rgb = IntersectionDataPlotRGB(self)
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

    @Slot(QListWidgetItem, name='apply_path_index_update')
    def apply_path_index_update(self, item):
        self.send_select_path(item.idx)

    @Slot(QListWidgetItem, name='update_hist_path')
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
