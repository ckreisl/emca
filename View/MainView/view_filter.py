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
from PyQt5.QtWidgets import QFormLayout
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QListWidgetItem
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt

from Types.point2 import Point2f
from Types.point2 import Point2i
from Types.point3 import Point3f
from Types.point3 import Point3i
from Types.color3 import Color3f
from enum import Enum
import re
import logging


class FilterType(Enum):
    SINGLE_VALUE = 0
    POINT2 = 1
    POINT3 = 2
    COLOR3 = 3


class FilterListItem(QWidget):

    """
        FilterListItem
        Represents a filter list item holding information about the filter
    """

    def __init__(self, filter_settings):
        QWidget.__init__(self)

        self._idx = filter_settings.get_idx()

        layout = QFormLayout()
        d_type = filter_settings.get_type()
        constraint = filter_settings.get_constraint()
        text = filter_settings.get_text()

        if d_type is FilterType.SINGLE_VALUE:
            layout.addRow("SingleValue:", QLabel(text))
            layout.addRow("val: ", QLabel(str(constraint[0])))
        elif d_type is FilterType.POINT2:
            layout.addRow("Point2:", QLabel(""))
            layout.addRow("x: ", QLabel(str(constraint[0])))
            layout.addRow("y: ", QLabel(str(constraint[1])))
        elif d_type is FilterType.POINT3:
            layout.addRow("Point3:", QLabel(text))
            layout.addRow("x: ", QLabel(str(constraint[0])))
            layout.addRow("y: ", QLabel(str(constraint[1])))
            layout.addRow("z: ", QLabel(str(constraint[2])))
        elif d_type is FilterType.COLOR3:
            layout.addRow("Color3:", QLabel(text))
            layout.addRow("r: ", QLabel(str(constraint[0])))
            layout.addRow("g: ", QLabel(str(constraint[1])))
            layout.addRow("b: ", QLabel(str(constraint[2])))
        self.setLayout(layout)

    def get_idx(self):
        """
        Returns an index referencing the filter settings index
        :return: integer
        """
        return self._idx


class FilterSettings(object):

    """
        FilterSettings
        Representing a container holding information about a filter
    """

    def __init__(self, view):
        self._idx = view.filterList.count()
        self._text = view.combItems.currentText()

        idx = view.stackedWidget.currentIndex()

        if idx == 0:
            self._type = FilterType.SINGLE_VALUE
            self._constraint = (view.leExp.text(),)
        elif idx == 1:
            self._type = FilterType.POINT2
            self._constraint = (view.leExpX.text(),
                                view.leExpY.text(),
                                view.cbPoint2.isChecked())
        elif idx == 2:
            self._type = FilterType.POINT3
            self._constraint = (view.leExpX_2.text(),
                                view.leExpY_2.text(),
                                view.leExpZ.text(),
                                view.cbPoint3.isChecked())
        elif idx == 3:
            self._type = FilterType.COLOR3
            self._constraint = (view.leExpR.text(),
                                view.leExpG.text(),
                                view.leExpB.text(),
                                view.cbColor.isChecked())

    def get_idx(self):
        """
        Returns the filter index
        :return: integer
        """
        return self._idx

    def get_type(self):
        """
        Returns the filter type
        :return: FilterType
        """
        return self._type

    def get_text(self):
        """
        Returns the text
        :return: string
        """
        return self._text

    def get_constraint(self):
        """
        Returns the constraint
        :return: string
        """
        return self._constraint

    @staticmethod
    def get_expr_from_string(regex_expr, string):
        """
        Returns a expr from a string depending on the given regex expression
        :param regex_expr: regex expression
        :param string: string
        :return:
        """
        s = re.search(regex_expr, string)
        if s:
            return s.group(0)
        else:
            return ""

    def get_expr(self):
        """
        Returns the entered expression symbol
        :return:
        """
        regex_expr = '[<!=>]+'
        if self._type is FilterType.SINGLE_VALUE:
            return self.get_expr_from_string(regex_expr, self._constraint[0])
        elif self._type is FilterType.POINT2:
            x = self.get_expr_from_string(regex_expr, self._constraint[0])
            if self._constraint[2]:
                return x, x
            y = self.get_expr_from_string(regex_expr, self._constraint[1])
            return x, y
        elif self._type is FilterType.POINT3 or self._type is FilterType.COLOR3:
            x = self.get_expr_from_string(regex_expr, self._constraint[0])
            if self._constraint[3]:
                return x, x, x
            y = self.get_expr_from_string(regex_expr, self._constraint[1])
            z = self.get_expr_from_string(regex_expr, self._constraint[2])
            return x, y, z

    def get_value(self):
        """
        Returns the entered value
        :return:
        """
        regex_value = '[+-]?([0-9]*[.,])?[0-9]+'
        if self._type is FilterType.SINGLE_VALUE:
            expr = self.get_expr_from_string(regex_value, self._constraint[0])
            if expr != "":
                return float(expr)
            return re.sub('[<!=>]+', '', self._constraint[0])
        elif self._type is FilterType.POINT2:
            expr_x = self.get_expr_from_string(regex_value, self._constraint[0])
            expr_y = self.get_expr_from_string(regex_value, self._constraint[1])
            if expr_x != "" and expr_y != "":
                return float(expr_x), float(expr_y)
            elif expr_x != "" and expr_y == "":
                return float(expr_x), 0
            elif expr_x == "" and expr_y != "":
                return 0, float(expr_y)
            else:
                return 0, 0
        elif self._type is FilterType.POINT3 or self._type is FilterType.COLOR3:
            expr_x = self.get_expr_from_string(regex_value, self._constraint[0])
            expr_y = self.get_expr_from_string(regex_value, self._constraint[1])
            expr_z = self.get_expr_from_string(regex_value, self._constraint[2])
            if expr_x != "" and expr_y != "" and expr_z != "":
                return float(expr_x), float(expr_y), float(expr_z)
            elif expr_x != "" and expr_y != "" and expr_z == "":
                return float(expr_x), float(expr_y), 0
            elif expr_x != "" and expr_y == "" and expr_z != "":
                return float(expr_x), 0, float(expr_z)
            elif expr_x == "" and expr_y != "" and expr_z != "":
                return 0, float(expr_y), float(expr_z)
            elif expr_x == "" and expr_y == "" and expr_z != "":
                return 0, 0, float(expr_z)
            elif expr_x != "" and expr_y == "" and expr_z == "":
                return float(expr_x), 0, 0
            elif expr_x == "" and expr_y != "" and expr_z == "":
                return 0, float(expr_y), 0
            else:
                return 0, 0, 0

    def to_string(self):
        """
        Returns a string with class information
        :return:
        """
        return "FilterType: {} " \
               "Text: {}" \
               "Constraint: {}".format(self._type, self._text, self._constraint)


