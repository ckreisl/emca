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

from PyQt5.QtWidgets import QTreeWidgetItem
import logging
import abc


class CustomData(object):

    """
        CustomData Base class, all other custom data have to inheriate from this base class.
        Allows to visualize custom data within the render data view (debugger tree view)
        Therefore deserialize and create_custom_node have to be implemented.
        Moreover the new CustomData class has to be imported within CustomData/__init__.py and added in __all__
    """

    def __init__(self, unique_id):

        self._id = unique_id
        self._name = 'not set'
        self._root = QTreeWidgetItem()

    @property
    def id(self):
        """
        Returns the unique identifier of the custom data
        :return:
        """
        return self._id

    @property
    def name(self):
        """
        Returns the name of the custom data.
        The name is set from the deserialized data from the server
        :return:
        """
        return self._name

    @name.setter
    def name(self, new_name):
        """
        Sets the name of the custom data class
        :param new_name:
        :return:
        """
        self._name = new_name

    @abc.abstractmethod
    def deserialize(self, msg_len, stream):
        """

        :param msg_len:
        :param stream:
        :return:
        """
        pass

    @abc.abstractmethod
    def create_custom_node(self):
        """
        Must be implemented by the user
        Add data to the root node with the provided functions of this class
        Is used to visualize data within render data view (debugger tree view)
        :return:
        """
        pass

    def add_node_to_root(self, node):
        """
        Adds a node to the root node,
        the root node is just a node with the class name
        :param node:
        :return:
        """
        self._root.addChild(node)

    def add_data_to_root(self, name, value):
        """
        Adds data to the root node,
        the root node is just a node with the class name
        :param name:
        :param value:
        :return:
        """
        child = QTreeWidgetItem()
        child.setText(0, str(name))
        child.setText(1, str(value))
        self._root.addChild(child)

    def create_node(self, name):
        """
        Returns a new node with inserted name
        Is used to append a node to the root node
        :param name:
        :return:
        """
        node = QTreeWidgetItem()
        node.setText(0, str(name))
        return node

    def add_data_to_node(self, node, name, value):
        """
        Adds data to node,
        Should be used if a new node is created with create_node,
        and therefore data should be inserted
        :param node:
        :param name:
        :param value:
        :return:
        """
        child = QTreeWidgetItem()
        child.setText(0, str(name))
        child.setText(1, str(value))
        node.addChild(child)

    def init_custom_data_node(self):
        """
        Do not call this function!
        Will be called from EMCA to insert the data within the render data view
        :return:
        """
        self._root = QTreeWidgetItem()
        self._root.setText(0, self._name)
        try:
            self.create_custom_node()
        except Exception as e:
            logging.error("Failed to create custom data node ({}): {}".format(self.name, e))
        return self._root
