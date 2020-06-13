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
from plugins.plugin_path_depth.plot_path_depth import PlotPathDepth
from PySide2.QtWidgets import QVBoxLayout


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
