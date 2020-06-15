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

from view.view_render_data.tree_node_items import PathNodeItem
from view.view_render_data.tree_node_items import IntersectionNodeItem

from core.pyside2_uic import loadUi
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
        Moreover, all user added data will be visualized here as tree structure.
    """

    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)
        ui_filepath = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'ui', 'render_data.ui'))
        loadUi(ui_filepath, self)

        self.tree.setHeaderLabels(["Item", "Value"])
        self.tree.setColumnWidth(0, 200)
        self._controller = None

        self.tree.currentItemChanged.connect(self.select_tree_item)
        self.tree.setSelectionMode(QAbstractItemView.SingleSelection)

        # connect buttons
        self.btnShowAll.clicked.connect(self.show_all_traced_paths)
        self.btnInspect.clicked.connect(self.inspect_selected_paths)
        self.cbExpand.toggled.connect(self.expand_items)

        self._shift_is_pressed = False
        self._selected_indices = np.array([], dtype=np.int32)

    def set_controller(self, controller):
        """
        Sets the connection to the controller
        :param controller: Controller
        :return:
        """
        self._controller = controller

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

    def show_path_data(self, indices, render_data):
        """
        Load path render data depending on indices input
        :param indices: np.array([])
        :param render_data: RenderData
        :return:
        """
        self.tree.clear()
        for i in indices:
            self.add_path_data_node(render_data.dict_paths[i])
        self.expand_items(self.cbExpand.isChecked())

    @Slot(bool, name='show_all_traced_paths')
    def show_all_traced_paths(self, clicked):
        self._controller.show_all_traced_paths(True)

    @Slot(QTreeWidgetItem, QTreeWidgetItem, name='select_tree_item')
    def select_tree_item(self, item, previous):
        """
        Handles if a path or intersection node is selected. Informs the controller about the selected index
        :param item: QTreeWidgetItem
        :return:
        """
        # select path or intersection of parent nodes
        while isinstance(item, QTreeWidgetItem):
            if isinstance(item, PathNodeItem) or isinstance(item, IntersectionNodeItem):
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
                # select first intersection of the path on path selection
                self._controller.select_intersection((item.index, 1))
        elif isinstance(item, IntersectionNodeItem):
            self._controller.select_intersection(item.index_tpl())

    @Slot(bool, name='inspect_selected_paths')
    def inspect_selected_paths(self, clicked):
        """
        Handles the button input of inspect,
        removes all other paths except the selected one(s)
        :param clicked: boolean
        :return:
        """
        if np.size(self._selected_indices) > 1:
            self._controller.update_path(np.unique(self._selected_indices), False)
            self._selected_indices = np.array([], dtype=np.int32)
        else:
            item = self.tree.currentItem()
            if isinstance(item, PathNodeItem):
                self._controller.update_path(np.array([item.index]), False)
            elif isinstance(item, IntersectionNodeItem):
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

    def select_intersection(self, tpl):
        """
        Select/Highlight a intersection node depending on the input tuple tpl
        :param tpl: tuple(path_index, intersection_index)
        :return:
        """
        self.tree.blockSignals(True)
        for i in range(0, self.tree.topLevelItemCount()):
            item = self.tree.topLevelItem(i)
            if isinstance(item, PathNodeItem):
                if item.index == tpl[0]:
                    for j in range(0, item.childCount()):
                        item_child = item.child(j)
                        if isinstance(item_child, IntersectionNodeItem):
                            if tpl[0] == item_child.parent_index and tpl[1] == item_child.index:
                                self.tree.setCurrentItem(item_child, 0)
                                break
                    break
        self.tree.blockSignals(False)

    def add_path_data_node(self, path_data):
        """
        Adds path data to a path node
        :param path_data:
        :return:
        """
        path = PathNodeItem(path_data.sample_idx)
        path.setText(0, "Path ({})".format(path_data.sample_idx))
        self.add_path_info_node(path, path_data)
        self.add_intersection_nodes(path, path_data.intersections)
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

    def add_intersection_nodes(self, parent, intersections):
        """
        Adds intersection nodes to a path node
        :param parent:
        :param intersections:
        :return:
        """
        for _, its in intersections.items():
            self.add_intersection_node(parent, its)

    def add_intersection_node(self, parent, its):
        """
        Adds a intersection node and all of its information within a node
        :param parent:
        :param its: Intersection
        :return:
        """
        its_node = IntersectionNodeItem(parent.index, its.depth_idx)
        its_node.setText(0, "Intersection ({})".format(its.depth_idx))
        self.add_child_item_node(its_node, "Position", str(its.pos))
        if its.pos_ne is not None:
            self.add_child_item_node(its_node, "Pos. NEE", str(its.pos_ne))
        if its.pos_envmap is not None:
            self.add_child_item_node(its_node, "Pos. Envmap", str(its.pos_envmap))
        self.add_child_item_node(its_node, "Estimate", str(its.li))
        self.add_user_data_to_node(its_node, its)
        parent.addChild(its_node)

    def add_user_data_to_node(self, node, user_data):
        """
        Adds the user data which was added by the user as nodes
        :param node:
        :param user_data:
        :return:
        """
        # insert general data
        for data in user_data.data_list:
            self.add_user_data_dict_to_node(node, data)

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
