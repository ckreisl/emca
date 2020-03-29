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
from Plugins.PathDepth.plot_path_depth import PlotPathDepth
from PyQt5.QtWidgets import QVBoxLayout


class PathDepth(Plugin):

    def __init__(self):
        Plugin.__init__(
            self,
            name='Path Depth',
            flag=28)

        self.plot_path_depth = PlotPathDepth(self.send_update_path_indices_callback)

        layout = QVBoxLayout(self)
        layout.addWidget(self.plot_path_depth)
        layout.addWidget(self.plot_path_depth.create_navigation_toolbar(self))

    def send_update_path_indices_callback(self, indices, add_item):
        self.send_update_path_indices(indices, add_item)

    def apply_theme(self, theme):
        self.plot_path_depth.apply_theme(theme)

    def init_render_data(self, render_data):
        x_list = []
        y_list = []
        for path_key, path in render_data.dict_paths.items():
            x_list.append(path_key)
            y_list.append(path.path_depth)

        self.plot_path_depth.plot(x_list, y_list)

    def prepare_new_data(self):
        self.plot_path_depth.clear()

    def update_path_indices(self, indices):
        self.plot_path_depth.mark_values(indices)

    def select_path(self, index):
        self.plot_path_depth.select_path(index)

    def update_vertex_indices(self, tpl_list):
        # nothing to-do here
        pass

    def select_vertex(self, tpl):
        # nothing to-do here
        pass

    def serialize(self, stream):
        # nothing to-do here since we work directly on render data
        pass

    def update_view(self):
        # nothing to-do here since we work directly on render data
        pass

    def deserialize(self, stream):
        # nothing to-do here since we work directly on render data
        pass

    def update_data(self):
        # nothing to-do here since we work directly on render data
        pass