class ViewFilter(QWidget):

    """
        ViewFilter
        Handles the view and all filter interactions
    """

    def __init__(self, parent=None):
        QWidget.__init__(self, parent=None)
        uic.loadUi('View/ui/filter.ui', self)

        self._controller = None

        # center widget depending on screen size
        desktop_widget = QApplication.desktop()
        screen_rect = desktop_widget.availableGeometry(self)
        self.move(screen_rect.center() - self.rect().center())

        self._filter_items = {}

        self.combItems.currentTextChanged.connect(self.update_stacked_widget)
        self.btnClose.clicked.connect(self.close)
        self.btnAddFilter.clicked.connect(self.add_filter)
        self.btnApplyFilter.clicked.connect(self.apply_filters)
        self.btnDeleteFilter.clicked.connect(self.delete_filter)
        self.btnClearAll.clicked.connect(self.clear_filter)

        self.cbPoint2.stateChanged.connect(self.state_changed)
        self.cbPoint3.stateChanged.connect(self.state_changed)
        self.cbColor.stateChanged.connect(self.state_changed)

        self.leExpX.textChanged.connect(self.le_point_2x)
        self.leExpY.textChanged.connect(self.le_point_2y)
        self.leExpX_2.textChanged.connect(self.le_point_3x)
        self.leExpY_2.textChanged.connect(self.le_point_3y)
        self.leExpZ.textChanged.connect(self.le_point_3z)
        self.leExpR.textChanged.connect(self.le_color_r)
        self.leExpG.textChanged.connect(self.le_color_g)
        self.leExpB.textChanged.connect(self.le_color_b)

        self.filterList.setStyleSheet("QListWidget::item { border-bottom: 1px solid black; }")

    def set_controller(self, controller):
        """
        Sets the connection to the controller
        :param controller: Controller
        :return:
        """
        self._controller = controller

    def prepare_new_data(self):
        """
        Prepare view for new incoming data
        :return:
        """
        # self._filter_items.clear()
        self.combItems.clear()

    def init_data(self, render_data):

        """
        Initialise the view
        :param render_data:
        :return:
        """

        # iterate through all paths and their vertices
        for key, path in render_data.dict_paths.items():

            # pathinfo stuff sample_idx, final_estimate, path_depth
            if path.sample_idx:
                if not self._filter_items.get('sampleIndex', None):
                    self._filter_items['sampleIndex'] = path.sample_idx

            if path.valid_depth:
                if not self._filter_items.get('pathDepth', None):
                    self._filter_items['pathDepth'] = path.path_depth

            if path.final_estimate:
                if not self._filter_items.get('finalEstimate', None):
                    self._filter_items['finalEstimate'] = path.final_estimate

            # add path user data
            user_data_path = path.data_list
            for item in user_data_path:
                for key_user, value_user in item.items():
                    if not self._filter_items.get(key_user, None):
                        # add item if not in list
                        if isinstance(value_user, list):
                            self._filter_items[key_user] = value_user[0]
                        else:
                            self._filter_items[key_user] = value_user

            # iterate over intersection points
            verts = path.dict_vertices
            for key_verts, vertex in verts.items():
                user_data_vert = vertex.data_list
                for item in user_data_vert:
                    for key_user, value_user in item.items():
                        # add item if not in list
                        if not self._filter_items.get(key_user, None):
                            if isinstance(value_user, list):
                                self._filter_items[key_user] = value_user[0]
                            else:
                                self._filter_items[key_user] = value_user

        # add all values to combBox
        for key, value in self._filter_items.items():
            self.combItems.addItem(key)

        # update expression view on current item
        if self.combItems.count() > 0:
            self.update_stacked_widget(self.combItems.currentText())

    def is_active(self):
        """
        Returns if filtering is active
        :return: boolean
        """
        return self.cbFilterEnabled.isChecked()

    def keyPressEvent(self, event):
        """
        Handles key press enter events.
        Checks if the enter key is pressed to apply the filter
        :param event:
        :return:
        """
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            self.add_filter(True)

    @pyqtSlot(str, name='update_stacked_widget')
    def update_stacked_widget(self, text):
        """
        Updates the stacked widget view handling the constraints inputs
        :param text: string
        :return:
        """
        item = self._filter_items.get(text, None)
        if item:
            """
                Index   - Widget:
                0       - bool, float, int, string
                1       - Point2
                2       - Point3
                3       - Color3
            """
            if isinstance(item, bool) or isinstance(item, float) or isinstance(item, int) or isinstance(item, str):
                self.stackedWidget.setCurrentIndex(0)
            elif isinstance(item, Point2f) or isinstance(item, Point2i):
                self.stackedWidget.setCurrentIndex(1)
            elif isinstance(item, Point3f) or isinstance(item, Point3i):
                self.stackedWidget.setCurrentIndex(2)
            elif isinstance(item, Color3f):
                self.stackedWidget.setCurrentIndex(3)

    @pyqtSlot(str, name='le_point_2x')
    def le_point_2x(self, text):
        if self.cbPoint2.isChecked():
            self.leExpY.blockSignals(True)
            self.leExpY.setText(text)
            self.leExpY.blockSignals(False)

    @pyqtSlot(str, name='le_point_2y')
    def le_point_2y(self, text):
        if self.cbPoint2.isChecked():
            self.leExpX.blockSignals(True)
            self.leExpX.setText(text)
            self.leExpX.blockSignals(False)

    @pyqtSlot(str, name='le_point_3x')
    def le_point_3x(self, text):
        if self.cbPoint3.isChecked():
            self.leExpY_2.blockSignals(True)
            self.leExpZ.blockSignals(True)
            self.leExpY_2.setText(text)
            self.leExpZ.setText(text)
            self.leExpY_2.blockSignals(False)
            self.leExpZ.blockSignals(False)

    @pyqtSlot(str, name='le_point_3y')
    def le_point_3y(self, text):
        if self.cbPoint3.isChecked():
            self.leExpX_2.blockSignals(True)
            self.leExpZ.blockSignals(True)
            self.leExpX_2.setText(text)
            self.leExpZ.setText(text)
            self.leExpX_2.blockSignals(False)
            self.leExpZ.blockSignals(False)

    @pyqtSlot(str, name='le_point_3z')
    def le_point_3z(self, text):
        if self.cbPoint3.isChecked():
            self.leExpX_2.blockSignals(True)
            self.leExpY_2.blockSignals(True)
            self.leExpX_2.setText(text)
            self.leExpY_2.setText(text)
            self.leExpX_2.blockSignals(False)
            self.leExpY_2.blockSignals(False)

    @pyqtSlot(str, name='le_color_r')
    def le_color_r(self, text):
        if self.cbColor.isChecked():
            self.leExpG.blockSignals(True)
            self.leExpB.blockSignals(True)
            self.leExpG.setText(text)
            self.leExpB.setText(text)
            self.leExpG.blockSignals(False)
            self.leExpB.blockSignals(False)

    @pyqtSlot(str, name='le_color_g')
    def le_color_g(self, text):
        if self.cbColor.isChecked():
            self.leExpR.blockSignals(True)
            self.leExpB.blockSignals(True)
            self.leExpR.setText(text)
            self.leExpB.setText(text)
            self.leExpR.blockSignals(False)
            self.leExpB.blockSignals(False)

    @pyqtSlot(str, name='le_color_b')
    def le_color_b(self, text):
        if self.cbColor.isChecked():
            self.leExpR.blockSignals(True)
            self.leExpG.blockSignals(True)
            self.leExpR.setText(text)
            self.leExpG.setText(text)
            self.leExpR.blockSignals(False)
            self.leExpG.blockSignals(False)

    @pyqtSlot(bool, name='clear_filter')
    def clear_filter(self, clicked):
        """
        Informs the controller to clear all filters
        :param clicked: boolean
        :return:
        """
        self._controller.clear_filter()

    @pyqtSlot(bool, name='delete_filter')
    def delete_filter(self, clicked):
        """
        Deletes a filter from the view and informs the controller to delete the filter
        :param clicked: boolean
        :return:
        """
        if self.filterList.count() > 0:
            item = self.filterList.currentItem()
            if item:
                self._controller.delete_filter(item)

    @pyqtSlot(int, name='state_changed')
    def state_changed(self, state):
        if state != Qt.Checked:
            return
        idx = self.stackedWidget.currentIndex()
        if idx == 1:
            self.leExpY.setText(self.leExpX.text())
        elif idx == 2:
            self.leExpY_2.setText(self.leExpX_2.text())
            self.leExpZ.setText(self.leExpX_2.text())
        elif idx == 3:
            self.leExpG.setText(self.leExpR.text())
            self.leExpB.setText(self.leExpR.text())

    @pyqtSlot(bool, name='add_filter')
    def add_filter(self, clicked):
        """
        Informs the controller to add a filter to the filter list view
        :param clicked: boolean
        :return:
        """
        idx = self.stackedWidget.currentIndex()
        if not self.is_line_edit_empty(idx):
            fs = FilterSettings(self)
            self._controller.add_filter(fs)

    @pyqtSlot(bool, name='apply_filters')
    def apply_filters(self, clicked):
        """
        Informs the controller to apply the filter
        :param clicked: boolean
        :return:
        """
        if self.filterList.count() > 0:
            self._controller.apply_filters()

    def add_filter_to_view(self, filter_settings):
        """
        Adds a filter to the filter list
        :param filter_settings:
        :return:
        """
        fi = FilterListItem(filter_settings)
        item = QListWidgetItem()
        item.setSizeHint(fi.sizeHint())
        idx = self.stackedWidget.currentIndex()
        self.filterList.addItem(item)
        self.filterList.setItemWidget(item, fi)
        self.clear_line_edit_entries(idx)

    def is_line_edit_empty(self, index):
        """
        Checks if a input is empty
        :param index:
        :return:
        """
        if index == 0:
            return self.leExp.text() == ""
        elif index == 1:
            if self.cbPoint2.isChecked():
                return self.leExpX.text() == ""
            return self.leExpX.text() == "" and self.leExpY.text() == ""
        elif index == 2:
            if self.cbPoint3.isChecked():
                return self.leExpX_2.text() == ""
            return self.leExpX_2.text() == "" and self.leExpY_2.text() == "" and self.leExpZ.text() == ""
        elif index == 3:
            if self.cbColor.isChecked():
                return self.leExpR.text() == ""
            return self.leExpR.text() == "" and self.leExpG.text() == "" and self.leExpB.text() == ""

    def clear_line_edit_entries(self, index):
        """
        Clears all line entries of the current view
        :param index: integer
        :return:
        """
        if index == 0:
            self.leExp.clear()
        elif index == 1:
            self.leExpX.clear()
            self.leExpY.clear()
        elif index == 2:
            self.leExpX_2.clear()
            self.leExpY_2.clear()
            self.leExpZ.clear()
        elif index == 3:
            self.leExpR.clear()
            self.leExpG.clear()
            self.leExpB.clear()
