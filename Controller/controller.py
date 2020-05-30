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
from PySide2.QtWidgets import QFileDialog
from Core.messages import StateMsg
from Core.messages import ViewMode
from Core.socket_stream_client import SocketStreamClient
import numpy as np
import threading
import logging
import os


class Controller(QObject):
    """
        Handles most connection and logic between view and model (dataset)
    """

    def __init__(self, model, view, parent=None):
        QObject.__init__(self, parent=parent)

        self._model = model
        self._view = view

        # set connection between views and controller
        self._view.set_controller(self)

        # set connection between model and controller
        self._model.set_controller(self)
        self._model.sendStateMsgSig.connect(self.handle_state_msg)

        # controller keeps track of current selected path indices
        self._indices = np.array([], dtype=np.int32)

        self._sstream_client = None

        self.init_view()

    def init_view(self):
        """
        Init all views with parameters from the model (dataset)
        :return:
        """
        # set plugin btn
        plugins = self._model.plugins_handler.plugins
        self._view.view_emca.add_plugins(plugins)
        # init detector view with values from detector class
        detector = self._model.detector
        self._view.view_detector.init_values(detector)

    @property
    def indices(self):
        return self._indices

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
        if msg is StateMsg.CONNECT:
            self._sstream_client.request_render_info()
            self._view.view_emca.enable_view(True)
            self._view.view_render_scene.enable_view(True)
            self._model.plugins_handler.enable_plugins(True)
        elif msg is StateMsg.DISCONNECT:
            self._view.view_emca.enable_view(False)
            self._view.view_render_image.enable_view(False)
            self._view.view_render_scene.enable_view(False)
            self._model.plugins_handler.enable_plugins(False)
            self._sstream_client.shutdown()
            self._sstream_client = None
        elif msg is StateMsg.DATA_INFO:
            self._view.view_render_info.update_render_info(tpl[1])
            # automatically request scene data once render info is available
            if self._model.options_data.get_option_auto_scene_load():
                self._view.view_render_scene.remove_scene_objects()
                self._sstream_client.request_scene_data()
        elif msg is StateMsg.DATA_CAMERA:
            self._view.view_render_scene.load_camera(tpl[1])
        elif msg is StateMsg.DATA_MESH:
            self._view.view_render_scene.load_mesh(tpl[1])
        elif msg is StateMsg.DATA_IMAGE:
            try:
                rendered_image_filepath = self._model.render_info.filepath()
                success = self._view.view_render_image.load_hdr_image(rendered_image_filepath)
                if success:
                    self._view.view_render_image.enable_view(True)
                    self.save_options({'rendered_image_filepath': rendered_image_filepath})
            except Exception as e:
                self._view.view_popup.error_no_output_filepath(str(e))
        elif msg is StateMsg.DATA_RENDER:
            if not tpl[1].valid_sample_count():
                self._view.view_popup.error_no_sample_idx_set("")
                return None

            threads = list()
            threads.append(threading.Thread(
                target=self._view.view_render_scene.load_traced_paths,
                args=(tpl[1],)))

            threads.append(threading.Thread(
                target=self._model.create_scatter_plot,
                args=()))

            for thread in threads:
                thread.setDaemon(True)
                thread.start()

            self._view.view_render_data.init_data(tpl[1])
            self._view.view_filter.init_data(tpl[1])
            self._view.enable_filter(True)
            self._view.view_render_data.enable_view(True)
            self._model.plugins_handler.init_data(tpl[1])

            for thread in threads:
                thread.join()

            threads.clear()

        elif msg is StateMsg.DATA_SCATTER_PLOT:
            self._view.view_plot.plot_final_estimate(tpl[1])
            # check if detector is enabled and run outlier detection
            detector = self._model.detector
            if detector.is_active:
                self.run_detector(detector)
            # run filter
            if self._view.view_filter.is_active():
                render_data = self._model.render_data
                xs = self._model.filter.apply_filters(render_data)
                self.update_path(xs, False)
        elif msg is StateMsg.DATA_NOT_VALID:
            logging.info("data not valid")
            pass
        elif msg is StateMsg.QUIT:
            self._sstream_client.wait()
            self._sstream_client.shutdown()
        elif msg is StateMsg.UPDATE_PLUGIN:
            plugin = self._model.plugins_handler.get_plugin_by_flag(tpl[1])
            if plugin:
                plugin.update_view()

    @Slot(bool, name='disconnect_socket_stream')
    def disconnect_socket_stream(self, disconnected):
        """
        Disconnects the client from the server
        :param disconnected:
        :return:
        """
        if self._sstream_client:
            logging.info('Handle Disconnect ...')
            self._sstream_client.disconnect_stream()

    def connect_socket_stream(self, hostname, port):
        """
        Connects the client to the given hostname:port.
        Establishes the connection and starts the Thread,
        which is listening for incoming messages (backend)
        :param hostname:
        :param port:
        :return:
        """
        self._model.options_data.set_last_hostname_and_port(hostname, port)
        self._sstream_client = SocketStreamClient(port=port,
                                                  hostname=hostname,
                                                  model=self._model,
                                                  callback=self.handle_state_msg)

        is_connected, error_msg = self._sstream_client.connect_stream()
        if not is_connected and error_msg:
            self._view.view_popup.server_error(error_msg)
            return is_connected

        self._sstream_client.start()
        return is_connected

    def load_image_dialog(self, triggered):
        """
        Opens a view for loading an image.
        Loads an HDR (.exr) image into the view render image view
        :param triggered:
        :return:
        """
        dialog = QFileDialog()
        dialog.setNameFilters(['*.exr'])
        dialog.setDefaultSuffix('.exr')

        if dialog.exec() == QFileDialog.Accepted:
            filepath = dialog.selectedFiles()[0]
            if self._view.view_render_image.load_hdr_image(filepath):
                self._view.view_render_image.enable_view(True)
                self.save_options({'rendered_image_filepath': filepath})

    def request_render_info(self):
        """
        Requests the render info data from the server interface
        :return:
        """
        self._sstream_client.request_render_info()

    def request_render_image(self):
        """
        Requests the render image from the server (sends start render call)
        :return:
        """
        self._sstream_client.request_render_image()

    def request_scene_data(self):
        """
        Requests the scene data
        :return:
        """
        self._sstream_client.request_scene_data()

    def request_render_data(self, pixel):
        """
        Sends the selected pixel position to the server
        and requests the render data of this pixel
        :param pixel: (x,y) pixel position
        :return:
        """

        # check if client is connected, if not inform user
        if not self._sstream_client:
            self._view.view_popup.error_not_connected("")
            return None

        # is called every time if new pixel data is requested
        self.prepare_new_data()

        pixmap = self._view.view_render_image.pixmap
        pixel_info = self._model.pixel_info
        pixel_info.set_pixel(pixmap, pixel)
        sample_count = self._model.render_info.sample_count
        self._view.view_emca.update_pixel_hist(pixel_info)
        self._sstream_client.request_render_data(pixel, sample_count)

    def request_plugin(self, flag):
        """
        Handles btn (request) interaction from plugin window,
        Gets the corresponding plugin and sends plugin id request to server
        :param flag: plugin_id
        :return:
        """
        if self._sstream_client.is_connected():
            plugins_handler = self._model.plugins_handler
            plugins_handler.request_plugin(flag, self._sstream_client.stream)

    def send_render_info(self):
        """
        Sends render info data to server.
        Currently updates only the sample count value
        :return:
        """
        self._model.render_info.serialize(self._sstream_client.stream)
        self._view.view_render_info.close()

    def update_render_info_sample_count(self, value):
        """
        Updates the sample count value of render info
        :param value: sample_count
        :return:
        """
        render_info = self._model.render_info
        render_info.set_sample_count(value)

    def prepare_new_data(self):
        """
        Prepare view and model for new incoming pixel render data
        (In most cases clear views and data for new incoming render data)
        :return:
        """
        self._view.view_render_scene.prepare_new_data()
        self._view.view_render_data.prepare_new_data()
        self._view.view_filter.prepare_new_data()
        self._model.prepare_new_data()
        self._indices = np.array([], dtype=np.int32)

    def update_path(self, indices, add_item):
        """
        Brushing and linking function,
        handles selected path indices,
        add_item informs if the next incoming index should be added to the current list or not
        :param indices: numpy array with path indices
        :param add_item: true or false
        :return:
        """

        if add_item:
            # add item to current indices array and update
            self._indices = np.unique(np.append(self._indices, indices))
        else:
            # just update whole indices array
            self._indices = indices

        # mark scatter plot
        self._view.view_plot.update_path_indices(self._indices)
        # draw 3d paths
        self._view.view_render_scene.display_traced_paths(self._indices)
        # update render data view
        self._view.view_render_data.display_traced_path_data(self._indices)
        # update all plugins
        self._model.plugins_handler.update_path_indices(self._indices)
        # select first path
        if np.size(self._indices) == 1:
            self.select_path(self._indices[0])

    def select_path(self, index):
        """
        Send path index update to all views
        :param index: path_index
        :return:
        """
        # this index must be an element of indices
        self._view.view_render_scene.select_path(index)
        # select path in render data view
        self._view.view_render_data.select_path(index)
        # send path index, update plugins
        self._model.plugins_handler.select_path(index)

    def select_vertex(self, tpl):
        """
        Send vertex index update to all views
        :param tpl: (path_index, vertex_index)
        :return:
        """
        # parent idx must be an element of indices

        # select vertex in 3D scene
        self._view.view_render_scene.select_vertex(tpl)
        # select vertex in render data view
        self._view.view_render_data.select_vertex(tpl)
        # send vertex index, update plugins
        self._model.plugins_handler.select_vertex(tpl)

    def load_pre_options(self):
        options = self._model.options_data
        # handle auto connect
        last_hostname = 'localhost'
        last_port = 50013
        if options.is_last_hostname_set():
            last_hostname = options.get_last_hostname()
        if options.is_last_port_set():
            last_port = options.get_last_port()
        # update connect view about last settings
        self._view.view_connect.set_hostname_and_port(last_hostname, last_port)
        if options.get_option_auto_connect():
            self.connect_socket_stream(last_hostname, last_port)
        if options.get_option_auto_image_load():
            filepath = options.get_last_rendered_image_filepath()
            success = False
            try:
                success = self._view.view_render_image.load_hdr_image(filepath)
            except Exception as e:
                logging.error(e)
                self._view.view_popup.error_on_loading_pre_saved_image(str(e))
            if success:
                self._view.view_render_image.enable_view(True)
                self._view.view_render_image.reset(True)

    def apply_theme(self, theme):
        self._view.view_plot.apply_theme(theme)
        self._model.plugins_handler.apply_theme(theme)

    def display_view(self):
        """
        Opens and shows the EMCA view
        :return:
        """
        self._view.show()
        self.load_pre_options()

    def close_app(self):
        """
        Closes all views and disconnected the client from the server (hard shut down)
        Server will be shutdown too.
        :return:
        """
        # close all views
        self._model.plugins_handler.close()
        self._view.view_render_info.close()
        self._view.view_detector.close()
        self._view.view_connect.close()
        self._view.view_render_scene.close()
        self._view.view_filter.close()
        self._view.close()
        # handle disconnect from server if socket connection is still active
        if self._sstream_client:
            self._sstream_client.close()

    def update_and_run_detector(self, m, alpha, k, pre_filter, is_default, is_active):
        """
        Saves all user changes of the detector
        :param m:
        :param alpha:
        :param k:
        :param pre_filter:
        :param is_default:
        :param is_active:
        :return:
        """
        detector = self._model.detector
        detector.update_values(m, alpha, k, pre_filter, is_default, is_active)
        # run detector if client is connected to server
        if self._sstream_client.is_connected():
            self.run_detector(detector)

    def run_detector(self, detector):
        """
        Only runs the detector if the checkbox for the detector is active,
        moreover the final estimate data is needed in order to detector outliers
        :param detector:
        :return:
        """
        if detector.is_active:
            if self._model.li_plot_data:
                data = self._model.li_plot_data.mean
                detector.run_outlier_detection(data=data)
                self.update_path(detector.path_outlier_key_list, False)
            else:
                self._view.view_popup.error_no_final_estimate_data("")

    def add_filter(self, filter_settings):
        """
        Adds a new filter to the current render data
        :param filter_settings:
        :return:
        """
        self._view.view_filter.add_filter_to_view(filter_settings)
        render_data = self._model.render_data
        xs = self._model.filter.filter(filter_settings, render_data)
        if xs is None:
            logging.error("Issue with filter ...")
            return
        self.update_path(xs, False)

    def apply_filters(self):
        """
        Applies all current active filters to the current render data
        :return:
        """
        render_data = self._model.render_data
        xs = self._model.filter.apply_filters(render_data)
        self.update_path(xs, False)

    def clear_filter(self):
        """
        Clears the filter entries
        :return:
        """
        self._model.filter.clear_all()
        self._view.view_filter.filterList.clear()

    def delete_filter(self, item):
        """
        Deletes the marked filter and updates the filtered render data.
        Paths which were deleted by the selected filter will be displayed again
        :param item: filter list item
        :return:
        """
        w = self._view.view_filter.filterList.itemWidget(item)
        row = self._view.view_filter.filterList.row(item)
        i = self._view.view_filter.filterList.takeItem(row)
        xs = self._model.filter.delete_filter(w.get_idx())
        self.update_path(xs, False)
        del i

    def open_options(self, clicked):
        options = self._model.options_data
        theme = options.get_theme()
        # default dark otherwise light
        if theme == 'light':
            self._view.view_options.enable_light_theme(True)
        else:
            self._view.view_options.enable_dark_theme(True)

        self._view.view_options.set_auto_connect(options.get_option_auto_connect())
        self._view.view_options.set_auto_scene_load(options.get_option_auto_scene_load())
        self._view.view_options.set_auto_image_load(options.get_option_auto_image_load())
        self._view.view_options.show()

    def save_options(self, options_dict):
        try:
            theme_changed = False
            options = self._model.options_data
            if 'theme' in options_dict:
                if options.get_theme() != options_dict['theme']:
                    theme_changed = True
            if 'auto_connect' in options_dict:
                options.set_options_auto_connect(options_dict['auto_connect'])
            if 'auto_scene_load' in options_dict:
                options.set_option_auto_scene_load(options_dict['auto_scene_load'])
            if 'rendered_image_filepath' in options_dict:
                options.set_last_rendered_image_filepath(options_dict['rendered_image_filepath'])
            if 'auto_rendered_image_load' in options_dict:
                options.set_option_auto_image_load(options_dict['auto_rendered_image_load'])
            # restart application if user user presses ok
            if theme_changed:
                from PySide2.QtWidgets import QMessageBox
                retval = self._view.view_popup.restart_application_info("Theme change in progress ...")
                if retval == QMessageBox.Ok:
                    options.set_theme(options_dict['theme'])
                    options.save()
                    import sys
                    python = sys.executable
                    os.execl(python, python, *sys.argv)
            else:
                options.save()
        except Exception as e:
            logging.error(e)
            self._view.view_popup.error_saving_options(str(e))
            return
        if self._view.view_options.isVisible():
            self._view.view_options.close()




