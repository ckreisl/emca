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

from Renderer.ray import Ray
from Renderer.vertex import Vertex
from Renderer.intersection import Intersection
import logging


class Path(object):

    """
        Path
        Visualizes one path in the vtkRenderer (3D viewer)
    """

    def __init__(self, idx, origin, path_data):
        self._path_idx = idx
        self._origin = origin
        self._its_dict = {}

        self._opacity = 1.0
        self._size = 1.0
        self._visible = True
        self._visible_ne = False

        dict_vertices = path_data.dict_vertices

        # start index mitsuba 1 (0 in nori2 framework)
        start_key = next(iter(dict_vertices))
        # algorithm which creates the path from the model vertices data
        for key, vertex in dict_vertices.items():

            if not vertex.is_pos_set:
                if key == start_key and vertex.is_envmap_set:
                    wi = Ray(origin, vertex.pos_envmap, is_envmap=True)
                    self._its_dict[key] = Intersection(key, wi, None, None, None)
                continue

            wi = None
            if key == start_key:
                wi = Ray(origin, vertex.pos)
            else:
                last_vertex = dict_vertices.get(key-1, None)
                if last_vertex:
                    wi = Ray(last_vertex.pos, vertex.pos)

            its = Vertex(idx, key, vertex.pos)

            wo = None
            next_vertex = dict_vertices.get(key+1, None)
            if next_vertex:
                if next_vertex.is_pos_set:
                    wo = Ray(vertex.pos, next_vertex.pos)
                elif next_vertex.is_envmap_set:
                    wo = Ray(vertex.pos, next_vertex.pos_envmap, is_envmap=True)

            if vertex.is_envmap_set:
                wo = Ray(vertex.pos, vertex.pos_envmap, is_envmap=True)

            ne = None
            if vertex.is_ne_set:
                ne = Ray(vertex.pos, vertex.pos_ne, is_ne=True, is_ne_occluded=vertex.is_ne_occluded)

            self._its_dict[key] = Intersection(key, wi, its, wo, ne)

    @property
    def path_idx(self):
        """
        Returns the path index
        :return: integer
        """
        return self._path_idx

    @property
    def origin(self):
        """
        Returns the path origin
        :return: point3f
        """
        return self._origin

    @property
    def its_dict(self):
        """
        Returns a dict containing all path intersection information
        :return: dict{vertex_idx : Intersection, ...}
        """
        return self._its_dict

    @property
    def opacity(self):
        """
        Returns the path opacity
        :return: float[0,1]
        """
        return self._opacity

    @property
    def size(self):
        """
        Returns the path size
        :return: float[0,1]
        """
        return self._size

    @property
    def default_opacity(self):
        """
        Returns the default path opacity 1.0
        :return: float
        """
        return 1.0

    @property
    def default_size(self):
        """
        Returns the default path size 1.0
        :return: float
        """
        return 1.0

    @property
    def is_visible(self):
        """
        Returns if the path is visible
        :return: boolean
        """
        return self._visible

    @is_visible.setter
    def is_visible(self, visible):
        """
        Sets the visibility of the path object
        :param visible:
        :return:
        """
        self._visible = visible
        for key, its in self._its_dict.items():
            its.is_wi_visible = visible

    @property
    def is_ne_visible(self):
        """
        Returns if the next event estimations are visible of the path
        :return: boolean
        """
        return self._visible_ne

    @is_ne_visible.setter
    def is_ne_visible(self, visible):
        """
        Sets the visibility of the next event estimations of the path
        :param visible:
        :return:
        """
        self._visible_ne = visible
        for key, its in self._its_dict.items():
            its.is_ne_visible = visible

    def draw_verts(self, renderer):
        """
        Draws all vertices of the path
        :param renderer: vtkRenderer
        :return:
        """
        for key, its in self._its_dict.items():
            its.draw_vert(renderer)

    def clear_verts(self, renderer):
        """
        Clears all vertices of the path
        :param renderer: vtkRenderer
        :return:
        """
        for key, its in self._its_dict.items():
            its.clear_vert(renderer)

    def draw_all(self, renderer):
        """
        Draws everything of the path
        :param renderer: vtkRenderer
        :return:
        """
        for key, its in self._its_dict.items():
            its.draw_all(renderer)

    def draw_path(self, renderer):
        """
        Draws only the path (incoming rays, rays that end in an environment map)
        :param renderer: vtkRenderer
        :return:
        """
        for key, its in self._its_dict.items():
            its.draw_wi(renderer)
            if its.is_wo_set:
                if its.wo.is_envmap:
                    its.draw_wo(renderer)

    def draw_ne(self, renderer):
        """
        Draws all next event estimations of the path
        :param renderer: vtkRenderer
        :return:
        """
        for key, its in self._its_dict.items():
            its.draw_ne(renderer)

    def clear_path(self, renderer):
        """
        Clears the path
        :param renderer: vtkRenderer
        :return:
        """
        for key, its in self._its_dict.items():
            its.clear_path(renderer)

    def clear_ne(self, renderer):
        """
        Clears all next event estimations of the path
        :param renderer: vtkRenderer
        :return:
        """
        for key, its in self._its_dict.items():
            its.clear_ne(renderer)

    def clear_envmap(self, renderer):
        """
        Clears all paths ending in an environment map
        :param renderer: vtkRenderer
        :return:
        """
        for key, its in self._its_dict.items():
            its.clear_envmap(renderer)

    def clear_all(self, renderer):
        """
        Clears the whole path with all objects
        :param renderer:
        :return:
        """
        for key, its in self._its_dict.items():
            its.clear_all(renderer)

    def draw_envmap(self, renderer):
        """
        Draws paths which ends in an environment map
        :param renderer:
        :return:
        """
        for key, its in self._its_dict.items():
            its.draw_envmap(renderer)

    def set_selected(self, selected):
        """
        Set the path selected
        :param selected: boolean
        :return:
        """
        for key, its in self._its_dict.items():
            its.set_selected(selected)

    def set_opacity(self, value):
        """
        Sets the opacity of the path and its vertices
        :param value: float[0,1]
        :return:
        """
        self._opacity = value
        for key, its in self._its_dict.items():
            its.set_opacity(value)

    def set_path_opacity(self, value):
        """
        Sets only the path opacity (no vertices)
        :param value: float[0,1]
        :return:
        """
        self._opacity = value
        for key, its in self._its_dict.items():
            its.set_path_opacity(value)

    def reset_path_opacity(self):
        """
        Resets the path opacity (no vertices reset)
        :return:
        """
        self._opacity = self.default_opacity
        for key, its in self._its_dict.items():
            its.reset_path_opacity()

    def reset_vertex_opacity(self):
        """
        Resets the opacity of all path vertices
        :return:
        """
        self._opacity = self.default_opacity
        for key, its in self._its_dict.items():
            its.reset_vertex_opacity()

    def set_path_size(self, value):
        """
        Sets only the path size (no vertices)
        :param value: float[0,1]
        :return:
        """
        self._size = value
        for key, its in self._its_dict.items():
            its.set_path_size(value)

    def reset_path(self):
        """
        Resets the path opacity and size (no vertices)
        :return:
        """
        self._opacity = self.default_opacity
        self._size = self.default_size
        for key, its in self._its_dict.items():
            its.reset_rays()

    def reset(self):
        """
        Resets the whole path and its vertices
        :return:
        """
        self._opacity = self.default_opacity
        self._size = self.default_size
        for key, its in self._its_dict.items():
            its.reset()

