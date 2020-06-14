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

from plugins.plugins_view_container import PluginsViewContainer
import plugins


class PluginsHandler(object):

    """
        PluginsHandler
        Initialises and handles all custom plugins.
        Plugins will be loaded if there are imported and added in Plugins/__init__.py (__add__)
    """

    def __init__(self):

        # plugins dict { unique_tool_id : plugin, ... }
        self._plugins_view_container = {}

        # loads and initialises all tools
        for plugin in [(name, cls()) for name, cls in plugins.__dict__.items() if isinstance(cls, type)]:
            self._plugins_view_container[plugin[1].flag] = PluginsViewContainer(plugin[1])

    def set_controller(self, controller):
        """
        Sets the controller to all loaded plugins
        :param controller:
        :return:
        """
        for _, value in self._plugins_view_container.items():
            value.set_controller(controller)

    def set_scene_renderer(self, renderer):
        """
        Sets the renderer reference to all registered plugins
        """
        for _, value in self._plugins_view_container.items():
            value.set_scene_renderer(renderer)

    def apply_theme(self, theme):
        for _, value in self._plugins_view_container.items():
            value.plugin.apply_theme(theme)

    def enable_plugins(self, enable):
        """
        Calls the tool container enable_tool_btn function.
        Enables the view Plugin button item
        :param enable:
        :return:
        """
        for _, value in self._plugins_view_container.items():
            value.enable_plugin_btn(enable)

    def request_plugin(self, flag, stream):
        """
        Calls the Tool Container
        :param flag: unique_tool_id
        :param stream: socket stream
        :return:
        """
        plugins_view_container = self._plugins_view_container.get(flag, None)
        if plugins_view_container:
            plugins_view_container.serialize(stream)

    def init_data(self, render_data):
        """
        Calls Tool Container init_render_data function.
        All plugins will be informed about a new render data package
        :param render_data:
        :return:
        """
        for _, value in self._plugins_view_container.items():
            value.init_render_data(render_data)

    def prepare_new_data(self):
        """
        Calls the Tool Container prepare_new_data function.
        Informs all plugins that a new render data package is requested
        :return:
        """
        for _, value in self._plugins_view_container.items():
            value.prepare_new_data()

    def update_path_indices(self, indices):
        """
        Calls the Tool Container update_path_indices function.
        Informs all plugins about selected path index/indices
        :param indices: np.array[path_index,...]
        :return:
        """
        for _, value in self._plugins_view_container.items():
            value.update_path_indices(indices)

    def update_vertex_indices(self, tpl_list):
        """
        Calls the Tool Container update_vertex_indices function.
        Informs all plugins about selected vertices
        :param tpl_list: [(path_index, vertex_index),...]
        :return:
        """
        for _, value in self._plugins_view_container.items():
            value.update_vertex_indices(tpl_list)

    def select_path(self, index):
        """
        Calls the Tool Container select_path function.
        Updates all tool views with the current selected path
        :param index: path_index
        :return:
        """
        for _, value in self._plugins_view_container.items():
            value.select_path(index)

    def select_intersection(self, tpl):
        """
        Calls the Plugin Container select_intersection function.
        Updates all tool views with the current selected vertex
        :param tpl: (path_index, vertex_index)
        :return:
        """
        for _, value in self._plugins_view_container.items():
            value.select_intersection(tpl)

    def get_plugin_by_flag(self, flag):
        """
        Returns the corresponding tool given the flag (unique_tool_id),
        if no tool was found None is returned
        :param flag: unique_tool_id
        :return: tool or None
        """
        plugins_view_container = self._plugins_view_container.get(flag, None)
        if plugins_view_container:
            return plugins_view_container.plugin
        return None

    def close(self):
        """
        Closes all Tool windows
        :return:
        """
        for _, plugin in self._plugins_view_container.items():
            plugin.close()

    @property
    def plugins(self):
        """
        Returns the Plugins View Container dictionary {unique_tool_id : PluginsViewContainer, ...}
        :return:
        """
        return self._plugins_view_container



