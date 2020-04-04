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

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QAction
from PyQt5.QtCore import pyqtSlot
from View.MainView.view_emca import ViewEMCA
from View.MainView.popup_messages import PopupMessages
from View.MainView.view_options import ViewOptions


class MainView(QMainWindow):

    """
        MainView
        Represents the MainView of EMCA
    """

    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent=parent)

        # center widget depending on screen size
        desktop_widget = QApplication.desktop()
        screen_rect = desktop_widget.availableGeometry(self)
        self.move(screen_rect.center() - self.rect().center())

        # Main view of EMCA, holding all subviews
        self._view_emca = ViewEMCA(parent=self)
        # Popup view handling error messages
        self._view_popup = PopupMessages(parent=self)
        self.setCentralWidget(self._view_emca)
        self.setWindowTitle('Explorer of Monte-Carlo based Algorithms (EMCA)')
        # Accept drops for Drag n drop events
        self.setAcceptDrops(True)

        self.add_menu_bar()

        self._controller = None

    def add_menu_bar(self):
        """
        Initialises and adds all menu items to the menu
        :return:
        """

        options = QAction('Options', self)
        options.setShortcut('Ctrl+S')
        options.setToolTip('Options')
        options.triggered.connect(self.open_options)

        load_image = QAction('Load image', self)
        load_image.setShortcut('Ctrl+O')
        load_image.setToolTip('Load .exr')
        load_image.triggered.connect(self.load_image_dialog)

        exit_action = QAction("Quit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.setToolTip("Closes the Application")
        exit_action.triggered.connect(self.close)

        """ 
            Remove buggy and not full implemented functions
            Screenshot is buggy since the vtk renderer view will stay transparent
        """
        """
        save_xml = QAction("Save State", self)
        save_xml.setShortcut("Ctrl+S")
        save_xml.setToolTip("Saves all information about current pixel")
        save_xml.triggered.connect(self.save_xml)

        load_xml = QAction("Load State", self)
        load_xml.setShortcut("Ctrl+L")
        load_xml.setToolTip("Load xml file with saved state")
        load_xml.triggered.connect(self.load_xml)

        screenshot = QAction("Screenshot", self)
        screenshot.setShortcut("F5")
        screenshot.setToolTip("Takes a Screenshot of the whole view")
        screenshot.triggered.connect(self.take_screenshot)
        """

        main_menu = self.menuBar()
        main_menu.setNativeMenuBar(False)
        menu = main_menu.addMenu("&Menu")
        menu.addAction(load_image)
        menu.addAction(options)
        # Remove buggy and not fully implemented functions
        #menu.addAction(load_xml)
        #menu.addAction(save_xml)
        #menu.addAction(screenshot)
        menu.addAction(exit_action)

    def set_controller(self, controller):
        """
        Set the connection to the controller
        :param controller:
        :return:
        """
        self._controller = controller
        self._view_emca.set_controller(controller)

    def closeEvent(self, q_close_event):
        """
        Handle the close event. Controller will be informed
        :param q_close_event:
        :return:
        """
        self._controller.close_app()

    def enable_filter(self, enable):
        """
        Depending on enable, the filter button and its view will be enabled
        :param enable: boolean
        :return:
        """
        self._view_emca.btnFilter.setEnabled(enable)

    @pyqtSlot(bool, name='open_options')
    def open_options(self, clicked):
        """
        Opens the options window
        :param clicked: boolean
        :return:
        """
        self._controller.open_options(clicked)

    @pyqtSlot(bool, name='load_image_dialog')
    def load_image_dialog(self, clicked):
        """
        Opens the dialog to load a file
        :param clicked: boolean
        :return:
        """
        self._controller.load_image_dialog(clicked)

    @pyqtSlot(bool, name='save_xml')
    def save_xml(self, clicked):
        """
        Opens the dialog to save the render data within a xml file
        :param clicked: boolean
        :return:
        """
        self._controller.save_xml(clicked)

    @pyqtSlot(bool, name='load_xml')
    def load_xml(self, clicked):
        """
        Opens the dialog to load a xml file with a stored render state
        :param clicked: boolean
        :return:
        """
        self._controller.load_xml(clicked)

    @pyqtSlot(bool, name='take_screenshot')
    def take_screenshot(self, clicked):
        """
        Takes a screenshow of the whole EMCA widget
        :param clicked: boolean
        :return:
        """
        self._controller.take_screenshot(self.centralWidget())

    @property
    def controller(self):
        """
        Returns the controller
        :return: Controller
        """
        return self._controller

    @property
    def view_emca(self):
        """
        Returns the view widget of EMCA
        :return: QWidget
        """
        return self._view_emca

    @property
    def view_popup(self):
        """
        Returns the view handling the popup messages
        :return: QObject
        """
        return self._view_popup

    @property
    def view_render_info(self):
        """
        Returns the view handling the render info
        :return: QWidget
        """
        return self._view_emca.view_render_info

    @property
    def view_plot(self):
        """
        Returns the view handling the final estimate view
        :return: QWidget
        """
        return self._view_emca.view_plot

    @property
    def view_connect(self):
        """
        Returns the view handling the connect settings
        :return: QWidget
        """
        return self._view_emca.view_connect

    @property
    def view_filter(self):
        """
        Returns the view handling the filter
        :return: QWidget
        """
        return self._view_emca.view_filter

    @property
    def view_render_image(self):
        """
        Returns the view handling the rendered image
        :return: QWidget
        """
        return self._view_emca.view_render_image

    @property
    def view_render_scene(self):
        """
        Returns the view handling the 3D viewer
        :return: QWidget
        """
        return self._view_emca.view_render_scene

    @property
    def view_render_scene_options(self):
        """
        Returns the view handling the scene options
        :return: QWidget
        """
        return self._view_emca.view_render_scene_options

    @property
    def view_render_data(self):
        """
        Returns the view handling the render data
        :return: QWidget
        """
        return self._view_emca.view_render_data

    @property
    def view_detector(self):
        """
        Returns the view handling the detector
        :return: QWidget
        """
        return self._view_emca.view_detector

    @property
    def view_options(self):
        """
        Returns the view handling the options
        :return: QWidget
        """
        return self._view_emca.view_options

