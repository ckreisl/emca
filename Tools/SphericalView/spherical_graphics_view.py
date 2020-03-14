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

from View.RenderView.hdr_image import HDRImage
from PyQt5.QtWidgets import QGraphicsPixmapItem
from PyQt5.QtWidgets import QGraphicsScene
from PyQt5.QtWidgets import QGraphicsView
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QBrush
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QPoint
import logging

import matplotlib.pyplot as plt
import numpy as np


class SphericalGraphicsView(QGraphicsView):

    def __init__(self, parent):
        QGraphicsView.__init__(self)

        # keep track of mouse moving within area
        self.setMouseTracking(True)
        # important for mouse tracking and later pixel selection
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)

        self._hdri = None

        self._scene = QGraphicsScene()
        self._parent = parent
        self._scale_factor = 1.15
        # self._pixmap_item = QGraphicsPixmapItem()
        self._pixmap_item = None
        self._highlights = {}

        self.setScene(self._scene)

    @property
    def pixmap(self):
        if self._hdri:
            return self._hdri.pixmap
        return None

    def wheelEvent(self, q_wheel_event):
        angle_delta = q_wheel_event.angleDelta()
        old_pos = self.mapToScene(q_wheel_event.pos())
        if angle_delta.y() > 0:
            self.scale(self._scale_factor,
                       self._scale_factor)
        else:
            self.scale(1 / self._scale_factor,
                       1 / self._scale_factor)
        new_pos = self.mapToScene(q_wheel_event.pos())
        delta = new_pos - old_pos
        self.translate(delta.x(), delta.y())
        q_wheel_event.accept()

    def load_hdr_image(self, filepath, falsecolor=False):
        try:
            if self._hdri:
                del self._hdri
                self._hdri = None
            self._hdri = HDRImage(filepath, falsecolor)
        except Exception as e:
            logging.error(e)
            return False

        self.display_image(self._hdri.pixmap)
        return True

    def display_image(self, pixmap):
        if len(self._scene.items()) > 0 and self._pixmap_item:
            self._pixmap_item.setPixmap(pixmap)
        else:
            item = self._scene.addPixmap(pixmap)
            item.setFlag(QGraphicsPixmapItem.ItemIsMovable)
            self.fitInView(item, Qt.KeepAspectRatio)
            self._pixmap_item = item

        self.update_highlights()

    def set_falsecolor(self, falsecolor):
        if self._hdri:
            self._hdri.falsecolor = falsecolor
            self.display_image(self._hdri.pixmap)

    def update_exposure(self, exposure):
        if self._hdri:
            self._hdri.exposure = exposure
            self.display_image(self._hdri.pixmap)

    def update_highlights(self):
        if self._pixmap_item is None:
            return

        for h_name in self._highlights.keys():
            #TODO: assign colors deterministically, based on name
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
        if not color is None:
            self._highlights[name]['color'] = QColor(color[0], color[1], color[2])
            if not self._highlights[name].get('ellipse') is None:
                self._highlights[name]['ellipse'].setPen(self._highlights[name]['color'])
        if direction is None:
            self._highlights[name]['x'] = None
            self._highlights[name]['y'] = None
            if not self._highlights[name].get('ellipse') is None:
                self._highlights[name]['ellipse'].hide()
        else:
            theta = np.arccos(direction[2]);
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

    def reset(self):
        self.fitInView(self._pixmap_item, Qt.KeepAspectRatio)
        self._scene.setSceneRect(self._scene.itemsBoundingRect())

    def clear(self):
        self._scene.clear()
        self._pixmap_item = None
        self._hdri = None
        for h_name in self._highlights.keys():
            if self._highlights[h_name].get('ellipse'):
                self._highlights[h_name]['ellipse'] = None
