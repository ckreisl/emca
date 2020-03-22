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

from View.RenderView.hdr_graphics_view import HDRGraphicsView
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSlot
from PyQt5 import uic
import math
import logging


class ViewRenderImage(QWidget):

    """
        ViewRenderImage
        Handles the view of the rendered image and the interaction to select a specific pixel.
        The selected pixel and its corresponding position will be send to the controller,
        which will then send a request to the server.
    """

    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)
        uic.loadUi('View/ui/render_image.ui', self)

        # accept drops for drag n drop feature
        self.setAcceptDrops(True)

        self._value = 0.0
        self._controller = None
        # HDR graphics view handles .exr images
        self._graphics_view = HDRGraphicsView(self)

        # add graphics view
        self.layoutView.addWidget(self._graphics_view)

        # connect signals
        self.btnLoadImage.clicked.connect(self.load_image_dialog)
        self.btnReset.clicked.connect(self.reset)
        self.hsExposure.valueChanged.connect(self.set_spin_value)
        self.dsbExposure.valueChanged.connect(self.set_slider_value)

    @property
    def pixmap(self):
        """
        Returns the render image as QPixmap
        :return:
        """
        return self._graphics_view.pixmap

    @pyqtSlot(float, name='set_slider_value')
    def set_slider_value(self, value):
        """
        Sets the slider value of the exposure
        :param value: float
        :return:
        """
        # code from HDRiTools qt4Image
        len_slider = self.hsExposure.maximum() - self.hsExposure.minimum()
        len_spin = self.dsbExposure.maximum() - self.dsbExposure.minimum()
        ratio = (value - self.dsbExposure.minimum()) / len_spin
        new_value = int(math.floor((ratio * len_slider) + 0.5 + self.hsExposure.minimum()))
        self.hsExposure.setValue(new_value)
        self.update_exposure(float(value))

    @pyqtSlot(int, name='set_spin_value')
    def set_spin_value(self, value):
        """
        Sets the spin value of the exposure
        :param value: float
        :return:
        """
        # code from HDRiTools qt4Image
        len_slider = self.hsExposure.maximum() - self.hsExposure.minimum()
        len_spin = self.dsbExposure.maximum() - self.dsbExposure.minimum()
        ratio = (value - self.hsExposure.minimum()) / len_slider
        new_value = (ratio * len_spin) + self.dsbExposure.minimum()
        self.dsbExposure.setValue(new_value)

    def update_exposure(self, value):
        """
        Updates the exposure of the image
        :param value: float
        :return:
        """
        if value != self._value:
            self._value = value
            self._graphics_view.update_exposure(value)

    def set_controller(self, controller):
        """
        Sets the connection to the controller
        :param controller: Controller
        :return:
        """
        self._controller = controller

    def enable_view(self, enable):
        """
        Enables the view elements
        :param enable: boolean
        :return:
        """
        self.btnReset.setEnabled(enable)
        self.dsbExposure.setEnabled(enable)
        self.hsExposure.setEnabled(enable)

    def request_render_data(self, pixel):
        """
        Informs the controller about the selected pixel
        :param pixel: tuple(x,y)
        :return:
        """
        self._controller.request_render_data(pixel=pixel)

    def load_hdr_image(self, filepath):
        """
        Loads an exr image from the given filepath
        :param filepath: string
        :return:
        """
        return self._graphics_view.load_hdr_image(filepath)

    @pyqtSlot(bool, name='reset')
    def reset(self, clicked):
        """
        Resets the exposure settings, and fits the render image within the view
        :param clicked: boolean
        :return:
        """
        self._graphics_view.reset()
        self.hsExposure.setValue(0)

    @pyqtSlot(bool, name='load_image_dialog')
    def load_image_dialog(self, clicked):
        """
        Informs the controller to open a dialog to load an image from a given filepath
        :param clicked: boolean
        :return:
        """
        self._controller.load_image_dialog(clicked)
