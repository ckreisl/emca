from Handler.tool_container import ToolContainer
import Tools
import logging


class ToolHandler(object):

    """
        ToolHandler
        Initialises and handles all custom tools.
        Tools will be loaded if there are imported and added in Tools/__init__.py (__add__)
    """

    def __init__(self):

        # tools dict { unique_tool_id : tool, ... }
        self._tool_container = {}

        # loads and initialises all tools
        for tool in [(name, cls()) for name, cls in Tools.__dict__.items() if isinstance(cls, type)]:
            self._tool_container[tool[1].flag] = ToolContainer(tool[1])

    def set_controller(self, controller):
        """
        Sets the controller to all loaded tools
        :param controller:
        :return:
        """
        for key, value in self._tool_container.items():
            value.set_controller(controller)

    def enable_tools(self, enable):
        """
        Calls the tool container enable_tool_btn function.
        Enables the view Tool button item
        :param enable:
        :return:
        """
        for key, value in self._tool_container.items():
            value.enable_tool_btn(enable)

    def request_tool(self, flag, stream):
        """
        Calls the Tool Container
        :param flag: unique_tool_id
        :param stream: socket stream
        :return:
        """
        tool_container = self._tool_container.get(flag, None)
        if tool_container:
            tool_container.serialize(stream)

    def init_data(self, render_data):
        """
        Calls Tool Container init_render_data function.
        All tools will be informed about a new render data package
        :param render_data:
        :return:
        """
        for key, value in self._tool_container.items():
            value.init_render_data(render_data)

    def prepare_new_data(self):
        """
        Calls the Tool Container prepare_new_data function.
        Informs all tools that a new render data package is requested
        :return:
        """
        for key, value in self._tool_container.items():
            value.prepare_new_data()

    def update_path_indices(self, indices):
        """
        Calls the Tool Container update_path_indices function.
        Informs all tools about selected path index/indices
        :param indices: np.array[path_index,...]
        :return:
        """
        for key, value in self._tool_container.items():
            value.update_path_indices(indices)

    def update_vertex_indices(self, tpl_list):
        """
        Calls the Tool Container update_vertex_indices function.
        Informs all tools about selected vertices
        :param tpl_list: [(path_index, vertex_index),...]
        :return:
        """
        for key, value in self._tool_container.items():
            value.update_vertex_indices(tpl_list)

    def select_path(self, index):
        """
        Calls the Tool Container select_path function.
        Updates all tool views with the current selected path
        :param index: path_index
        :return:
        """
        for key, value in self._tool_container.items():
            value.select_path(index)

    def select_vertex(self, tpl):
        """
        Calls the Tool Container select_vertex function.
        Updates all tool views with the current selected vertex
        :param tpl: (path_index, vertex_index)
        :return:
        """
        for key, value in self._tool_container.items():
            value.select_vertex(tpl)

    def get_tool_by_flag(self, flag):
        """
        Returns the corresponding tool given the flag (unique_tool_id),
        if no tool was found None is returned
        :param flag: unique_tool_id
        :return: tool or None
        """
        tool_container = self._tool_container.get(flag, None)
        if tool_container:
            return tool_container.tool
        return None

    def close(self):
        """
        Closes all Tool windows
        :return:
        """
        for key, tool in self._tool_container.items():
            tool.close()

    @property
    def tools(self):
        """
        Returns the Tools Container dictionary {unique_tool_id : ToolContainer, ...}
        :return:
        """
        return self._tool_container



