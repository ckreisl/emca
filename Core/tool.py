from PyQt5.QtWidgets import QWidget
import abc


class Tool(QWidget):
    """
    Tool interface, inherites from QWidget

    The tool interface can be used to visualizes own generated data sets.
    It can request own data from the server interface or work on the current render data,
    to visualize other aspects which are not implemented yet.

    New tools are loaded via Tools/__init__.py,
    therefore import new tools there and add the class name to __all__ list.
    """

    def __init__(self, name, flag):
        QWidget.__init__(self, parent=None)
        self._name = name
        self._flag = flag

    @property
    def flag(self):
        """
        Returns the unique identifier of the tool
        :return: flag (unique identifier)
        """
        return self._flag

    @property
    def name(self):
        """
        Returns the name of the tool
        :return: tool name
        """
        return self._name

    def send_update_path_indices(self, indices, add_item):
        """
        This function gets overwritten by the tool container,
        which will connect this function with the controller
        :param indices: numpy array:
        :param add_item: bool, add values or not:
        :return:
        """

    def send_select_path(self, index):
        """
        This function gets overwritten by the tool container,
        which will connect this function with the controller
        :param index:
        :return:
        """
        pass

    def send_select_vertex(self, tpl):
        """
        This function gets overwritten by the tool container,
        which will connect this function with the controller
        :param tpl:
        :return:
        """
        pass

    @abc.abstractmethod
    def init_render_data(self, render_data):
        """
        Apply current pixel render data to tools
        :param render_data:
        :return:
        """
        pass

    @abc.abstractmethod
    def prepare_new_data(self):
        """
        Resets all views and prepares class for new incoming pixel data package
        :return:
        """
        pass

    @abc.abstractmethod
    def update_path_indices(self, indices):
        """
        Sends list of path indices to all views to update selected paths
        :param indices: Numpy array [(path_index),...]
        :return:
        """
        pass

    @abc.abstractmethod
    def update_vertex_indices(self, tpl_list):
        """
        Send update of multiple selected vertices as tuple list
        :param tpl_list: [(path_index, vertex_index), ...]
        :return:
        """
        pass

    @abc.abstractmethod
    def select_path(self, index):
        """
        Will be called if a path element is selected within the view
        :param index: path_idx
        :return:
        """
        pass

    @abc.abstractmethod
    def select_vertex(self, tpl):
        """
        Will be called if a vertex element is selected within the view
        :param tpl: (path_idx, vertex_idx)
        :return:
        """
        pass

    @abc.abstractmethod
    def serialize(self, stream):
        """
        Send data to server
        :param stream:
        :return:
        """
        pass

    @abc.abstractmethod
    def deserialize(self, stream):
        """
        Receive data from server
        Will be handled within an extra thread,
        therefor do not update Qt view elements within this function
        :param stream:
        :return:
        """
        pass

    @abc.abstractmethod
    def update_view(self):
        """
        This function will be called after deserialize is finished
        It will update all data within the view
        :return:
        """
