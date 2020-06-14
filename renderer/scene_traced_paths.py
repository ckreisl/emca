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

from renderer.path import Path
import numpy as np
import time
import logging


class SceneTracedPaths(object):

    def __init__(self, opacity):

        self._path_opacity = opacity
        self._path_size = 1.0

        self._paths = {}
        self._path_indices = np.array([], dtype=np.int32)
        self._prev_path = None
        self._prev_intersection = None
        self._is_path_selected = False
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
    def all_paths_visible(self):
        return self._all_paths_visible

    @all_paths_visible.setter
    def all_paths_visible(self, visible):
        self._all_paths_visible = visible

    @property
    def all_nees_visible(self):
        return self._all_nees_visible

    @all_nees_visible.setter
    def all_nees_visible(self, visible):
        self._all_nees_visible = visible

    @property
    def all_vertices_visible(self):
        return self._all_vertices_visible

    @all_vertices_visible.setter
    def all_vertices_visible(self, visible):
        self._all_vertices_visible = visible

    def get_path(self, path_index):
        return self._paths.get(path_index, None)

    def get_intersection(self, vertex_tpl):
        path = self.get_path(vertex_tpl[0])
        return path.its_dict.get(vertex_tpl[1], None)

    def get_path_and_intersection(self, tpl):
        path = self._paths[tpl[0]]
        intersection = path.its_dict[tpl[1]]
        return path, intersection

    def select_path(self, index):
        if self._prev_path is None:
            self._prev_path = self._paths.get(index, None)
        if self._prev_path is not None:
            self._prev_path.is_path_selected = False
            self._prev_path = self._paths.get(index, None)
        self._is_path_selected = True

    def select_vertex(self, tpl):
        # tpl = (path_idx, vertex_idx)
        intersection = self.get_intersection(tpl)
        if self._prev_intersection is None:
            self._prev_intersection = intersection
        if self._prev_intersection is not None:
            self._prev_intersection.set_selected(False)
            self._prev_intersection = intersection
        intersection.set_selected(True)

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
        self._prev_path = None
        self._prev_intersection = None
        self._is_path_selected = False
        self._all_paths_visible = False
        self._all_vertices_visible = False
        self._all_nees_visible = False

