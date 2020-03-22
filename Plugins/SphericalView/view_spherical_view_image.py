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

from Plugins.SphericalView.spherical_graphics_view import SphericalGraphicsView
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSlot
from PyQt5 import uic
import logging


class ViewSphericalViewImage(QWidget):

    """
        ViewSphericalViewImage
    """

    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)
        uic.loadUi('Plugins/SphericalView/ui/spherical_view_image.ui', self)

        self._pos = None
        self._dirW_i = None
        self._dirW_o = None
        self._dirW_o_is_envmap = False
        self._falsecolor = False
        self._exposure = 0.0

        self._controller = None
        self._is_btn_enabled = False
        # HDR graphics view handles .exr images
        self._graphics_view = SphericalGraphicsView(self)

        # add graphics view
        self.hdrImage.addWidget(self._graphics_view)

        # connect signals
        self.btnSave.clicked.connect(self.save_image)
        self.btnReset.clicked.connect(self.fit_view)
        self.falsecolorCb.toggled.connect(self.falsecolor_cb)
        self.exposureSlider.valueChanged.connect(self.exposure_slider)

    @pyqtSlot(bool, name='save_image')
    def save_image(self, clicked):
        self._graphics_view.save_image()

    @pyqtSlot(bool, name='fit_view')
    def fit_view(self, clicked):
        self._graphics_view.reset()

    @pyqtSlot(bool, name='falsecolor_cb')
    def falsecolor_cb(self, checked):
        self.falsecolor = checked

    @pyqtSlot(int, name='exposure_slider')
    def exposure_slider(self, value):
        self.exposure = float(value)/100.0

    def load_hdr_image(self, filepath, falsecolor=False):
        return self._graphics_view.load_hdr_image(filepath, falsecolor=self._falsecolor)

    def set_highlight(self, name, direction=None, color=None):
        self._graphics_view.set_highlight(name, direction, color)

    def update_hightlights(self):
        self._graphics_view.update_highlights()

    @property
    def is_btn_enabled(self):
        return self._is_btn_enabled

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, pos):
        self._pos = pos

    @property
    def dirW_i(self):
        return self._dirW_i

    @dirW_i.setter
    def dirW_i(self, dirW_i):
        self._dirW_i = dirW_i
        self._graphics_view.set_highlight('incident direction', self._dirW_i, [0, 255, 0])

    @property
    def dirW_o(self):
        return self._dirW_o

    @dirW_o.setter
    def dirW_o(self, dirW_o):
        self._dirW_o = dirW_o
        if self._dirW_o_is_envmap:
            self._graphics_view.set_highlight('envmap', self._dirW_o, [255, 255, 0])
            self._graphics_view.set_highlight('outgoing direction', None, [255, 255, 255])
        else:
            self._graphics_view.set_highlight('envmap', None, [255, 255, 0])
            self._graphics_view.set_highlight('outgoing direction', self._dirW_o, [255, 255, 255])

    @property
    def dirW_o_is_envmap(self):
        return self._dirW_o_is_envmap

    @dirW_o_is_envmap.setter
    def dirW_o_is_envmap(self, dirW_o_is_envmap):
        changed = self._dirW_o_is_envmap != dirW_o_is_envmap
        self._dirW_o_is_envmap = dirW_o_is_envmap

        if changed:
            if self._dirW_o_is_envmap:
                self._graphics_view.set_highlight('envmap', self._dirW_o, [255, 255, 0])
                self._graphics_view.set_highlight('outgoing direction', None, [255, 255, 255])
            else:
                self._graphics_view.set_highlight('envmap', None, [255, 255, 0])
                self._graphics_view.set_highlight('outgoing direction', self._dirW_o, [255, 255, 255])

    @property
    def falsecolor(self):
        return self._falsecolor

    @falsecolor.setter
    def falsecolor(self, falsecolor):
        self._falsecolor = falsecolor
        if falsecolor:
            self.falsecolorCb.setCheckState(Qt.Checked)
        else:
            self.falsecolorCb.setCheckState(Qt.Unchecked)

        self._graphics_view.set_falsecolor(falsecolor)

    @property
    def exposure(self):
        return self._exposure

    @exposure.setter
    def exposure(self, exposure):
        self._exposure = exposure
        self.exposureSlider.setSliderPosition(int(exposure*100))

        self._graphics_view.update_exposure(exposure)

    def clear(self):
        self._graphics_view.clear()
        self.pos = None
        self.dirW_i = None
        self.dirW_o = None
        self.dirW_o_is_envmap = False

    def enable_buttons(self, enable):
        self._is_btn_enabled = enable
        self.btnSave.setEnabled(enable)
        self.btnReset.setEnabled(enable)

    def select_vertex(self, dict_paths, tpl):
        path = dict_paths.get(tpl[0], None)
        if path:
            dict_verts = path.dict_vertices
            vert = dict_verts.get(tpl[1], None)
            if vert and vert.pos:
                self.pos = vert.pos

                self.set_highlight('NEE', vert.pos.dir_to(vert.pos_ne), [255, 0, 0] if vert.is_ne_occluded else [0, 0, 255])

                prev_vert = next_vert = dict_verts.get(tpl[1]-1, None)
                if prev_vert and prev_vert.pos:
                    self.dirW_i = vert.pos.dir_to(prev_vert.pos)
                elif tpl[1] == 1 and path and path.path_origin:
                    self.dirW_i = vert.pos.dir_to(path.path_origin)
                else:
                    self.dirW_i = None

                next_vert = dict_verts.get(tpl[1]+1, None)
                if next_vert and next_vert.pos:
                    self.dirW_o_is_envmap = False
                    self.dirW_o = vert.pos.dir_to(next_vert.pos)
                else:
                    if vert.pos_envmap:
                        self.dirW_o_is_envmap = True
                        self.dirW_o = vert.pos.dir_to(vert.pos_envmap)
                    else:
                        self.dirW_o_is_envmap = False
                        self.dirW_o = None

