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

from Renderer.path import Path
import numpy as np
import time
import logging


class SceneTracedPaths(object):

    def __init__(self, opacity):

        self._path_opacity = opacity
        self._path_size = 1.0

        self._paths = {}
        self._path_indices = np.array([], dtype=np.int32)
        self._is_path_selected = False
        self._selected_path_index = -1
        self._is_vertex_selected = False
        self._selected_vertex_tpl = ()

        self._all_paths_visible = False
        self._all_nees_visible = False
        self._all_vertices_visible = False

    @property
    def paths(self):
        """
        Returns all traced paths within the scene
        """
        return self._paths

    @property
    def path_indices(self):
        """
        Returns the current numpy array of path indices
        """
        return self._path_indices

    @path_indices.setter
    def path_indices(self, indices):
        """
        Returns the current numpy array of path indices
        """
        self._path_indices = indices

    @property
    def is_path_selected(self):
        return self._is_path_selected

    @property
    def selected_path_index(self):
        return self._selected_path_index

    @property
    def is_vertex_selected(self):
        return self._is_vertex_selected

    @property
    def selected_vertex_tpl(self):
        return self._selected_vertex_tpl

    @property
    def all_paths_visible(self):
        return self._all_paths_visible

    @property
    def all_nees_visible(self):
        return self._all_nees_visible

    @property
    def all_vertices_visible(self):
        return self._all_vertices_visible

    def select_path(self, index):
        self._is_path_selected = True
        self._selected_path_index = index

    def select_vertex(self, tpl):
        # tpl = (path_idx, vertex_idx)
        if not self._is_vertex_selected:
            self._is_vertex_selected = True
        if self._selected_vertex_tpl:
            path = self._paths[self._selected_vertex_tpl[0]]
            vertex = path.its_dict[self._selected_vertex_tpl[1]]
            vertex.set_selected(False)
        self._selected_vertex_tpl = tpl
        path = self._paths[tpl[0]]
        vertex = path.its_dict[tpl[1]]
        vertex.set_selected(True)

    def get_path_and_vertex(self, tpl):
        path = self._paths[tpl[0]]
        vertex = path.its_dict[tpl[1]]
        return path, vertex

    def load_traced_paths(self, render_data):
        """
        Initialises the 3D path structure from the render data of the model.
        Necessary for path visualization.
        :param render_data: DataView
        :return:
        """
        start = time.time()
        for key, path in render_data.dict_paths.items():
            self._paths[key] = Path(idx=key,
                                    origin=path.path_origin,
                                    path_data=path,
                                    default_opacity=self._path_opacity,
                                    default_size=self._path_size)
        logging.info("creating traced paths runtime: {}ms".format(time.time() - start))
        return True

    def clear(self):
        """
        Prepare render view for new incoming render data,
        is called if a new pixel is clicked and its corresponding data is computed.
        :return:
        """
        self._paths.clear()
        self._path_indices = np.array([], dtype=np.int32)
        self._is_path_selected = False
        self._selected_path_index = -1
        self._is_vertex_selected = False
        self._selected_vertex_tpl = ()
        self._all_paths_visible = False
        self._all_vertices_visible = False
        self._all_nees_visible = False

