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
from PyQt5.Qt import Qt
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QApplication
import logging


class ViewOptions(QWidget):

    """
        ViewOptions
        Handles options of EMCA
    """

    def __init__(self, parent=None):
        QWidget.__init__(self, parent=None)
        uic.loadUi('View/ui/options.ui', self)

        self._controller = None

        # center widget depending on screen size
        desktop_widget = QApplication.desktop()
        screen_rect = desktop_widget.availableGeometry(self)
        self.move(screen_rect.center() - self.rect().center())

        self.cbDarkTheme.stateChanged.connect(self.handle_dark_theme_change)
        self.cbLightTheme.stateChanged.connect(self.handle_light_theme_change)
        self.btnSave.clicked.connect(self.btn_save)
        self.btnClose.clicked.connect(self.btn_close)

    def set_controller(self, controller):
        """
        Set the connection to the controller
        :param controller: Controller
        :return:
        """
        self._controller = controller

    def enable_dark_theme(self, enabled):
        self.cbDarkTheme.setChecked(enabled)

    def enable_light_theme(self, enabled):
        self.cbLightTheme.setChecked(enabled)

    def get_theme(self):
        theme = 'dark'
        if self.cbDarkTheme.isChecked():
            theme = 'dark'
        elif self.cbLightTheme.isChecked():
            theme = 'light'
        return theme

    def get_auto_connect(self):
        return self.cbAutoConnect.isChecked()

    def get_auto_scene_load(self):
        return self.cbAutoSceneLoad.isChecked()

    def get_auto_image_load(self):
        return self.cbAutoLoadImage.isChecked()

    def set_auto_connect(self, enabled):
        self.cbAutoConnect.setChecked(enabled)

    def set_auto_scene_load(self, enabled):
        self.cbAutoSceneLoad.setChecked(enabled)

    def set_auto_image_load(self, enabled):
        self.cbAutoLoadImage.setChecked(enabled)

    @pyqtSlot(int, name='handle_dark_theme_change')
    def handle_dark_theme_change(self, state):
        self.cbDarkTheme.blockSignals(True)
        if state == Qt.Checked:
            self.cbLightTheme.blockSignals(True)
            if self.cbLightTheme.isChecked():
                self.cbLightTheme.setChecked(False)
            self.cbLightTheme.blockSignals(False)
        elif state == Qt.Unchecked:
            self.cbLightTheme.blockSignals(True)
            if not self.cbLightTheme.isChecked():
                self.cbLightTheme.setChecked(True)
            self.cbLightTheme.blockSignals(False)
        self.cbDarkTheme.blockSignals(False)

    @pyqtSlot(int, name='handle_light_theme_change')
    def handle_light_theme_change(self, state):
        self.cbLightTheme.blockSignals(True)
        if state == Qt.Checked:
            self.cbDarkTheme.blockSignals(True)
            if self.cbDarkTheme.isChecked():
                self.cbDarkTheme.setChecked(False)
            self.cbDarkTheme.blockSignals(False)
        elif state == Qt.Unchecked:
            self.cbDarkTheme.blockSignals(True)
            if not self.cbDarkTheme.isChecked():
                self.cbDarkTheme.setChecked(True)
            self.cbDarkTheme.blockSignals(False)
        self.cbLightTheme.blockSignals(False)

    @pyqtSlot(bool, name='btn_save')
    def btn_save(self, clicked):
        options_dict = {'theme': self.get_theme(),
                        'auto_connect': self.get_auto_connect(),
                        'auto_scene_load': self.get_auto_scene_load(),
                        'auto_rendered_image_load': self.get_auto_image_load()}
        self._controller.save_options(options_dict)

    @pyqtSlot(bool, name='btn_close')
    def btn_close(self, clicked):
        self.close()


