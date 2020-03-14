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

from PyQt5 import uic
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import pyqtSlot
from PyQt5.Qt import Qt


class ViewRenderInfo(QWidget):

    """
        ViewRenderInfo
        Handles general information about the scene
    """

    def __init__(self, parent=None):
        QWidget.__init__(self, parent=None)
        uic.loadUi('View/ui/render_info.ui', self)

        self._controller = None

        # center widget depending on screen size
        desktop_widget = QApplication.desktop()
        screen_rect = desktop_widget.availableGeometry(self)
        self.move(screen_rect.center() - self.rect().center())

        self.btnSubmit.clicked.connect(self.btn_submit)
        self.sbSampleCount.valueChanged.connect(self.sb_update_sample_count)

    def set_controller(self, controller):
        """
        Sets the connection to the controller
        :param controller: Controller
        :return:
        """
        self._controller = controller

    def update_render_info(self, render_info):
        """
        Updates the view info with new render information
        :param render_info: RenderInfo from model
        :return:
        """
        self.labelSceneName.setText(render_info.scene_name)
        self.labelOutputName.setText(render_info.output_filepath)
        self.labelExtensionName.setText(render_info.file_extension)
        self.sbSampleCount.setValue(render_info.sample_count)

    def keyPressEvent(self, event):
        """
        Handles key press event, if enter is pressed the submit button will be triggered
        :param event:
        :return:
        """
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            self.btn_submit(True)

    @pyqtSlot(bool, name='btn_submit')
    def btn_submit(self, clicked):
        """
        Informs the controller to submit render info and inform the server
        :param clicked:
        :return:
        """
        self._controller.send_render_info()

    @pyqtSlot(int, name='sb_update_sample_count')
    def sb_update_sample_count(self, value):
        """
        Informs the controller to update the sample count of render info
        :param value: integer
        :return:
        """
        self._controller.update_render_info_sample_count(value)

