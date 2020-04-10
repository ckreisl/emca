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

        self.sbSampleCount.valueChanged.connect(self.sb_update_sample_count)
        self.btnSubmit.clicked.connect(self.btn_submit)
        self.btnClose.clicked.connect(self.btn_close)

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

    @pyqtSlot(int, name='sb_update_sample_count')
    def sb_update_sample_count(self, value):
        """
        Informs the controller to update the sample count of render info
        :param value: integer
        :return:
        """
        self._controller.update_render_info_sample_count(value)

    @pyqtSlot(bool, name='btn_submit')
    def btn_submit(self, clicked):
        """
        Informs the controller to submit render info and inform the server
        :param clicked:
        :return:
        """
        self._controller.send_render_info()

    @pyqtSlot(bool, name='btn_close')
    def btn_close(self, clicked):
        self.close()

