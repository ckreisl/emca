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

from Core.messages import ViewMode
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QStackedWidget
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QPixmap
from PyQt5 import uic

from View.MainView.view_options import ViewOptions
from View.MainView.view_connect_settings import ViewConnectSettings
from View.MainView.view_filter import ViewFilter
from View.MainView.view_detector_settings import ViewDetectorSettings
from View.MainView.view_render_info import ViewRenderInfo

from View.DataView.view_render_data import ViewRenderData
from View.SceneView.view_render_scene import ViewRenderScene
from View.RenderView.view_render_image import ViewRenderImage
from View.SampleContributionView.view_sample_contribution_plot import ViewScatterPlot

import logging


class ViewEMCA(QWidget):

    """
        EMCA Mainview
        Holding all sub-view items.
        Handling connection between the views and informs the controller about interactions.
    """

    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)
        uic.loadUi('View/ui/emca.ui', self)

        self.setAcceptDrops(True)

        # init views
        self._controller = None
        self._view_main = parent
        self._view_options = ViewOptions(parent=parent)
        self._view_connect = ViewConnectSettings(parent=parent)
        self._view_detector = ViewDetectorSettings(parent=parent)
        self._view_filter = ViewFilter(parent=parent)
        self._view_render_info = ViewRenderInfo(parent=parent)
        self._view_render_image = ViewRenderImage(parent=self)
        self._view_render_scene = ViewRenderScene(parent=self)
        self._view_plot = ViewScatterPlot(parent=self)
        self._view_render_data = ViewRenderData(parent=self)

        # stacked widget
        self._stacked_widget_left = QStackedWidget()
        self._stacked_widget_left.addWidget(self._view_render_image)
        self._stacked_widget_left.addWidget(self._view_render_scene)
        self.left.addWidget(self._stacked_widget_left)

        self._stacked_widget_right = QStackedWidget()
        self._stacked_widget_right.addWidget(self._view_plot)
        self._stacked_widget_right.addWidget(self._view_render_data)
        self.right.addWidget(self._stacked_widget_right)

        self._pixel_info = QPixmap(16, 16)

        # connect signals
        self.btnConnect.clicked.connect(self.open_connect_view)
        self.btnDetector.clicked.connect(self.open_detector_view)
        self.btnFilter.clicked.connect(self.open_filter_view)
        self.btnOptions.clicked.connect(self.open_render_info_view)
        self.btnRender.clicked.connect(self.request_render_image)
        self.btn2D3DView.clicked.connect(self.toggle_view_left)
        self.btnHistRenderDataView.clicked.connect(self.toggle_view_right)
        self.cbPixelHistory.currentIndexChanged.connect(self.request_history_pixel)

    def set_controller(self, controller):
        """
        Sets the connection to the controller
        :param controller: Controller
        :return:
        """
        self._controller = controller

    @pyqtSlot(bool, name='open_connect_view')
    def open_connect_view(self, clicked):
        """
        Opens the connect view, if the view is already open the window is set back to active
        :param clicked: boolean
        :return:
        """
        if self._view_connect.isVisible():
            self._view_connect.activateWindow()
        else:
            self._view_connect.show()

    @pyqtSlot(bool, name='open_detector_view')
    def open_detector_view(self, clicked):
        """
        Opens the detector view, if the view is already open the window is set back to active
        :param clicked: boolean
        :return:
        """
        if self._view_detector.isVisible():
            self._view_detector.activateWindow()
        else:
            self._view_detector.show()

    @pyqtSlot(bool, name='open_filter_view')
    def open_filter_view(self, clicked):
        """
        Opens the filter view, if the view is already open the window is set back to active
        :param clicked: boolean
        :return:
        """
        if self._view_filter.isVisible():
            self._view_filter.activateWindow()
        else:
            self._view_filter.show()

    @pyqtSlot(bool, name='open_render_info_view')
    def open_render_info_view(self, clicked):
        """
        Opens the render info view, if the view is already open the window is set back to active
        :param clicked:
        :return:
        """
        if self._view_render_info.isVisible():
            self._view_render_info.activateWindow()
        else:
            self._view_render_info.show()

    @pyqtSlot(bool, name='request_render_image')
    def request_render_image(self, clicked):
        """
        Informs the controller to request the render image from the server
        :param clicked: boolean
        :return:
        """
        self._controller.request_render_image()

    @pyqtSlot(bool, name='toggle_view_left')
    def toggle_view_left(self, clicked):
        """
        Toggles the two views on the left side 2D and 3D view via a stacked widget
        :param clicked: boolean
        :return:
        """
        idx = self._stacked_widget_left.currentIndex()
        if idx == 0:
            # change view to 2D
            self.btn2D3DView.setText('Render View')
            self._stacked_widget_left.setCurrentIndex(1)
        elif idx == 1:
            # change view to 3D
            self.btn2D3DView.setText('Scene View')
            self._stacked_widget_left.setCurrentIndex(0)

    @pyqtSlot(bool, name='toggle_view_right')
    def toggle_view_right(self, clicked):
        """
        Toggles the two views on the right side final estimate plot and render data via a stacked widget
        :param clicked:
        :return:
        """
        idx = self._stacked_widget_right.currentIndex()
        if idx == 0:
            # change view to render data
            self.btnHistRenderDataView.setText("Sample Contribution View")
            self._stacked_widget_right.setCurrentIndex(1)
        elif idx == 1:
            # change view to histogram
            self.btnHistRenderDataView.setText("Data View")
            self._stacked_widget_right.setCurrentIndex(0)

    @property
    def controller(self):
        """
        Returns the controller
        :return: Controller
        """
        return self._controller

    @property
    def view_main(self):
        """
        Returns the QMainView
        :return: QMainView
        """
        return self._view_main

    @property
    def view_connect(self):
        """
        Returns the connect view
        :return: QWidget
        """
        return self._view_connect

    @property
    def view_detector(self):
        """
        Returns the detector view
        :return: QWidget
        """
        return self._view_detector

    @property
    def view_filter(self):
        """
        Returns the filter view
        :return: QWidget
        """
        return self._view_filter

    @property
    def view_render_info(self):
        """
        Returns the render info view
        :return: QWidget
        """
        return self._view_render_info

    @property
    def view_render_image(self):
        """
        Returns the render image view
        :return: QWidget
        """
        return self._view_render_image

    @property
    def view_render_data(self):
        """
        Returns the render data view
        :return: QWidget
        """
        return self._view_render_data

    @property
    def view_plot(self):
        """
        Returns the final estimate plot view
        :return: QWidget
        """
        return self._view_plot

    @property
    def view_render_scene(self):
        """
        Returns the 3D render scene view
        :return: QWidget
        """
        return self._view_render_scene

    @property
    def view_options(self):
        """
        Returns the options widget
        :return: QWidget
        """
        return self._view_options

    def enable_view(self, enabled, mode=ViewMode.CONNECTED):
        """
        Enables view elements depending on enabled and ViewMode
        :param enabled: boolean
        :param mode: ViewMode
        :return:
        """
        if mode is ViewMode.CONNECTED:
            if enabled:
                self.btnConnect.setText('Disconnect')
                self.btnConnect.clicked.disconnect(self.open_connect_view)
                self.btnConnect.clicked.connect(self._controller.handle_disconnect)
            else:
                self.btnConnect.setText('Connect')
                self.btnConnect.clicked.disconnect(self._controller.handle_disconnect)
                self.btnConnect.clicked.connect(self.open_connect_view)
                self.btnFilter.setEnabled(enabled)

            self.btnRender.setEnabled(enabled)
            self.btnOptions.setEnabled(enabled)
            self.labelSelectedPixel.setEnabled(enabled)
            self.cbPixelHistory.setEnabled(enabled)
            self.btnDetector.setEnabled(enabled)
        elif mode is ViewMode.XML:
            self.labelSelectedPixel.setEnabled(enabled)
            self.cbPixelHistory.setEnabled(enabled)
            self.btnDetector.setEnabled(enabled)
            self.btnFilter.setEnabled(enabled)

    def add_plugins(self, plugins):
        """
        Adds the plugin buttons to the view
        :param plugins: dict{tool_id : PluginsViewContainer, ... }
        :return:
        """
        row = 0
        col = 0
        for flag, plugin in plugins.items():
            btn_plugin = plugin.get_plugin_btn()
            if col > 5:
                row = row + 1
            self.layoutPlugins.addWidget(btn_plugin, row, col)
            col = col + 1

    def update_pixel_hist(self, pixel_info):
        """
        Updates the pixel history
        :param pixel_info: PixelInfo
        :return:
        """
        self.cbPixelHistory.blockSignals(True)
        text = pixel_info.get_pixel_str()
        # check if item is already in list
        idx = self.cbPixelHistory.findText(text)
        if idx == -1:
            # item not found, insert new item
            if self.cbPixelHistory.count() > 6:
                self.cbPixelHistory.removeItem(0)
            self.cbPixelHistory.addItem(pixel_info.icon, text)
            idx = self.cbPixelHistory.count()-1
            self.cbPixelHistory.setCurrentIndex(idx)
        else:
            # item found, select its index
            self.cbPixelHistory.setCurrentIndex(idx)
        self.cbPixelHistory.blockSignals(False)

    @pyqtSlot(int, name='request_history_pixel')
    def request_history_pixel(self, index):
        """
        Informs the controller to request an old data set from the pixel history
        :param index: integer
        :return:
        """
        text = self.cbPixelHistory.itemText(index)
        text = text.strip('()')
        values = text.split(",")
        x, y = int(values[0]), int(values[1])
        logging.info('Request pixel=({},{})'.format(x, y))
        self._controller.request_render_data(QPoint(x, y))
