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
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QPoint
import math
import logging


class HDRGraphicsView(QGraphicsView):

    """
        HDRGraphicsView
        Custom QGraphicsView which holds the rendered image and handles interactions
    """

    def __init__(self, parent):
        QGraphicsView.__init__(self)

        # allow drag n drop events
        self.setAcceptDrops(True)
        # keep track of mouse moving within area
        self.setMouseTracking(True)
        # important for mouse tracking and later pixel selection
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)

        self._hdri = None

        self._scene = QGraphicsScene()
        self._parent = parent
        self._scale_factor = 1.15
        self._pixmap_item = QGraphicsPixmapItem()

        self.setScene(self._scene)

        self._old_scene_pos = QPoint()

    @property
    def pixmap(self):
        """
        Returns the rendered image as pixmap if there is one,
        otherwise None will be returned
        :return: QPixmap or None
        """
        if self._pixmap_item:
            return self._pixmap_item.pixmap()
        return None

    def transform_to_image_coordinate(self, pos):
        """
        Transforms the selected position into image coordinates space
        :param pos: QPoint
        :return: QPoint
        """
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

    def mousePressEvent(self, q_mouse_event):
        """
        Handles a mouse press event, aves the current position.
        A request to the controller will only be send if the position will be the same after mouse btn release.
        :param q_mouse_event:
        :return:
        """
        global_pos = q_mouse_event.globalPos()
        self._old_scene_pos = self.transform_to_scene_pos(global_pos)
        super().mousePressEvent(q_mouse_event)

    def mouseReleaseEvent(self, q_mouse_event):
        """
        Handles a mouse button release.
        Informs the controller if the position has not changed since the click.
        Otherwise the image will be moved.
        :param q_mouse_event:
        :return:
        """
        global_pos = q_mouse_event.globalPos()
        new_pos = self.transform_to_scene_pos(global_pos)
        if self._old_scene_pos == new_pos:
            pixel = self.transform_to_image_coordinate(q_mouse_event.globalPos())
            if self.pixel_within_bounds(pixel):
                self._parent.request_render_data(pixel)
        super().mouseReleaseEvent(q_mouse_event)

    def mouseMoveEvent(self, q_mouse_event):
        """
        Handles mouse move event
        :param q_mouse_event:
        :return:
        """
        image_coord = self.transform_to_image_coordinate(q_mouse_event.globalPos())
        text = '({},{})'.format(image_coord.x(), image_coord.y())
        self._parent.labelCurrentPos.setText(text)
        super().mouseMoveEvent(q_mouse_event)

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

    def pixel_within_bounds(self, pixel):
        """
        Checks if the selected pixel is within the image ranges,
        returns false if no image is available or the coordinates are out of range
        :param pixel: QPoint
        :return: boolean
        """
        if self._hdri:
            pixmap = self._hdri.pixmap
            b1 = pixel.x() >= 0 and pixel.y() >= 0
            b2 = pixel.x() < pixmap.width() and pixel.y() < pixmap.height()
            return b1 and b2
        return False

    def display_image(self):
        """
        Displays the image within the view
        :return:
        """
        self._pixmap_item = QGraphicsPixmapItem(self._hdri.pixmap)
        self._pixmap_item.setFlag(QGraphicsPixmapItem.ItemIsMovable)
        self._scene.addItem(self._pixmap_item)
        self.fitInView(self._pixmap_item, Qt.KeepAspectRatio)

    def update_image(self):
        """
        Upates the render image in the view
        :return:
        """
        items_list = self._scene.items()
        items_list[0].setPixmap(self._hdri.pixmap)

    def load_hdr_image(self, filepath):
        """
        Loads a hdr (exr) image from a given filepath.
        Returns true if the image was successfully loaded
        :param filepath: string
        :return:
        """
        try:
            self._scene.clear()
            self._hdri = HDRImage(filepath)
            self.display_image()
            self._parent.enable_view(True)
            return True
        except Exception as e:
            logging.error(e)
            return False

    def update_exposure(self, value):
        """
        Updates the exposure of the image, informs the HDRImage class.
        :param value: float
        :return:
        """
        self._hdri.exposure = value
        self.update_image()

    def reset(self):
        """
        Resets the image view. Image sets to fit in view.
        :return:
        """
        if self._pixmap_item:
            self.fitInView(self._pixmap_item, Qt.KeepAspectRatio)
            self._scene.setSceneRect(self._scene.itemsBoundingRect())
