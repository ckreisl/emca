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

from PySide2.QtCore import QThread
from Core.socket_stream import SocketStream
from Core.messages import ServerMsg
from Core.messages import StateMsg
from PySide2.QtCore import Signal
import logging


class SocketStreamClient(QThread):

    """
    Socket Stream Client (QThread)

    Handles all incoming messages from the server and sends them via a Qt Signal to the controller.
    Incoming data is deserialized within this thread.
    """

    _sendStateMsgSig = Signal(tuple)

    def __init__(self, port, hostname):
        QThread.__init__(self)
        # init socket stream
        self._stream = SocketStream(port=port, hostname=hostname)
        # model will be used to deserialize data within this thread
        self._model = None
        # bool to check an open socket connection
        self._is_connected = False

    def set_model(self, model):
        """
        Set Model / Dataset
        """
        self._model = model

    def set_callback(self, callback):
        # callback function (QtSlot) to controller msg handler
        self._sendStateMsgSig.connect(callback)

    @property
    def stream(self):
        """
        Return socket stream connection
        """
        return self._stream

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

    def request_disconnect(self):
        """
        Sends disconnect signal to server
        :return:
        """
        self._stream.write_short(ServerMsg.EMCA_DISCONNECT.value)

    def is_connected(self):
        """
        Returns true when there is a open socket connection
        """
        return self._stream.is_connected()

    def connect_socket_stream(self, hostname, port):
        """
        Connects the socket stream and returns if successful
        :return: True|False, None|ErrorMsg
        """
        self._stream.hostname = hostname
        self._stream.port = port
        return self._stream.connect()

    def disconnect_socket_stream(self):
        """
        Shutdown / Disconnect the SocketStream and returns if successful
        :return: True|False, None|ErrorMsg
        """
        return self._stream.disconnect()

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
        logging.info('Start SocketStreamClient ...')

        # Next few lines handle the handshake protocol with the server
        msg = self._stream.read_short()

        state = ServerMsg.get_server_msg(msg)

        if state is not ServerMsg.EMCA_HELLO:
            logging.error('Received wrong handshake message from server')
            self._stream.write_short(ServerMsg.EMCA_QUIT.value)
            return None

        self._stream.write_short(ServerMsg.EMCA_HELLO.value)
        # Handshake complete, set StateMsg to controller to enable views
        self._sendStateMsgSig.emit((StateMsg.CONNECT, None))

        while True:

            try:
                # read header of message (message identifier)
                msg = self._stream.read_short()
            except RuntimeError as e:
                logging.error(e)
                break
            except Exception as e:
                logging.error(e)
                break

            # check if message is a plugin
            plugin = self._model.plugins_handler.get_plugin_by_flag(msg)
            state = ServerMsg.get_server_msg(msg)

            logging.info('msg={} is state={} or plugin={}'.format(msg, state, plugin))

            if plugin:
                plugin.deserialize(stream=self._stream)
                self._sendStateMsgSig.emit((StateMsg.UPDATE_PLUGIN, plugin.flag))
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

        logging.info("Shutdown SocketStreamClient Thread ...")
