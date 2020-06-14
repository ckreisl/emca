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

from renderer.ray import Ray
from renderer.intersection_vertex import IntersectionVertex
from renderer.intersection import Intersection
import logging


class Path(object):

    """
        Path
        Visualizes one path in the vtkRenderer (3D viewer)
    """

    def __init__(self, idx, origin, path_data, default_opacity=1.0, default_size=1.0):
        self._path_idx = idx
        self._origin = origin
        self._its_dict = {}

        self._default_opacity = default_opacity
        self._opacity = default_opacity
        self._default_size = default_size
        self._size = default_size

        self._visible = True
        self._visible_ne = False

        self.create_path(idx, origin, path_data)

    def init_default_opacity_and_size(self, objects):
        """
        Initialises the vtk 3d actor with its default size and opacity
        :param objects: list
        :return:
        """
        for obj in objects:
            obj.default_opacity = self._default_opacity
            obj.opacity = self._opacity
            obj.default_size = self._default_size
            obj.size = self._size

    def create_path(self, idx, origin, path_data):
        """
        Initializes the path and sets each corresponding intersection point with its rays
        :param idx: sample_index/path_index integer
        :param origin: Point3f
        :param path_data: PathData
        :return:
        """

        intersections = path_data.intersections

        # start index mitsuba 1 (0 in nori2 framework)
        start_key = next(iter(intersections))
        # algorithm which creates the path from the model vertices data
        for its_key, its in intersections.items():

            if not its.is_pos_set:
                if its_key == start_key and its.is_envmap_set:
                    wi = Ray(origin, its.pos_envmap, is_envmap=True)
                    self._its_dict[its_key] = Intersection(its_key, wi, None, None, None)
                continue

            wi = None
            if its_key == start_key:
                wi = Ray(origin, its.pos)
            else:
                last_vertex = intersections.get(its_key-1, None)
                if last_vertex:
                    wi = Ray(last_vertex.pos, its.pos)

            vertex = IntersectionVertex(idx, its_key, its.pos)

            wo = None
            next_vertex = intersections.get(its_key+1, None)
            if next_vertex:
                if next_vertex.is_pos_set:
                    wo = Ray(its.pos, next_vertex.pos)
                elif next_vertex.is_envmap_set:
                    wo = Ray(its.pos, next_vertex.pos_envmap, is_envmap=True)

            if its.is_envmap_set:
                wo = Ray(its.pos, its.pos_envmap, is_envmap=True)

            ne = None
            if its.is_ne_set:
                ne = Ray(its.pos, its.pos_ne, is_ne=True, is_ne_occluded=its.is_ne_occluded)

            self.init_default_opacity_and_size([i for i in [vertex, wi, wo, ne] if i])
            self._its_dict[its_key] = Intersection(its_key, wi, vertex, wo, ne)

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
        Returns the current path opacity
        :return: float[0,1]
        """
        return self._opacity

    @property
    def default_opacity(self):
        """
        Returns the default opacity of the path
        """
        return self._default_opacity

    @property
    def default_size(self):
        """
        Returns the default size of the path
        """
        return self._default_size

    @property
    def size(self):
        """
        Returns the current path size
        :return: float[0,1]
        """
        return self._size

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
        for _, its in self._its_dict.items():
            its.draw_vert(renderer)

    def clear_verts(self, renderer):
        """
        Clears all vertices of the path
        :param renderer: vtkRenderer
        :return:
        """
        for _, its in self._its_dict.items():
            its.clear_vert(renderer)

    def draw_all(self, renderer):
        """
        Draws everything of the path
        :param renderer: vtkRenderer
        :return:
        """
        for _, its in self._its_dict.items():
            its.draw_all(renderer)

    def draw_path(self, renderer):
        """
        Draws only the path (incoming rays, rays that end in an environment map)
        :param renderer: vtkRenderer
        :return:
        """
        for _, its in self._its_dict.items():
            its.draw_wi(renderer)
            if its.is_wo_set:
                if its.wo.is_envmap:
                    its.draw_wo(renderer)
        self._visible = True

    def draw_ne(self, renderer):
        """
        Draws all next event estimations of the path
        :param renderer: vtkRenderer
        :return:
        """
        for _, its in self._its_dict.items():
            its.draw_ne(renderer)
        self._visible_ne = True

    def clear_path(self, renderer):
        """
        Clears the path
        :param renderer: vtkRenderer
        :return:
        """
        for _, its in self._its_dict.items():
            its.clear_path(renderer)
        self._visible = False

    def clear_ne(self, renderer):
        """
        Clears all next event estimations of the path
        :param renderer: vtkRenderer
        :return:
        """
        for _, its in self._its_dict.items():
            its.clear_ne(renderer)
        self._visible_ne = False

    def clear_envmap(self, renderer):
        """
        Clears all paths ending in an environment map
        :param renderer: vtkRenderer
        :return:
        """
        for _, its in self._its_dict.items():
            its.clear_envmap(renderer)

    def clear_all(self, renderer):
        """
        Clears the whole path with all objects
        :param renderer:
        :return:
        """
        for _, its in self._its_dict.items():
            its.clear_all(renderer)
        self._visible = False
        self._visible_ne = False

    def draw_envmap(self, renderer):
        """
        Draws paths which ends in an environment map
        :param renderer:
        :return:
        """
        for _, its in self._its_dict.items():
            its.draw_envmap(renderer)

    def set_selected(self, selected):
        """
        Set the path selected
        :param selected: boolean
        :return:
        """
        for _, its in self._its_dict.items():
            its.set_selected(selected)

    def set_path_opacity(self, value):
        """
        Sets only the path opacity (no vertices)
        :param value: float[0,1]
        :return:
        """
        self._opacity = value
        for _, its in self._its_dict.items():
            its.set_path_opacity(value)

    def reset_path_opacity(self):
        """
        Resets the path opacity (no vertices reset)
        :return:
        """
        self._opacity = self.default_opacity
        for _, its in self._its_dict.items():
            its.reset_path_opacity()

    def reset_path_size(self):
        """
        Resets the path size (no vertices reset)
        """
        self._size = self.default_size
        for _, its in self._its_dict.items():
            its.reset_path_size()

    def reset_vertex_opacity(self):
        """
        Resets the opacity of all path vertices / intersections
        :return:
        """
        self._opacity = self.default_opacity
        for _, its in self._its_dict.items():
            its.reset_vertex_opacity()

    def reset_vertex_size(self):
        """
        Resets the size of all path vertices / intersections
        """
        self._size = self.default_size
        for _, its in self._its_dict.items():
            its.reset_vertex_size()

    def set_path_size(self, value):
        """
        Sets only the path size (no vertices)
        :param value: float[0,1]
        :return:
        """
        self._size = value
        for key, its in self._its_dict.items():
            its.set_path_size(value)
