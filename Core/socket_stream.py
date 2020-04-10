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

from Core.stream import Stream
import socket
import logging


class SocketStream(Stream):
    """
    Socket Stream inheriates from Stream

    Handles Port, Hostname and Socket.
    Handles read and write from Socket Stream pipeline
    """

    def __init__(self, port, hostname=None):
        Stream.__init__(self)
        logging.info("Starting SocketStream ...")
        self._port = port
        self._hostname = hostname or socket.gethostname()
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect((self._hostname, self._port))

    @property
    def port(self):
        """
        Returns the port of the socket stream connection
        :return:
        """
        return self._port

    @property
    def hostname(self):
        """
        Returns the hostname of the socket stream connection
        :return:
        """
        return self._hostname

    @property
    def socket(self):
        """
        Returns the socket
        :return:
        """
        return self._socket

    def disconnect(self):
        """
        Closes the socket and disconnects from the server
        :return:
        """
        logging.info('Disconnecting from {} with port: {}'.format(self._hostname, self._port))
        try:
            self._socket.close()
            self._socket = None
        except socket.error as e:
            logging.error("Socket error {}".format(e))
        except Exception as e:
            logging.error("Exception {}".format(e))

    def read(self, size):
        """
        Reads size bytes from the socket stream pipeline
        :param size: package size
        :return:
        """
        try:
            data = b''
            while len(data) < size:
                chunk = self._socket.recv(size - len(data))
                if chunk == b'':
                    raise RuntimeError('Socket connection broken')
                data += chunk
            return data
        except ConnectionResetError as e:
            logging.error(e)

    def write(self, data, size):
        """
        Writes data onto the socket stream
        :param data:
        :param size:
        :return:
        """
        try:
            total_sent = 0
            while total_sent < size:
                sent = self._socket.send(data[total_sent:])
                if sent == 0:
                    raise RuntimeError('Socket connection broken')
                total_sent += sent
        except BrokenPipeError as e:
            logging.error(e)
