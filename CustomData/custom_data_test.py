from CustomData.custom_data_base import CustomData
import logging


class CustomDataTest(CustomData):

    """
    CustomDataTest

    Example how to use and add CustomData
    """

    def __init__(self):
        CustomData.__init__(self, 256)

        self._x = 0
        self._y = 0

    def deserialize(self, msg_len, stream):
        """
        Deserialize the data from the socket stream
        :param msg_len:
        :param stream:
        :return:
        """
        self._x = stream.read_int()
        self._y = stream.read_int()

    def create_custom_node(self):
        """
        Add data for visualization in view render data
        add...(description, value)
        :return:
        """
        self.add_data_to_root("x", self._x)
        self.add_data_to_root("y", self._y)
