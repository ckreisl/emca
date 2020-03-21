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

from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QFrame
from PyQt5.QtCore import pyqtSlot
import logging


class PluginsViewContainer(QWidget):

    """
        PluginsViewContainer
        QtWidget that inserts the plugin widget.
        Represents a container with Request and Close button to request plugin data or close the window
        Besides holds the Plugin button which is used to open the Plugin view.
    """

    def __init__(self, plugin):
        QWidget.__init__(self)

        self.setWindowTitle("Plugin {}".format(plugin.name))

        self._controller = None
        self._plugin = plugin
        self._plugin.send_select_path = self.send_select_path
        self._plugin.send_select_vertex = self.send_select_vertex
        self._plugin.send_update_path_indices = self.send_update_path_indices
        self._btn = QPushButton(plugin.name)
        self._btn.setEnabled(False)
        self._btn.clicked.connect(self.display_plugin)

        self._btn_request = QPushButton("Request")
        self._btn_request.setEnabled(False)
        self._btn_request.clicked.connect(self.request_plugin)

        self._btn_close = QPushButton("Close")
        self._btn_close.clicked.connect(self.close)

        layout = QVBoxLayout(self)
        layout.addWidget(self._plugin)

        hline = QFrame()
        hline.setFrameShape(QFrame.HLine)
        hline.setFrameShadow(QFrame.Sunken)
        layout.addWidget(hline)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self._btn_request)
        btn_layout.addWidget(self._btn_close)
        layout.addLayout(btn_layout)

    @property
    def plugin(self):
        """
        Returns the Plugin
        :return:
        """
        return self._plugin

    def send_update_path_indices(self, indices, add_item):
        """
        Calls the controller update_path function.
        Update the path indices of all views
        :param indices: np.array[(path_index,...)]
        :param add_item: true or false
        :return:
        """
        self._controller.update_path(indices, add_item)

    def send_select_path(self, index):
        """
        Calls the controller select_path function.
        Updates the current selected path
        :param index: path_index
        :return:
        """
        self._controller.select_path(index=index)

    def send_select_vertex(self, tpl):
        """
        Calls the controller select_vertex function.
        Updates the current selected vertex
        :param tpl: (path_index, vertex_index)
        :return:
        """
        self._controller.select_vertex(tpl=tpl)

    def select_path(self, index):
        """
        Calls the Plugin select_path function
        Informs the Plugin about the current selected path
        :param index: path_index
        :return:
        """
        self._plugin.select_path(index)

    def select_vertex(self, tpl):
        """
        Calls the Plugin select_vertex function.
        Informs the Plugin about the current selected vertex
        :param tpl: (path_index, vertex_index)
        :return:
        """
        self._plugin.select_vertex(tpl)
        #automatically request new data for the selected vertex if the tool is visible
        if self.isVisible():
            self._controller.request_plugin(self._plugin.flag)

    def serialize(self, stream):
        """
        Calls the Plugin serialize function.
        Data from the Plugin will be send to the server.
        :param stream:
        :return:
        """
        self._plugin.serialize(stream)

    def get_plugin_btn(self):
        """
        Returns the Plugin QButton
        Used to visualize Plugin button with name within view
        :return:
        """
        return self._btn

    def enable_plugin_btn(self, enable):
        """
        Enables or disables the Plugin button
        :param enable: true or false
        :return:
        """
        self._btn.setEnabled(enable)
        self._btn_request.setEnabled(enable)

    def set_controller(self, controller):
        """
        Set the controller
        :param controller:
        :return:
        """
        self._controller = controller

    def init_render_data(self, render_data):
        """
        Calls the Plugin init_render_data function.
        Render data will be set within Plugins,
        to provide them with the current render data set from the selected pixel
        :param render_data:
        :return:
        """
        self._plugin.init_render_data(render_data)

    def prepare_new_data(self):
        """
        Calls the Plugin prepare_new_data function.
        Is called if a new pixel is selected in order to gather new pixel information
        :return:
        """
        self._plugin.prepare_new_data()

    def update_path_indices(self, indices):
        """
        Calls the Plugin update_path_indices function.
        Informs the Plugin about all selected paths
        :param indices: np.array[(path_index),...]
        :return:
        """
        self._plugin.update_path_indices(indices)

    def update_vertex_indices(self, tpl_list):
        """
        Calls the Plugin update_vertex_indices function.
        Informs the Plugin about all selected vertices
        :param tpl_list: [(path_index, vertex_index),...]
        :return:
        """
        self._plugin.update_vertex_indices(tpl_list)

    def update_view(self):
        """
        Calls the Plugin update_view function.
        This function is called after the deserialize function of the Plugin is finished
        :return:
        """
        self._plugin.update_view()

    @pyqtSlot(bool, name='request_plugin')
    def request_plugin(self, clicked):
        """
        Calls the controller request_tool function.
        If the Request button within the tool view is clicked,
        a request with the tool_id will be send to the server.
        :param clicked:
        :return:
        """
        self._controller.request_plugin(self._plugin.flag)

    @pyqtSlot(bool, name='display_tool')
    def display_plugin(self, clicked):
        """
        Opens and displays the tool window,
        if the view is already opened but in not active in the background,
        this functions sets the tool window back active and brings it to the foreground.
        :param clicked:
        :return:
        """
        if self.isVisible():
            self.activateWindow()
        else:
            self.show()
            self._controller.request_plugin(self._plugin.flag)
