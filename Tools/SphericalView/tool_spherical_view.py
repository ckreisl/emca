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

from Core.tool import Tool
import logging

from View.SphericalViewImage.view_spherical_view_image import ViewSphericalViewImage
from Types.point3 import Point3f
from Types.point2 import Point2i
from Types.vector3 import Vec3f
from PyQt5.QtCore import pyqtSlot
from PyQt5 import uic

import numpy as np
import io


class SphericalView(Tool):

    def __init__(self):
        Tool.__init__(
            self,
            "SphericalView",
            66
        )
        uic.loadUi('Tools/SphericalView/spherical_view.ui', self)

        self._path = None
        self._render_data = None
        self._render_size = Point2i(256, 128)
        self._sample_count = 16
        self._integrator = "path"

        self._spherical_view = ViewSphericalViewImage(self)
        self.hdrImage.addWidget(self._spherical_view)

    def prepare_new_data(self):
        self._spherical_view.clear()
        self._spherical_view.enable_buttons(False)

    def update_path_indices(self, indices):
        pass

    def update_vertex_indices(self, tpl_list):
        pass

    def select_path(self, index):
        pass

    def select_vertex(self, tpl):
        if self._render_data:
            dict_paths = self._render_data.dict_paths
            self._spherical_view.select_vertex(dict_paths, tpl)

    def serialize(self, stream):
        logging.info("Serialize in: {}".format(self.name))
        if not self._spherical_view.pos is None:
            self._render_size.x = self.sbWidth.value()
            self._render_size.y = self.sbHeight.value()
            self._sample_count = int(self.sbSampleCount.value())
            self._integrator = self.integrator.text()
            # send package id
            stream.write_short(self.flag)
            # send point / data
            stream.write_float(self._spherical_view.pos.x)
            stream.write_float(self._spherical_view.pos.y)
            stream.write_float(self._spherical_view.pos.z)
            # send amount of samples
            stream.write_int(self._sample_count)
            # send render size
            stream.write_int(self._render_size.x)
            stream.write_int(self._render_size.y)
            # send integrator
            stream.write_string(self._integrator)

    def deserialize(self, stream):
        logging.info("Deserialize in: {}".format(self.name))
        size = stream.read_int()
        if size > 0:
            self._path = io.BytesIO(stream.read(size))
        else:
            self._path = None

    def update_view(self):
        if self._spherical_view.load_hdr_image(self._path):
            self._spherical_view.enable_buttons(True)

    def init_render_data(self, render_data):
        self._render_data = render_data
