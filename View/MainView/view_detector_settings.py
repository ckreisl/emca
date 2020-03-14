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
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QApplication
import logging


class ViewDetectorSettings(QWidget):

    """
        ViewDetectorSettings
        Handles the settings of the detector.
        The view will trigger the detector which will detect outliers based on the final estimate data.
    """

    def __init__(self, parent=None):
        QWidget.__init__(self, parent=None)
        uic.loadUi('View/ui/detector.ui', self)

        self._controller = None

        # center widget depending on screen size
        desktop_widget = QApplication.desktop()
        screen_rect = desktop_widget.availableGeometry(self)
        self.move(screen_rect.center() - self.rect().center())

        self.cb_default.clicked.connect(self.toggle_esd)
        self.cb_esd.clicked.connect(self.toggle_default)
        self.btn_apply.clicked.connect(self.apply)
        self.btn_apply_close.clicked.connect(self.apply_close)

    def set_controller(self, controller):
        """
        Sets the connection to the controller
        :param controller: Controller
        :return:
        """
        self._controller = controller

    def init_values(self, detector):
        """
        Initialise the values of the view from the detector
        :param detector:
        :return:
        """
        self.dsb_m.setValue(detector.m)
        self.dsb_alpha.setValue(detector.alpha)
        self.dsb_k.setValue(detector.k)
        self.dsb_pre_filter.setValue(detector.pre_filter)
        self.cb_default.setChecked(detector.is_default_active())

    @pyqtSlot(bool, name='toggle_esd')
    def toggle_esd(self, clicked):
        """
        Toggles the checkbox of the ESD detector, only one detector can be active
        :param clicked: boolean
        :return:
        """
        if self.cb_default.isChecked():
            self.cb_esd.setChecked(False)
        if not self.cb_default.isChecked() and not self.cb_esd.isChecked():
            self.cb_esd.setChecked(True)

    @pyqtSlot(bool, name='toggle_default')
    def toggle_default(self, clicked):
        """
        Toggles the checkbox of the default detector, only one detector can be active
        :param clicked: boolean
        :return:
        """
        if self.cb_esd.isChecked():
            self.cb_default.setChecked(False)
        if not self.cb_esd.isChecked() and not self.cb_default.isChecked():
            self.cb_default.setChecked(True)

    @pyqtSlot(bool, name='apply')
    def apply(self, clicked):
        """
        Informs the controller to apply the current detector settings
        :param clicked: boolean
        :return:
        """
        self._controller.update_and_run_detector(
            self.dsb_m.value(),
            self.dsb_alpha.value(),
            self.dsb_k.value(),
            self.dsb_pre_filter.value(),
            self.cb_default.isChecked(),
            self.cb_is_active.isChecked()
        )

    @pyqtSlot(bool, name='apply_close')
    def apply_close(self, clicked):
        """
        Applies the current detector by informing the controller and closes the view.
        :param clicked: boolean
        :return:
        """
        self.apply(clicked)
        self.close()

