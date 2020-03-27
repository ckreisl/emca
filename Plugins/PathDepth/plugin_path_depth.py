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

from Plugins.PathDepth.plot_2d_canvas import PlotPathDepth
from Core.plugin import Plugin
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolBar

from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.Qt import Qt


class PathDepth(Plugin):

    def __init__(self):
        Plugin.__init__(
            self,
            name='Path Depth',
            flag=28
        )

        self._plot = PlotPathDepth(self.send_update_path_indices_callback)
        self._plot.setFocusPolicy(Qt.ClickFocus)
        self._plot.setFocus()

        layout = QVBoxLayout(self)
        layout.addWidget(self._plot)
        layout.addWidget(NavigationToolBar(self._plot, self))

    def send_update_path_indices_callback(self, indices, add_item):
        self.send_update_path_indices(indices, add_item)

    def apply_theme(self, theme):
        self._plot.apply_theme(theme)

    def init_render_data(self, render_data):
        x_list = []
        y_list = []
        for path_key, path in render_data.dict_paths.items():
            x_list.append(path_key)
            y_list.append(path.path_depth)

        self._plot.plot(x_list, y_list)

    def prepare_new_data(self):
        self._plot.clear_plot()

    def update_path_indices(self, indices):
        self._plot.mark_values(indices)

    def select_path(self, index):
        self._plot.select_path(index)

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
