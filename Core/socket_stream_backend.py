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

from PyQt5.QtCore import QThread
from Core.messages import ServerMsg
from Core.messages import StateMsg
from PyQt5.QtCore import pyqtSignal
import logging


class SocketStreamBackend(QThread):

    """
    Socket Stream Backend (QThread)

    Handles all incoming messages from the server and sends them via a Qt Signal to the controller.
    Incoming data is deserialized within this thread.
    """

    _sendStateMsgSig = pyqtSignal(tuple)

    def __init__(self, stream, controller, model, parent=None):
        QThread.__init__(self, parent=parent)

        # socket stream reference
        self._stream = stream
        # holds a reference to the model to deserialize incoming data
        self._model = model

        # connection to the controller
        self._sendStateMsgSig.connect(controller.handle_state_msg)

    def request_render_info(self):
        """
        Requests the render info data package from the server
        :return:
        """
        self._stream.write_short(ServerMsg.EMCA_HEADER_RENDER_INFO.value)

    def request_render_image(self):
        """
        Requests the render image from the server (starts the rendering process)
        :return:
        """
        self._stream.write_short(ServerMsg.EMCA_HEADER_IMAGE_DATA.value)

    def request_scene_data(self):
        """
        Requests the three-dimensional scene data from the server
        :return:
        """
        self._stream.write_short(ServerMsg.EMCA_HEADER_SCENE_DATA.value)

    def request_render_data(self, pixel, sample_count):
        """
        Requests the render data of the selected pixel
        :param pixel: (x,y)
        :param sample_count: sampleCount Integer
        :return:
        """
        logging.info('Request pixel=({},{})'.format(pixel.x(), pixel.y()))
        self._stream.write_short(ServerMsg.EMCA_HEADER_PIXEL_DATA.value)
        self._stream.write_int(int(pixel.x()))
        self._stream.write_int(int(pixel.y()))
        self._stream.write_int(int(sample_count))

    def send_render_info(self, render_info):
        """
        Sends the render info to the server
        :param render_info:
        :return:
        """
        render_info.serialize(stream=self._stream)

    def disconnect_stream(self):
        """
        Sends disconnect signal to server
        :return:
        """
        self._stream.write_short(ServerMsg.EMCA_DISCONNECT.value)

    def close(self):
        """
        Sends hard disconnect to server (client is closed)
        :return:
        """
        self._stream.write_short(ServerMsg.EMCA_QUIT.value)

    def run(self):
        """
        Handles handshake and incoming messages from the server,
        moreover all incoming data packages are called to deserialize.
        The model will inform the controller via a Qt signal after data package deserialization.
        :return:
        """
        logging.info('Start SSBackend ...')

        # Next few lines handle the handshake protocol with the server
        msg = self._stream.read_short()

        state = ServerMsg.get_server_msg(msg)

        if state is not ServerMsg.EMCA_HELLO:
            logging.error('Received wrong handshake message from server')
            self._stream.write_short(ServerMsg.EMCA_QUIT.value)

        self._stream.write_short(ServerMsg.EMCA_HELLO.value)
        # Handshake complete, set StateMsg to controller to enable views
        self._sendStateMsgSig.emit((StateMsg.CONNECT, None))

        running = True

        while running:

            try:
                # read header of message (message identifier)
                msg = self._stream.read_short()
            except RuntimeError as e:
                logging.error(e)
                break

            # check if message is a tool
            tool = self._model.tool_handler.get_tool_by_flag(msg)
            state = ServerMsg.get_server_msg(msg)

            logging.info('msg={} is state={} or tool={}'.format(msg, state, tool))

            if tool:
                tool.deserialize(stream=self._stream)
                self._sendStateMsgSig.emit((StateMsg.UPDATE_TOOL, tool.flag))
            elif state is ServerMsg.EMCA_HEADER_RENDER_INFO:
                self._model.deserialize_render_info(stream=self._stream)
            elif state is ServerMsg.EMCA_HEADER_CAMERA:
                self._model.deserialize_camera(stream=self._stream)
            elif state is ServerMsg.EMCA_HEADER_SCENE_DATA:
                self._model.deserialize_scene_objects(stream=self._stream)
            elif state is ServerMsg.EMCA_HEADER_IMAGE_DATA:
                self._sendStateMsgSig.emit((StateMsg.DATA_IMAGE, None))
            elif state is ServerMsg.EMCA_HEADER_PIXEL_DATA:
                self._model.deserialize_render_data(stream=self._stream)
            elif state is ServerMsg.EMCA_NO_VALID_DATA:
                self._sendStateMsgSig.emit((StateMsg.DATA_NOT_VALID, None))
            elif state is ServerMsg.EMCA_DISCONNECT:
                self._sendStateMsgSig.emit((StateMsg.DISCONNECT, None))
            elif state is ServerMsg.EMCA_QUIT:
                self._sendStateMsgSig.emit((StateMsg.QUIT, None))
                break

        logging.info("Shutdown client-backend thread ...")