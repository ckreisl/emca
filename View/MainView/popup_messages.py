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

from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QMessageBox


class PopupMessages(QObject):

    """
        PopupMessages
        Handles all popup messages. Used to inform the user with popups about error messages.
    """

    def __init__(self, parent=None):
        QObject.__init__(self, parent=parent)
        self._parent = parent
        self._msgBox = QMessageBox()

    def server_connection_broke(self, msg):
        """
        Popup error message if the socket connection broke
        :param msg: string
        :return:
        """
        self._msgBox.setIcon(QMessageBox.Warning)
        self._msgBox.setWindowTitle("Connection Error")
        self._msgBox.setText("Server connection broke")
        self._msgBox.setInformativeText("Restart Server and reconnect client")
        self._msgBox.setDetailedText(msg)
        self._msgBox.exec_()

    def server_error(self, msg):
        """
        Popup error message if something went wrong with the server
        :param msg: string
        :return:
        """
        self._msgBox.setIcon(QMessageBox.Information)
        self._msgBox.setWindowTitle("Connection Error")
        self._msgBox.setText("Server error")
        self._msgBox.setInformativeText("Can not connect to server. Start server or check for right port and hostname.")
        self._msgBox.setDetailedText(msg)
        self._msgBox.exec_()

    def error_not_connected(self, msg):
        """
        Popup error message if no connection is esablished
        :param msg: string
        :return:
        """
        self._msgBox.setIcon(QMessageBox.Information)
        self._msgBox.setWindowTitle("Connection Error")
        self._msgBox.setText("Diconnected")
        self._msgBox.setInformativeText("You are currently not connected to any server")
        self._msgBox.setDetailedText(msg)
        self._msgBox.exec_()

    def error_no_sample_idx_set(self, msg):
        """
        Popup error message if no sample index was set on server side
        :param msg: string
        :return:
        """
        self._msgBox.setIcon(QMessageBox.Information)
        self._msgBox.setWindowTitle("Index error")
        self._msgBox.setText("Sample index error")
        self._msgBox.setInformativeText("Sample index was not set on server side")
        self._msgBox.setDetailedText(msg)
        self._msgBox.exec_()

    def error_no_depth_idx_set(self, msg):
        """
        Popup error message if no depth index was set on server side
        :param msg:
        :return:
        """
        self._msgBox.setIcon(QMessageBox.Information)
        self._msgBox.setWindowTitle("Index error")
        self._msgBox.setText("Path depth index error")
        self._msgBox.setInformativeText("Path depth index was not set on server side")
        self._msgBox.setDetailedText(msg)
        self._msgBox.exec_()

    def error_no_final_estimate_data(self, msg):
        """
        Popup error message if no final estimate data was set on server side
        :param msg:
        :return:
        """
        self._msgBox.setIcon(QMessageBox.Information)
        self._msgBox.setWindowTitle("Missing data")
        self._msgBox.setText("Missing final estimate values")
        self._msgBox.setInformativeText("No final estimate data available to run outlier detection")
        self._msgBox.setDetailedText(msg)
        self._msgBox.exec_()









