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


class ToolContainer(QWidget):

    """
        ToolContainer
        QtWidget that inserts the tool widget.
        Represents a container with Request and Close button to request tool data or close the window
        Besides holds the Tool button which is used to open the tool view.
    """

    def __init__(self, tool):
        QWidget.__init__(self)

        self.setWindowTitle("Tool {}".format(tool.name))

        self._controller = None
        self._tool = tool
        self._tool.send_select_path = self.send_select_path
        self._tool.send_select_vertex = self.send_select_vertex
        self._tool.send_update_path_indices = self.send_update_path_indices
        self._btn = QPushButton(tool.name)
        self._btn.setEnabled(False)
        self._btn.clicked.connect(self.display_tool)

        self._btn_request = QPushButton("Request")
        self._btn_request.setEnabled(False)
        self._btn_request.clicked.connect(self.request_tool)

        self._btn_close = QPushButton("Close")
        self._btn_close.clicked.connect(self.close)

        layout = QVBoxLayout(self)
        layout.addWidget(self._tool)

        hline = QFrame()
        hline.setFrameShape(QFrame.HLine)
        hline.setFrameShadow(QFrame.Sunken)
        layout.addWidget(hline)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self._btn_request)
        btn_layout.addWidget(self._btn_close)
        layout.addLayout(btn_layout)

    @property
    def tool(self):
        """
        Returns the tool
        :return:
        """
        return self._tool

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
        Calls the tool select_path function
        Informs the tool about the current selected path
        :param index: path_index
        :return:
        """
        self._tool.select_path(index)

    def select_vertex(self, tpl):
        """
        Calls the tool select_vertex function.
        Informs the tool about the current selected vertex
        :param tpl: (path_index, vertex_index)
        :return:
        """
        self._tool.select_vertex(tpl)
        #automatically request new data for the selected vertex if the tool is visible
        if self.isVisible():
            self._controller.request_tool(self._tool.flag)

    def serialize(self, stream):
        """
        Calls the tool serialize function.
        Data from the tool will be send to the server.
        :param stream:
        :return:
        """
        self._tool.serialize(stream)

    def get_tool_btn(self):
        """
        Returns the Tool QButton
        Used to visualize Tool button with name within view
        :return:
        """
        return self._btn

    def enable_tool_btn(self, enable):
        """
        Enables or disables the Tool button
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
        Calls the Tool init_render_data function.
        Render data will be set within tools,
        to provide them with the current render data set from the selected pixel
        :param render_data:
        :return:
        """
        self._tool.init_render_data(render_data)

    def prepare_new_data(self):
        """
        Calls the Tool prepare_new_data function.
        Is called if a new pixel is selected in order to gather new pixel information
        :return:
        """
        self._tool.prepare_new_data()

    def update_path_indices(self, indices):
        """
        Calls the Tool update_path_indices function.
        Informs the tool about all selected paths
        :param indices: np.array[(path_index),...]
        :return:
        """
        self._tool.update_path_indices(indices)

    def update_vertex_indices(self, tpl_list):
        """
        Calls the Tool update_vertex_indices function.
        Informs the tool about all selected vertices
        :param tpl_list: [(path_index, vertex_index),...]
        :return:
        """
        self._tool.update_vertex_indices(tpl_list)

    def update_view(self):
        """
        Calls the Tool update_view function.
        This function is called after the deserialize function of the tool is finished
        :return:
        """
        self._tool.update_view()

    @pyqtSlot(bool, name='request_tool')
    def request_tool(self, clicked):
        """
        Calls the controller request_tool function.
        If the Request button within the tool view is clicked,
        a request with the tool_id will be send to the server.
        :param clicked:
        :return:
        """
        self._controller.request_tool(self._tool.flag)

    @pyqtSlot(bool, name='display_tool')
    def display_tool(self, clicked):
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
            self._controller.request_tool(self._tool.flag)
