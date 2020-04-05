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

from Core.hdr_image import HDRImage
from PyQt5.QtWidgets import QGraphicsPixmapItem
from PyQt5.QtWidgets import QGraphicsScene
from PyQt5.QtWidgets import QGraphicsView
from PyQt5.QtCore import QPoint
from PyQt5.QtCore import Qt
import math
import logging


class HDRGraphicsViewBase(QGraphicsView):

    def __init__(self):
        QGraphicsView.__init__(self)
        # allow drag n drop events
        self.setAcceptDrops(True)
        # keep track of mouse moving within area
        self.setMouseTracking(True)
        # important for mouse tracking and later pixel selection
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self._hdri = HDRImage()
        self._scene = QGraphicsScene()
        self._scale_factor = 1.15
        # self._pixmap_item = QGraphicsPixmapItem()
        self._pixmap_item = None
        self.setScene(self._scene)

    @property
    def hdr_image(self):
        if self._hdri:
            return self._hdri
        return None

    @property
    def pixmap(self):
        """
        Returns the rendered image as pixmap if there is one,
        otherwise None will be returned
        :return: QPixmap or None
        """
        if self._hdri:
            return self._hdri.pixmap
        return None

    @property
    def pixmap_item(self):
        return self._pixmap_item

    def mousePressEvent(self, q_mouse_event):
        super().mousePressEvent(q_mouse_event)

    def mouseReleaseEvent(self, q_mouse_event):
        super().mouseReleaseEvent(q_mouse_event)

    def mouseMoveEvent(self, q_mouse_event):
        super().mouseMoveEvent(q_mouse_event)

    def dragMoveEvent(self, q_drag_move_event):
        """
        Nothing to-do here, has to be implemented for drag and drop
        :param q_drag_move_event:
        :return:
        """
        # nothing to-do here
        pass

    def dragEnterEvent(self, q_drag_enter_event):
        """
        Handles drag enter event for drag and drop of exr images
        :param q_drag_enter_event:
        :return:
        """
        if q_drag_enter_event.mimeData().hasFormat('text/plain'):
            q_drag_enter_event.acceptProposedAction()

    def dropEvent(self, q_drop_event):
        """
        Handles drop events, will load and display an exr image
        :param q_drop_event:
        :return:
        """
        if q_drop_event.mimeData().hasUrls():
            q_url = q_drop_event.mimeData().urls()[0]
            path = str(q_url.path())
            if path.endswith('.exr'):
                self.load_hdr_image(path)

    def wheelEvent(self, q_wheel_event):
        """
        Handles the mouse wheel event for zooming in and out
        :param q_wheel_event:
        :return:
        """
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

    def set_falsecolor(self, falsecolor):
        if self._hdri:
            self._hdri.falsecolor = falsecolor
            self.display_image(self.pixmap)

    def transform_to_image_coordinate(self, pos):
        """
        Transforms the selected position into image coordinates space
        :param pos: QPoint
        :return: QPoint
        """
        if self._pixmap_item is None:
            return QPoint(0, 0)
        local_pos = self.mapFromGlobal(pos)
        scene_pos = self.mapToScene(local_pos)
        item_local_pos = self._pixmap_item.mapFromScene(scene_pos)
        x = math.floor(item_local_pos.x())
        y = math.floor(item_local_pos.y())
        return QPoint(x, y)

    def transform_to_scene_pos(self, pos):
        """
        Transforms a point into scene space
        :param pos: QPoint
        :return: QPoint
        """
        local_pos = self.mapFromGlobal(pos)
        scene_pos = self.mapToScene(local_pos)
        x = math.floor(scene_pos.x())
        y = math.floor(scene_pos.y())
        return QPoint(x, y)

    def pixel_within_bounds(self, pixel):
        """
        Checks if the selected pixel is within the image ranges,
        returns false if no image is available or the coordinates are out of range
        :param pixel: QPoint
        :return: boolean
        """
        if not self._hdri.is_pixmap_set():
            return False

        if self._hdri:
            pixmap = self._hdri.pixmap
            b1 = pixel.x() >= 0 and pixel.y() >= 0
            b2 = pixel.x() < pixmap.width() and pixel.y() < pixmap.height()
            return b1 and b2
        return False

    def display_image(self, pixmap):
        """
        Displays the image within the view
        :return:
        """
        if len(self._scene.items()) > 0 and self._pixmap_item:
            self._pixmap_item.setPixmap(pixmap)
        else:
            item = self._scene.addPixmap(pixmap)
            item.setFlag(QGraphicsPixmapItem.ItemIsMovable)
            self.fitInView(item, Qt.KeepAspectRatio)
            self._pixmap_item = item

    def update_image(self, pixmap):
        """
        Upates the render image in the view
        :return:
        """
        items_list = self._scene.items()
        items_list[0].setPixmap(pixmap)

    def load_hdr_image(self, filepath, falsecolor=False):
        """
        Loads a hdr (exr) image from a given filepath or bytestream
        Returns true if the image was successfully loaded
        :param filepath: string
        :param falsecolor: boolean
        :return:
        """
        success = self._hdri.load_exr(filepath, falsecolor)
        self.display_image(self._hdri.pixmap)
        return success

    def update_exposure(self, value):
        """
        Updates the exposure of the image, informs the HDRImage class.
        :param value: float
        :return:
        """
        if self._hdri:
            self._hdri.exposure = value
            self.update_image(self._hdri.pixmap)

    def reset(self):
        """
        Resets the image view. Image sets to fit in view.
        :return:
        """
        if self._pixmap_item:
            self.fitInView(self._pixmap_item, Qt.KeepAspectRatio)
            self._scene.setSceneRect(self._scene.itemsBoundingRect())

    def clear(self):
        self._scene.clear()
        self._pixmap_item = None
