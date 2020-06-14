"""
    MIT License

    Copyright (c) 2020 Christoph Kreisl

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
"""

from plugins.plugins_handler import PluginsHandler
from model.options_data import OptionsConfig
from model.render_info import RenderInfo
from model.camera_data import CameraData
from model.mesh_data import MeshData
from model.render_data import RenderData
from model.contribution_data import SampleContributionData
from PySide2.QtCore import Signal
from PySide2.QtCore import QObject
from core.messages import StateMsg
from filter.filter import Filter
from detector.detector import Detector
import numpy as np
import time
import logging


class Model(QObject):

    """
        Dataset
        Represents the Model of the Model-View-Controller.
        Stores and handles all data files.
        Therefore deserializes the data from the socket stream.
    """

    sendStateMsgSig = Signal(tuple)

    def __init__(self):
        QObject.__init__(self, parent=None)
        self._options = OptionsConfig()
        self._plugins_handler = PluginsHandler()

        self._render_info = RenderInfo()
        self._camera_data = CameraData()
        self._mesh_data = MeshData()
        self._render_data = RenderData()
        self._final_estimate_data = SampleContributionData()

        # Model also holds refs to filter and detector
        self._filter = Filter()
        self._detector = Detector()

        # model keeps track of current selected path indices
        self._current_path_indices = np.array([], dtype=np.int32)
        self._current_path_index = -1
        self._current_vertex_tpl = ()

        self._controller = None

    def set_callback(self, callback):
        """
        Set / Connect Qt signal callback to controllers msg handler
        """
        self.sendStateMsgSig.connect(callback)

    def set_controller(self, controller):
        """
        Set the connection to the controller
        :param controller:
        :return:
        """
        self._controller = controller
        self._plugins_handler.set_controller(controller)

    @property
    def filter(self):
        return self._filter

    @property
    def detector(self):
        return self._detector

    @property
    def current_path_indices(self):
        return self._current_path_indices

    @current_path_indices.setter
    def current_path_indices(self, indices):
        self._current_path_indices = indices

    @property
    def current_path_index(self):
        return self._current_path_index

    @current_path_index.setter
    def current_path_index(self, path_index):
        self._current_path_index = path_index

    @property
    def current_vertex_tpl(self):
        return self._current_vertex_tpl

    @current_vertex_tpl.setter
    def current_vertex_tpl(self, tpl):
        self._current_vertex_tpl = tpl

    @property
    def plugins_handler(self):
        """
        Returns the Plugins Handler
        :return:
        """
        return self._plugins_handler

    @property
    def render_info(self):
        """
        Returns the Render Info
        :return:
        """
        return self._render_info

    @property
    def camera_data(self):
        """
        Returns the Camera Data
        :return:
        """
        return self._camera_data

    @property
    def mesh_data(self):
        """
        Returns the Mesh Data
        :return:
        """
        return self._mesh_data

    @property
    def render_data(self):
        """
        Returns the Render Data.
        All gathered information of one pixel
        :return:
        """
        return self._render_data

    @property
    def final_estimate_data(self):
        """
        Returns the Final Estimate Plot Data
        :return:
        """
        return self._final_estimate_data

    @property
    def options_data(self):
        """
        Returns the options loaded from .ini file
        :return: Options Object
        """
        return self._options

    @render_info.setter
    def render_info(self, new_render_info):
        """
        Set function for Render Info data
        :param new_render_info:
        :return:
        """
        self._render_info = new_render_info

    @camera_data.setter
    def camera_data(self, new_camera_data):
        """
        Set function for Camera data
        :param new_camera_data:
        :return:
        """
        self._camera_data = new_camera_data

    @mesh_data.setter
    def mesh_data(self, new_mesh_data):
        """
        Set function for Mesh data
        :param new_mesh_data:
        :return:
        """
        self._mesh_data = new_mesh_data

    @render_data.setter
    def render_data(self, new_render_data):
        """
        Set function for Render data
        :param new_render_data:
        :return:
        """
        self._render_data = new_render_data

    def prepare_new_data(self):
        """
        Resets the current selected path|vertex|indices and
        calls the PluginsHandler prepare_new_data function.
        :return:
        """
        self._plugins_handler.prepare_new_data()
        self._current_path_indices = np.array([], dtype=np.int32)
        self._current_path_index = -1
        self._current_vertex_tpl = ()

    def serialize_render_info(self, stream):
        """
        Serialize the Render Info data and informs the controller about it
        Sends data to the server
        :param stream:
        :return:
        """
        start = time.time()
        self._render_info.serialize(stream=stream)
        logging.info('serialize render info in: {:.3}s'.format(time.time() - start))

    def deserialize_render_info(self, stream):
        """
        Deserialize the Render Info data and informs the controller about it
        Reads data from the socket stream
        :param stream:
        :return:
        """
        start = time.time()
        self._render_info.deserialize(stream=stream)
        logging.info('deserialize render info in: {:.3}s'.format(time.time() - start))
        self.sendStateMsgSig.emit((StateMsg.DATA_INFO, self._render_info))

    def deserialize_camera(self, stream):
        """
        Deserialize the Camera data and informs the controller about it
        :param stream:
        :return:
        """
        start = time.time()
        self._camera_data.deserialize(stream=stream)
        logging.info('deserialize camera data in: {:.3}s'.format(time.time() - start))
        self.sendStateMsgSig.emit((StateMsg.DATA_CAMERA, self._camera_data))

    def deserialize_scene_objects(self, stream):
        """
        Deserialize Mesh data (3D Scene objects) and informs the controller about it
        :param stream:
        :return:
        """
        start = time.time()
        self._mesh_data.deserialize(stream=stream)
        logging.info('deserialize mesh item in: {:.3}s'.format(time.time() - start))
        self.sendStateMsgSig.emit((StateMsg.DATA_MESH, self._mesh_data.meshes[-1]))

    def deserialize_render_data(self, stream):
        """
        Deserialize Render data and informs the controller about it
        :param stream:
        :return:
        """
        start = time.time()
        self._render_data.deserialize(stream=stream)
        logging.info('deserialize render data in: {:.3}s'.format(time.time() - start))
        self.sendStateMsgSig.emit((StateMsg.DATA_RENDER, self._render_data))

    def load_sample_contribution_data(self, dict_paths):
        """
        Return the Final Estimate data and informs the controller about it
        :return:
        """
        return self._final_estimate_data.load_final_estimate_from_data(dict_paths)
