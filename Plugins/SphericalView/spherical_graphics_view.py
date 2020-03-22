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

from Core.hdr_graphics_view_base import HDRGraphicsViewBase
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QBrush
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QPoint
import logging

import matplotlib.pyplot as plt
import numpy as np


class SphericalGraphicsView(HDRGraphicsViewBase):

    def __init__(self, parent):
        HDRGraphicsViewBase.__init__(self)
        self._parent = parent
        self._highlights = {}

    def update_highlights(self):
        if self._pixmap_item is None:
            return

        for h_name in self._highlights.keys():
            # TODO: assign colors deterministically, based on name
            if self._highlights[h_name].get('color') is None:
                cmap = plt.get_cmap('Accent')
                color = cmap(np.random.rand())
                self._highlights[h_name]['color'] = QColor(color[0]*255, color[1]*255, color[2]*255)

            if self._highlights[h_name].get('ellipse') is None:
                self._highlights[h_name]['ellipse'] = self._scene.addEllipse(0.0, 0.0, 5.0, 5.0, self._highlights[h_name]['color'], QBrush(Qt.NoBrush))
                self._highlights[h_name]['ellipse'].setParentItem(self._pixmap_item)
                self._highlights[h_name]['ellipse'].setToolTip(h_name)

            if self._highlights[h_name].get('x') and self._highlights[h_name].get('y'):
                self._highlights[h_name]['ellipse'].setPos(QPoint(self._highlights[h_name]['x']*self.pixmap.width()-2.5, self._highlights[h_name]['y']*self.pixmap.height()-2.5))
                self._highlights[h_name]['ellipse'].show()
            else:
                self._highlights[h_name]['ellipse'].hide()

    def set_highlight(self, name, direction=None, color=None):
        if self._highlights.get(name) is None:
            self._highlights[name] = {}
        if color is not None:
            self._highlights[name]['color'] = QColor(color[0], color[1], color[2])
            if not self._highlights[name].get('ellipse') is None:
                self._highlights[name]['ellipse'].setPen(self._highlights[name]['color'])
        if direction is None:
            self._highlights[name]['x'] = None
            self._highlights[name]['y'] = None
            if not self._highlights[name].get('ellipse') is None:
                self._highlights[name]['ellipse'].hide()
        else:
            theta = np.arccos(direction[2])
            phi = np.arctan2(direction[1], direction[0])

            self._highlights[name]['x'] = (np.pi-phi)/(2.0*np.pi)
            self._highlights[name]['y'] = theta/np.pi

    def save_image(self):
        dialog = QFileDialog(self)
        dialog.setNameFilter("Images (*.png *.jpg)")
        dialog.selectNameFilter("Images (*.png *.jpg)")
        filepath = dialog.getSaveFileName(self)[0]

        logging.info('filepath: {}'.format(filepath))

        if filepath and self.pixmap:
            if filepath.endswith('.jpg'):
                self.pixmap.save(filepath, "jpg")
            if filepath.endswith('.png'):
                self.pixmap.save(filepath, "png")
            elif filepath.endswith('.exr'):
                if self._hdri:
                    self._hdri.save(filepath)

    def clear(self):
        super().clear()
        for h_name in self._highlights.keys():
            if self._highlights[h_name].get('ellipse'):
                self._highlights[h_name]['ellipse'] = None
