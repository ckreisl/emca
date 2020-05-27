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

from View.DataView.tree_node_items import PathNodeItem
from View.DataView.tree_node_items import VertexNodeItem

from Core.pyside2_uic import loadUi
from PySide2.QtWidgets import QWidget
from PySide2.QtWidgets import QTreeWidgetItem
from PySide2.QtCore import Slot
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QAbstractItemView
import numpy as np
import os
import logging


class ViewRenderData(QWidget):

    """
        ViewRenderData
        Handles the view of the Render data containing all information about the selected pixel and its traced paths.
        Moreover, all user added and CustomData will be visualized here as tree structure.
    """

    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)
        ui_filepath = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'ui', 'render_data.ui'))
        loadUi(ui_filepath, self)

        self.tree.setHeaderLabels(["Item", "Value"])
        self.tree.setColumnWidth(0, 200)
        self._controller = None
        self._render_data = None

        self.tree.currentItemChanged.connect(self.select_tree_item)
        self.tree.setSelectionMode(QAbstractItemView.SingleSelection)

        # connect buttons
        self.btnShowAll.clicked.connect(self.show_all_data)
        self.btnInspect.clicked.connect(self.inspect_selected_paths)
        self.cbExpand.toggled.connect(self.expand_items)

        self._shift_is_pressed = False
        self._selected_indices = np.array([], dtype=np.int32)

        self._handling_selection_signal = False

    def enable_view(self, enabled):
        self.btnShowAll.setEnabled(enabled)
        self.btnInspect.setEnabled(enabled)
        self.cbExpand.setEnabled(enabled)

    def add_selected_index(self, index):
        """
        Adss the index to the selected indices list
        :param index: integer
        :return:
        """
        self._selected_indices = np.append(self._selected_indices, index)

    @Slot(QTreeWidgetItem, QTreeWidgetItem, name='select_tree_item')
    def select_tree_item(self, item, previous):
        """
        Handles if a path or vertex node is selected. Informs the controller about the selected index
        :param item: QTreeWidgetItem
        :return:
        """

        self._handling_selection_signal = True

        #select path or vertex of parent nodes
        while isinstance(item, QTreeWidgetItem):
            if isinstance(item, PathNodeItem) or isinstance(item, VertexNodeItem):
                break

            parent = item.parent()
            if isinstance(parent, QTreeWidgetItem):
                item = parent

        if isinstance(item, PathNodeItem):
            if self._shift_is_pressed:
                self.add_selected_index(item.index)
                item.setSelected(True)
            else:
                self._selected_indices = np.array([item.index], dtype=np.int32)
                self._controller.select_path(item.index)
                #select first vertex of the path on path selection
                self._controller.select_vertex((item.index, 1))
        elif isinstance(item, VertexNodeItem):
            self._controller.select_vertex(item.index_tpl())

        self._handling_selection_signal = True

    @Slot(bool, name='show_all_data')
    def show_all_data(self, clicked):
        """
        Handles the button input of show all data,
        shows all paths traced through the selected pixel.
        :param clicked: boolean
        :return:
        """
        if self._render_data:
            indices = self._render_data.get_indices()
            self._controller.update_path(indices, False)

    @Slot(bool, name='inspect_selected_paths')
    def inspect_selected_paths(self, clicked):
        """
        Handles the button input of inspect,
        removes all other paths except the selected one(s)
        :param clicked: boolean
        :return:
        """
        if self._render_data:
            if np.size(self._selected_indices) > 1:
                self._controller.update_path(np.unique(self._selected_indices), False)
                self._selected_indices = np.array([], dtype=np.int32)
            else:
                item = self.tree.currentItem()
                if isinstance(item, PathNodeItem):
                    self._controller.update_path(np.array([item.index]), False)
                elif isinstance(item, VertexNodeItem):
                    self._controller.update_path(np.array([item.parent_index]), False)

    @Slot(bool, name='expand_items')
    def expand_items(self, state):
        """
        Depending on state, expands the tree view and shows all child items.
        :param state: boolean
        :return:
        """
        if state:
            self.tree.expandAll()
        else:
            self.tree.collapseAll()

    def keyPressEvent(self, key_event):
        """
        Handles a key press event, checks if Shift is pressed to select more nodes
        :param key_event:
        :return:
        """
        if key_event.key() == Qt.Key_Shift:
            self._shift_is_pressed = True
            self.tree.setSelectionMode(QAbstractItemView.MultiSelection)

    def keyReleaseEvent(self, key_event):
        """
        Handles a key release event, check if the Shift key is released
        :param key_event:
        :return:
        """
        if key_event.key() == Qt.Key_Shift:
            self._shift_is_pressed = False
            self.tree.setSelectionMode(QAbstractItemView.SingleSelection)

    def set_controller(self, controller):
        """
        Sets the connection to the controller
        :param controller: Controller
        :return:
        """
        self._controller = controller

    def init_data(self, render_data):
        """
        Saves a reference to the models render data
        :param render_data: DataView
        :return:
        """
        self._render_data = render_data

    def select_path(self, index):
        """
        Select/Highlight a path node depending on the input index
        :param index: integer - path_index
        :return:
        """
        self.tree.blockSignals(True)
        for i in range(0, self.tree.topLevelItemCount()):
            item = self.tree.topLevelItem(i)
            if isinstance(item, PathNodeItem):
                if item.index == index:
                    self.tree.setCurrentItem(item)
                    break
        self.tree.blockSignals(False)

    def select_vertex(self, tpl):
        """
        Select/Highlight a vertex node depending on the input tuple tpl
        :param tpl: tuple(path_index, vertex_index)
        :return:
        """
        self.tree.blockSignals(True)
        for i in range(0, self.tree.topLevelItemCount()):
            item = self.tree.topLevelItem(i)
            if isinstance(item, PathNodeItem):
                if item.index == tpl[0]:
                    for j in range(0, item.childCount()):
                        item_child = item.child(j)
                        if isinstance(item_child, VertexNodeItem):
                            if tpl[0] == item_child.parent_index and tpl[1] == item_child.index:
                                self.tree.setCurrentItem(item_child, 0)
                                break
                    break
        self.tree.blockSignals(False)

    def display_traced_path_data(self, indices):
        """
        Display the data of all paths that are in the list indices
        :param indices: numpy array containing path indices
        :return:
        """
        self.tree.clear()
        path_data_dict = self._render_data.dict_paths
        for i in indices:
            self.add_path_data_node(path_data_dict[i])
        if self.cbExpand.isChecked():
            self.expand_items(True)

    def add_path_data_node(self, path_data):
        """
        Adds path data to a path node
        :param path_data:
        :return:
        """
        path = PathNodeItem(path_data.sample_idx)
        path.setText(0, "Path ({})".format(path_data.sample_idx))
        self.add_path_info_node(path, path_data)
        self.add_vertex_nodes(path, path_data.dict_vertices)
        self.tree.addTopLevelItem(path)

    def add_path_info_node(self, parent, path_data):
        """
        Adds path information data to a path node
        :param parent:
        :param path_data:
        :return:
        """
        path_info = QTreeWidgetItem()
        path_info.setText(0, "Info")
        self.add_child_item_node(path_info, "Sample Index", str(path_data.sample_idx))
        self.add_child_item_node(path_info, "Path Depth", str(path_data.path_depth))
        self.add_child_item_node(path_info, "Final Estimate", str(path_data.final_estimate))
        self.add_child_item_node(path_info, "Origin", str(path_data.path_origin))
        self.add_user_data_to_node(path_info, path_data)
        parent.addChild(path_info)

    def add_vertex_nodes(self, parent, dict_vertices):
        """
        Adds vertex nodes to a path node
        :param parent:
        :param dict_vertices:
        :return:
        """
        for key, vert in dict_vertices.items():
            self.add_vertex_node(parent, vert)

    def add_vertex_node(self, parent, vert):
        """
        Adds a vertex node and all of its information within a node
        :param parent:
        :param vert:
        :return:
        """
        path_vertex = VertexNodeItem(parent.index, vert.depth_idx)
        path_vertex.setText(0, "Vertex ({})".format(vert.depth_idx))
        #self.add_child_item_node(path_vertex, "Index", str(vert.depth_idx))
        self.add_child_item_node(path_vertex, "Position", str(vert.pos))
        if not vert.pos_ne is None:
            self.add_child_item_node(path_vertex, "Pos. NEE", str(vert.pos_ne))
        if not vert.pos_envmap is None:
            self.add_child_item_node(path_vertex, "Pos. Envmap", str(vert.pos_envmap))
        self.add_child_item_node(path_vertex, "Estimate", str(vert.li))
        self.add_user_data_to_node(path_vertex, vert)
        parent.addChild(path_vertex)

    def add_user_data_to_node(self, node, user_data):
        """
        Adds the user and custom data which was added by the user as nodes
        :param node:
        :param user_data:
        :return:
        """
        # insert general data
        for data in user_data.data_list:
            self.add_user_data_dict_to_node(node, data)
        # try to insert custom data
        for key, custom_data in user_data.dict_custom_data.items():
            node.addChild(custom_data.init_custom_data_node())

    def add_user_data_dict_to_node(self, node, dict_data):
        """
        Adds added user data as nodes
        :param node:
        :param dict_data:
        :return:
        """
        for key, value in dict_data.items():
            self.add_child_item_node(node, str(key), str(value[0]))

    def add_child_item_node(self, parent, name, value):
        """
        Adds a child item to a node parent containing name and value
        :param parent:
        :param name:
        :param value:
        :return:
        """
        item = QTreeWidgetItem()
        item.setText(0, name)
        item.setText(1, value)
        parent.addChild(item)

    def prepare_new_data(self):
        """
        Prepare new data for new incoming data, clears the tree view.
        :return:
        """
        self.tree.clear()
        self._render_data = None
