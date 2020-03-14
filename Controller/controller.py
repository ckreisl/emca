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

from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QFileDialog
from Core.messages import StateMsg
from Core.messages import ViewMode
from Core.socket_stream import SocketStream
from Core.socket_stream_backend import SocketStreamBackend
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
        self._view.view_emca.set_controller(self)
        self._view.view_plot.set_controller(self)
        self._view.view_render_scene.set_controller(self)
        self._view.view_render_data.set_controller(self)
        self._view.view_render_image.set_controller(self)
        self._view.view_render_info.set_controller(self)
        self._view.view_connect.set_controller(self)
        self._view.view_detector.set_controller(self)
        self._view.view_filter.set_controller(self)

        # set connection between model and controller
        self._model.set_controller(self)
        self._model.tool_handler.set_controller(self)
        self._model.sendStateMsgSig.connect(self.handle_state_msg)

        # set tool btn
        tools = self._model.tool_handler.tools
        self._view.view_emca.add_tools(tools)

        # controller keeps track of current selected path indices
        self._indices = np.array([], dtype=np.int32)

        self._stream = None
        self._sstream_backend = None

        self.init_view()

    def init_view(self):
        """
        Init all views with parameters from the model (dataset)
        :return:
        """
        # init detector view with values from detector class
        detector = self._model.detector
        self._view.view_detector.init_values(detector)

    @property
    def indices(self):
        return self._indices

    @pyqtSlot(tuple, name='handle_state_msg')
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
            self._sstream_backend.request_render_info()
            self._view.view_emca.enable_view(True)
            self._view.view_render_scene.enable_view(True)
            self._model.tool_handler.enable_tools(True)
        elif msg is StateMsg.DISCONNECT:
            self._view.view_emca.enable_view(False)
            self._view.view_render_image.enable_view(False)
            self._view.view_render_scene.enable_view(False)
            self._model.tool_handler.enable_tools(False)
            self._stream.disconnect()
            self._sstream_backend = None
            self._stream = None
        elif msg is StateMsg.DATA_INFO:
            self._view.view_render_info.update_render_info(tpl[1])
            #automatically request scene data once render info is available
            self._view.view_render_scene.remove_scene_objects()
            self._sstream_backend.request_scene_data()
        elif msg is StateMsg.DATA_CAMERA:
            self._view.view_render_scene.load_camera(tpl[1])
        elif msg is StateMsg.DATA_MESH:
            self._view.view_render_scene.load_mesh(tpl[1])
        elif msg is StateMsg.DATA_IMAGE:
            self._view.view_render_image.load_hdr_image(
                self._model.render_info.filepath()
            )
        elif msg is StateMsg.DATA_RENDER:
            if not tpl[1].valid_sample_count():
                self._view.view_popup.error_no_sample_idx_set("")
                return None

            threads = list()
            threads.append(threading.Thread(
                target=self._view.view_render_scene.load_traced_paths,
                args=(tpl[1],)
            ))

            threads.append(threading.Thread(
                target=self._model.create_scatter_plot,
                args=()
            ))

            for thread in threads:
                thread.setDaemon(True)
                thread.start()

            self._view.view_render_data.init_data(tpl[1])
            self._view.view_filter.init_data(tpl[1])
            self._view.enable_filter(True)
            self._model.tool_handler.init_data(tpl[1])

            for thread in threads:
                thread.join()

            threads.clear()

        elif msg is StateMsg.DATA_SCATTER_PLOT:
            t1 = threading.Thread(
                target=self._view.view_plot.plot_final_estimate,
                args=(tpl[1],)
            )

            t1.start()
            t1.join()

            # check if detector is enabled and run outlier detection
            detector = self._model.detector
            if detector.is_active:
                self.run_detector(detector)
            # run filter
            if self._view.view_filter.is_active():
                render_data = self._model.render_data
                xs = self._model.filter.apply_filters(render_data)
                self.update_path(xs, False)
        elif msg is StateMsg.XML_LOADED:
            self.prepare_new_data()
            logging.info("xml file loaded")
            """
                todo: test and verify
                still experimental to save / load current state via xml
            """
            filepath = self._model.render_info.output_filepath
            if not filepath.endswith(".exr"):
                filepath = filepath + ".exr"
            self._view.view_render_image.load_hdr_image(filepath)
            self._view.view_render_info.update_render_info(self._model.render_info)

            self._view.view_emca.enable_view(True, ViewMode.XML)
            self._view.view_render_scene.enable_view(True, ViewMode.XML)
            self._model.tool_handler.enable_tools(True)

            threading.Thread(
                target=self._view.view_render_scene.load_scene,
                args=(self._model.camera_data, self._model.mesh_data)
            ).start()

            threads = list()
            threads.append(threading.Thread(
                target=self._view.view_render_scene.load_traced_paths,
                args=(self._model.render_data,)
            ))

            threads.append(threading.Thread(
                target=self._model.create_scatter_plot,
                args=()
            ))

            for thread in threads:
                thread.setDaemon(True)
                thread.start()

            self._view.view_emca.update_pixel_hist(self._model.pixel_info)
            self._view.view_render_data.init_data(self._model.render_data)
            self._model.tool_handler.init_data(self._model.render_data)
            self._view.view_filter.init_data(self._model.render_data)

            for thread in threads:
                thread.join()

            threads.clear()
        elif msg is StateMsg.DATA_NOT_VALID:
            logging.info("data not valid")
            pass
        elif msg is StateMsg.QUIT:
            self._sstream_backend.wait()
            self._stream.disconnect()
        elif msg is StateMsg.UPDATE_TOOL:
            tool = self._model.tool_handler.get_tool_by_flag(tpl[1])
            if tool:
                tool.update_view()

    @pyqtSlot(bool, name='handle_disconnect')
    def handle_disconnect(self, disconnected):
        """
        Disconnects the client from the server
        :param disconnected:
        :return:
        """
        if self._sstream_backend and self._stream:
            logging.info('Handle Disconnect ...')
            self._sstream_backend.disconnect_stream()

    def handle_connect(self, hostname, port):
        """
        Connects the client to the given hostname:port.
        Establishes the connection and starts the Thread,
        which is listening for incoming messages (backend)
        :param hostname:
        :param port:
        :return:
        """

        logging.info('connect {}:{}'.format(hostname, port))
        try:
            self._stream = SocketStream(hostname=hostname, port=port)
        except Exception as e:
            # server is not running
            self._view.view_popup.server_error(str(e))
            logging.error(e)
            return None

        self._sstream_backend = SocketStreamBackend(stream=self._stream,
                                                    model=self._model,
                                                    controller=self)
        self._sstream_backend.start()

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
            self._view.view_render_image.load_hdr_image(
                dialog.selectedFiles()[0])

    def load_xml(self, clicked):
        """
        Loads render data from a xml file
        :param clicked:
        :return:
        """
        dialog = QFileDialog()
        dialog.setNameFilters(['*.xml'])
        dialog.setDefaultSuffix('.xml')

        if dialog.exec() == QFileDialog.Accepted:
            threading.Thread(target=self._model.read_xml,
                             args=(dialog.selectedFiles()[0],)).start()

    def save_xml(self, clicked):
        """
        Saves the current render data within an xml file
        :param clicked:
        :return:
        """
        dialog = QFileDialog()
        path = dialog.getSaveFileName(
            self._view,
            'Save xml',
            os.getenv('HOME'),
            filter='xml (*.xml)')
        if path:
            threading.Thread(target=self._model.write_xml,
                             args=(path[0],)).start()

    def request_render_info(self):
        """
        Requests the render info data from the server interface
        :return:
        """
        self._sstream_backend.request_render_info()

    def request_render_image(self):
        """
        Requests the render image from the server (sends start render call)
        :return:
        """
        self._sstream_backend.request_render_image()

    def request_scene_data(self):
        """
        Requests the scene data
        :return:
        """
        self._sstream_backend.request_scene_data()

    def request_render_data(self, pixel):
        """
        Sends the selected pixel position to the server
        and requests the render data of this pixel
        :param pixel: (x,y) pixel position
        :return:
        """

        # check if client is connected, if not inform user
        if not self._sstream_backend:
            self._view.view_popup.error_not_connected("")
            return None

        # is called every time if new pixel data is requested
        self.prepare_new_data()

        pixmap = self._view.view_render_image.pixmap
        pixel_info = self._model.pixel_info
        pixel_info.set_pixel(pixmap, pixel)
        sample_count = self._model.render_info.sample_count
        self._view.view_emca.update_pixel_hist(pixel_info)
        self._sstream_backend.request_render_data(pixel, sample_count)

    def request_tool(self, flag):
        """
        Handles btn (request) interaction from tool window,
        Gets the corresponding tool and sends tool id request to server
        :param flag: tool_id
        :return:
        """
        if self._stream:
            tool_handler = self._model.tool_handler
            tool_handler.request_tool(flag, self._stream)

    def send_render_info(self):
        """
        Sends render info data to server.
        Currently updates only the sample count value
        :return:
        """
        render_info = self._model.render_info
        self._sstream_backend.send_render_info(render_info)
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
        #threading.Thread(target=self._view.view_plot.update_path_indices,
        #                 args=(self._indices,)).start()
        # draw 3d paths
        self._view.view_render_scene.display_traced_paths(self._indices)
        #threading.Thread(target=self._view.view_render_scene.display_traced_paths,
        #                 args=(self._indices,)).start()

        # update render data view
        self._view.view_render_data.display_traced_path_data(self._indices)

        # update all tools
        self._model.tool_handler.update_path_indices(self._indices)

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
        #threading.Thread(target=self._view.view_render_scene.select_path,
        #                 args=(index,)).start()

        # select path in render data view
        self._view.view_render_data.select_path(index)

        # send path index, update tools
        self._model.tool_handler.select_path(index)

    def select_vertex(self, tpl):
        logging.info("Tuple: {}".format(tpl))
        """
        Send vertex index update to all views
        :param tpl: (path_index, vertex_index)
        :return:
        """
        # parent idx must be an element of indices

        # select vertex in 3D scene
        self._view.view_render_scene.select_vertex(tpl)
        #threading.Thread(target=self._view.view_render_scene.select_vertex,
        #                 args=(tpl,)).start()

        # select vertex in render data view
        self._view.view_render_data.select_vertex(tpl)

        # send vertex index, update tools
        self._model.tool_handler.select_vertex(tpl)

    def display_view(self):
        """
        Opens and shows the EMCA view
        :return:
        """
        self._view.show()

    def close_app(self):
        """
        Closes all views and disconnected the client from the server (hard shut down)
        Server will be shutdown too.
        :return:
        """
        # close all views
        self._model.tool_handler.close()
        self._view.view_render_info.close()
        self._view.view_detector.close()
        self._view.view_connect.close()
        self._view.view_render_scene.close()
        self._view.view_filter.close()
        self._view.close()
        # handle disconnect from server if socket connection is still active
        if self._sstream_backend:
            self._sstream_backend.close()

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
        if self._stream:
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

    def take_screenshot(self, widget):
        """
        Takes a screenshot of the whole visible view widget
        :param widget: view widget
        :return:
        """
        dialog = QFileDialog(widget)
        dialog.setNameFilter("Images (*.png *.jpg)")
        dialog.selectNameFilter("Images (*.png *.jpg)")
        filename = dialog.getSaveFileName(widget)[0]
        if filename:
            pixmap = widget.grab()
            pixmap.save(filename, "png")




