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
from PyQt5.QtCore import QPoint
import logging


class HDRGraphicsView(HDRGraphicsViewBase):

    """
        HDRGraphicsView
        Custom QGraphicsView which holds the rendered image and handles interactions
    """

    def __init__(self, parent):
        HDRGraphicsViewBase.__init__(self)
        self._parent = parent
        self._old_scene_pos = QPoint()

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

    def dropEvent(self, q_drop_event):
        try:
            super().dropEvent(q_drop_event)
            self._parent.enable_view(True)
        except Exception as e:
            logging.error(e)

