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
