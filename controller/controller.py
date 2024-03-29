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

from PySide2.QtCore import QObject
from PySide2.QtCore import Slot
from core.messages import StateMsg
from controller.controller_stream import ControllerSocketStream
from controller.controller_detector import ControllerDetector
from controller.controller_filter import ControllerFilter
from controller.controller_scene import ControllerRenderScene
from controller.controller_options import ControllerOptions
import numpy as np
import logging
import os


class Controller(QObject):

    """
        Handles the core functionality of the Brushing and Linking concept.
        Contains Sub-Controllers handling specific sub logic.
    """

    def __init__(self, model, view, parent=None):
        QObject.__init__(self, parent=parent)

        self._model = model
        self._view = view

        # init sub controllers
        self._controller_detector = ControllerDetector(self, model, view)
        self._controller_filter = ControllerFilter(self, model, view)
        self._controller_stream = ControllerSocketStream(self, model, view)
        self._controller_scene = ControllerRenderScene(self, model, view)
        self._controller_options = ControllerOptions(self, model, view)

        # set connection between views and controller
        self._view.set_controller(self)

        # set connection between model and controller
        self._model.set_controller(self)
        self._model.set_callback(self.handle_state_msg)

        self.init_plugins()

    @property
    def detector(self):
        """
        Returns the sub-controller which handles the detector logic
        """
        return self._controller_detector

    @property
    def filter(self):
        """
        Returns the sub-controller which handles the filter logic
        """
        return self._controller_filter

    @property
    def stream(self):
        """
        Returns the sub-controller which handles the socket stream logic
        """
        return self._controller_stream

    @property
    def scene(self):
        """
        Returns the sub-controller which handles the 3d scene logic
        """
        return self._controller_scene

    @property
    def options(self):
        """
        Returns the sub-controller which handles the option logic
        """
        return self._controller_options

    def init_scene_renderer(self, scene_renderer):
        scene_renderer.set_update_path_callback(self.update_path)
        scene_renderer.set_select_path_callback(self.select_path)
        scene_renderer.set_select_intersection_callback(self.select_intersection)
        self._view.view_render_scene.init_scene_renderer(scene_renderer)
        # set scene renderer to plugins
        self._model.plugins_handler.set_scene_renderer(self._view.view_render_scene.scene_renderer)

    def init_plugins(self):
        """
        Init all views with parameters from the model (dataset)
        :return:
        """
        # set plugin btn
        plugins = self._model.plugins_handler.plugins
        self._view.view_emca.add_plugins(plugins)

    @Slot(tuple, name='handle_state_msg')
    def handle_state_msg(self, tpl):
        """
        Handle current state, messages mostly received from thread,
        which listens on the socket pipeline for incoming messages
        :param tpl: (StateMsg, None or Datatype)
        :return:
        """
        msg = tpl[0]
        logging.info('State: {}'.format(msg))
        if msg is StateMsg.DATA_INFO:
            self._view.view_render_info.update_render_info(tpl[1])
        elif msg is StateMsg.DATA_IMAGE:
            try:
                rendered_image_filepath = self._model.render_info.filepath()
                success = self._view.view_render_image.load_hdr_image(rendered_image_filepath)
                if success:
                    self._view.view_render_image.enable_view(True)
                    self._controller_options.save_options({'rendered_image_filepath': rendered_image_filepath})
            except Exception as e:
                self._view.view_popup.error_no_output_filepath(str(e))
        elif msg is StateMsg.DATA_RENDER:
            if not tpl[1].valid_sample_count():
                self._view.view_popup.error_no_sample_idx_set("")
                return None
            self._view.view_render_scene.load_traced_paths(tpl[1])
            self._view.view_render_scene_options.enable_general_settings(True)
            self._view.view_filter.init_data(tpl[1])
            self._view.enable_filter(True)
            self._view.view_render_data.enable_view(True)
            self._model.plugins_handler.init_data(tpl[1])
            if self._model.load_sample_contribution_data(self._model.render_data.dict_paths):
                self._view.view_plot.plot_final_estimate(self._model.final_estimate_data)
        elif msg is StateMsg.DATA_NOT_VALID:
            logging.error("Data is not valid!")
            # todo handle
        elif msg is StateMsg.SUPPORTED_PLUGINS:
            plugin_keys = tpl[1]
            for plugin_id in plugin_keys:
                if not self._model.plugins_handler.get_plugin_by_flag(plugin_id):
                    logging.error('Plugin = {} is not supported by client'.format(plugin_id))
                else:
                    self._model.plugins_handler.enable_plugin_by_id(plugin_id, True)
        elif msg is StateMsg.UPDATE_PLUGIN:
            plugin = self._model.plugins_handler.get_plugin_by_flag(tpl[1])
            if plugin:
                plugin.update_view()

        self._controller_scene.handle_state_msg(tpl)
        self._controller_stream.handle_state_msg(tpl)
        self._controller_filter.handle_state_msg(tpl)
        self._controller_detector.handle_state_msg(tpl)

    @Slot(bool, name='display_view_render_scene_options')
    def display_view_render_scene_options(self, clicked):
        if self._view.view_render_scene_options.isVisible():
            self._view.view_render_scene_options.activateWindow()
        else:
            self._view.view_render_scene_options.show()

    @Slot(bool, name='show_all_traced_paths')
    def show_all_traced_paths(self, enabled):
        """
        Informs the renderer to show all traced paths
        :param enabled:
        :return:
        """
        indices = np.array([])
        if enabled:
            indices = self._model.render_data.get_indices()
        self._view.view_render_scene_options.cbShowAllPaths.blockSignals(True)
        self._view.view_render_scene_options.cbShowAllPaths.setChecked(enabled)
        self._view.view_render_scene_options.cbShowAllPaths.blockSignals(False)
        self.update_path(indices, False)
        its = self._view.view_render_scene_options.cbShowAllIntersections.isChecked()
        self._view.view_render_scene.scene_renderer.show_all_traced_intersections(its)
        self._view.view_render_scene_options.cbShowPathRays.blockSignals(True)
        self._view.view_render_scene_options.cbShowPathRays.setChecked(enabled)
        self._view.view_render_scene_options.cbShowPathRays.blockSignals(False)

    def update_render_info_sample_count(self, value):
        """
        Updates the sample count value of render info
        :param value: sample_count
        :return:
        """
        render_info = self._model.render_info
        render_info.sample_count = value

    def prepare_new_data(self):
        """
        Prepare view and model for new incoming pixel render data
        (In most cases clear views and data for new incoming render data)
        :return:
        """
        self._view.view_render_scene.prepare_new_data()
        self._view.view_render_scene_options.prepare_new_data()
        self._view.view_render_data.prepare_new_data()
        self._view.view_filter.prepare_new_data()
        self._model.prepare_new_data()

    def update_path(self, indices, add_item):
        """
        Brushing and linking function,
        handles selected path indices,
        add_item informs if the next incoming index should be added to the current list or not
        :param indices: numpy array with path indices
        :param add_item: boolean
        :return:
        """

        if add_item:
            # add item to current indices array and update
            new_indices = np.unique(np.append(self._model.current_path_indices, indices))
        else:
            # just update whole indices array
            new_indices = indices

        # mark scatter plot
        self._view.view_plot.update_path_indices(new_indices)
        # draw 3d paths
        self._view.view_render_scene.update_path_indices(new_indices)
        # update 3d scene options
        self._view.view_render_scene_options.update_path_indices(new_indices)
        if len(self._model.render_data.get_indices()) != len(new_indices):
            self._view.view_render_scene_options.cbShowAllPaths.blockSignals(True)
            self._view.view_render_scene_options.cbShowAllPaths.setChecked(False)
            self._view.view_render_scene_options.cbShowAllPaths.blockSignals(False)
        # update all plugins
        self._model.plugins_handler.update_path_indices(new_indices)
        # update render data view
        self._view.view_render_data.show_path_data(new_indices, self._model.render_data)
        # select path if only one item
        if len(new_indices) == 1:
            self.select_path(new_indices[0])
        self._model.current_path_indices = new_indices

    def select_path(self, index):
        """
        Send path index update to all views
        :param index: path_index
        :return:
        """
        # self._view.view_plot.select_path(index) # does not work / function now available
        # this index must be an element of indices
        self._view.view_render_scene.select_path(index)
        # update 3d scene options
        path_option_settings = self._view.view_render_scene.scene_renderer.get_path_option_settings(index)
        self._view.view_render_scene_options.load_path_settings(path_option_settings)
        path_data = self._model.render_data.dict_paths[index]
        self._view.view_render_scene_options.select_path(index)
        self._view.view_render_scene_options.update_intersection_list(path_data)
        # select path in render data view
        self._view.view_render_data.select_path(index)
        # send path index, update plugins
        self._model.plugins_handler.select_path(index)
        # save current path_index
        self._model.current_path_index = index

    def select_intersection(self, tpl):
        """
        Send intersection index update to all views
        :param tpl: (path_index, intersection_index)
        :return:
        """
        # select intersection in 3D scene
        self._view.view_render_scene.select_intersection(tpl)
        # update 3d scene options
        self._view.view_render_scene_options.select_intersection(tpl)
        intersection_option_settings = self._view.view_render_scene.scene_renderer.get_intersection_option_settings(tpl)
        self._view.view_render_scene_options.load_intersection_settings(intersection_option_settings)
        # select intersection in render data view
        self._view.view_render_data.select_intersection(tpl)
        # send intersection index, update plugins
        self._model.plugins_handler.select_intersection(tpl)
        # save current tpl (path_index, intersection_index)
        self._model.current_intersection_tpl = tpl

    def display_view(self):
        """
        Opens and shows the EMCA view
        :return:
        """
        self._view.show()
        self._controller_options.load_pre_options()

    def close_app(self):
        """
        Closes all views and disconnected the client from the server (hard shut down)
        :return:
        """
        # close all views and close connection
        self._controller_stream.close()
        self._model.plugins_handler.close()
        self._view.view_render_info.close()
        self._view.view_detector.close()
        self._view.view_connect.close()
        self._view.view_render_scene.close()
        self._view.view_render_scene_options.close()
        self._view.view_filter.close()
        self._view.close()
