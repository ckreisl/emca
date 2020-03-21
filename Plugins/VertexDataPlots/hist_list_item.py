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

from PyQt5.QtWidgets import QListWidgetItem


class HistListItem(QListWidgetItem):

    def __init__(self, name, list_widget, plot_data, xmin, xmax, plot_canvas, widget_idx):
        QListWidgetItem.__init__(self, name, list_widget)

        self._name = name
        self._plot_data = plot_data
        self._xmin = xmin
        self._xmax = xmax
        self._plot_canvas = plot_canvas
        self._widget_idx = widget_idx

    @property
    def name(self):
        return self._name

    @property
    def plot_data(self):
        return self._plot_data

    @property
    def xmin(self):
        return self._xmin

    @property
    def xmax(self):
        return self._xmax

    @property
    def plot_canvas(self):
        return self._plot_canvas

    @property
    def widget_idx(self):
        return self._widget_idx
