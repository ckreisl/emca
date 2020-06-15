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

import logging


class Intersection(object):

    """
        Intersection
        Represents an intersection.
        Holding render information for the 3D view for every intersection,
        such as incoming, outgoing, next event estimation vector, opacity and size
    """

    def __init__(self, idx, wi, its, wo, ne):
        self._idx = idx     # intersection index
        self._wi = wi       # incoming ray
        self._wo = wo       # outgoing ray
        self._ne = ne       # next event estimation
        self._its = its     # intersection (shading point)

        self._opacity = 1.0
        self._size = 1.0

        self._is_wi_visible = True
        self._is_wo_visible = False
        if self._wo:
            if self._wo.is_envmap:
                self._is_wo_visible = True
        self._is_ne_visible = False

    def set_visibility(self, wi, wo, ne):
        """
        Sets the visibility of incoming, outgoing and next event estimation visualization
        :param wi: incoming ray
        :param wo: outgoing ray
        :param ne: next event estimation ray
        :return:
        """
        self._is_wi_visible = wi
        self._is_wo_visible = wo
        self._is_ne_visible = ne

    @property
    def is_wi_visible(self):
        """
        Returns if the incoming ray is visible
        :return: boolean
        """
        return self._is_wi_visible

    @is_wi_visible.setter
    def is_wi_visible(self, visible):
        """
        Sets the visibility of the incoming ray
        :param visible:
        :return:
        """
        self._is_wi_visible = visible

    @property
    def is_wo_visible(self):
        """
        Returns if the outgoing ray is visible
        :return: boolean
        """
        return self._is_wo_visible

    @is_wo_visible.setter
    def is_wo_visible(self, visible):
        """
        Sets the visibility of the outgoing ray
        :param visible:
        :return:
        """
        self._is_wo_visible = visible

    @property
    def is_ne_visible(self):
        """
        Returns if the next event estimation ray is visible
        :return: boolean
        """
        return self._is_ne_visible

    @is_ne_visible.setter
    def is_ne_visible(self, visible):
        """
        Sets the visibility of the next event estimation
        :param visible:
        :return:
        """
        self._is_ne_visible = visible

    @property
    def pos(self):
        """
        Returns the 3D position of the intersection
        :return: point3f
        """
        return self._its.pos

    @property
    def wi(self):
        """
        Returns the incoming ray
        :return: ray
        """
        return self._wi

    @property
    def wo(self):
        """
        Returns the outgoing ray
        :return: ray
        """
        return self._wo

    @property
    def ne(self):
        """
        Returns the next event estimation ray
        :return: ray
        """
        return self._ne

    @property
    def its(self):
        """
        Returns the current intersection (vtkVertex)
        :return:
        """
        return self._its

    @property
    def idx(self):
        """
        Returns the intersection index
        :return:
        """
        return self._idx

    @property
    def is_wi_set(self):
        """
        Returns the incoming ray or None
        :return: ray or None
        """
        return self._wi is not None

    @property
    def is_wo_set(self):
        """
        Returns the outgoing ray or None
        :return: ray or None
        """
        return self._wo is not None

    @property
    def is_ne_set(self):
        """
        Returns the next event estimation ray or None
        :return: ray or None
        """
        return self._ne is not None

    @property
    def opacity(self):
        """
        Returns the opacity
        :return:
        """
        return self._opacity

    @property
    def size(self):
        """
        Returns the size
        :return:
        """
        return self._size

    @property
    def default_opacity(self):
        """
        Returns the default opacity 1.0
        :return:
        """
        return 1.0

    @property
    def default_size(self):
        """
        Returns the default size 1.0
        :return:
        """
        return 1.0

    def set_wo(self, ray_wo):
        """
        Sets the outgoing ray
        :param ray_wo:
        :return:
        """
        self._wo = ray_wo

    def draw_all(self, renderer):
        """
        Draws all, including incoming, outgoing, nee and the intersection vertex
        :param renderer:
        :return:
        """
        self.draw_wi(renderer)
        self.draw_its(renderer)
        self.draw_ne(renderer)
        if self._wo:
            if self._wo.is_envmap:
                self.draw_wo(renderer)

    def draw_wi(self, renderer):
        """
        Draws the incoming ray
        :param renderer:
        :return:
        """
        renderer.AddActor(self._wi)
        self._is_wi_visible = True

    def draw_wo(self, renderer):
        """
        Draws the outgoing ray
        :param renderer:
        :return:
        """
        renderer.AddActor(self._wo)
        self._is_wo_visible = True

    def draw_ne(self, renderer):
        """
        Draws the next event estimation
        :param renderer:
        :return:
        """
        renderer.AddActor(self._ne)
        self._is_ne_visible = True

    def draw_its(self, renderer):
        """
        Draws the intersection / vertex (vtkVertex)
        :param renderer:
        :return:
        """
        renderer.AddActor(self._its)

    def draw_envmap(self, renderer):
        """
        Draws a outgoing ray that end in the environment map
        :param renderer:
        :return:
        """
        if self._wo:
            if self._wo.is_envmap:
                renderer.AddActor(self._wo)

    def set_selected(self, selected):
        """
        Highlight incoming ray and intersection vertex
        :param selected: boolean
        :return:
        """
        if self._wi:
            self._wi.selected = selected
        if self._its:
            self._its.selected = selected

    def set_color_wi(self, color):
        """
        Sets the color of the incoming ray to color
        :param color:
        :return:
        """
        if self._wi:
            self._wi.set_color_list(color)

    def set_color_wo(self, color):
        """
        Sets the color of the outgoing ray to color
        :param color:
        :return:
        """
        if self._wo:
            self._wo.set_color_list(color)

    def set_color_its(self, color):
        """
        Sets the intersection color
        :param color:
        :return:
        """
        if self._its:
            self._its.set_color_list(color)

    def set_intersection_opacity(self, value):
        """
        Set the intersection opacity
        :param value:
        :return:
        """
        self._opacity = value
        self._its.opacity = value

    def set_intersection_size(self, value):
        """
        Set the intersection size
        :param value:
        :return:
        """
        self._size = value
        self._its.size = value

    def reset_intersection(self):
        """
        Resets the intersection to its default values (opacity and size)
        :return:
        """
        self._opacity = self.default_opacity
        self._size = self.default_size
        self._its.opacity = self.default_opacity
        self._its.size = self.default_size

    def set_path_size(self, value):
        """
        Sets size of whole path
        :param value:
        :return:
        """
        if self._wi:
            self._wi.size = value
        if self._wo:
            if self._wo.is_envmap:
                self._wo.size = value

    def set_path_opacity(self, value):
        """
        Sets the path opacity to a value
        :param value:
        :return:
        """
        if self._wi:
            self._wi.opacity = value
        if self._wo:
            self._wo.opacity = value
        if self._ne:
            self._ne.opacity = value

    def reset_path_opacity(self):
        """
        Resets the path opacity
        :return:
        """
        self._opacity = self.default_opacity
        self.set_path_opacity(self.default_opacity)
        
    def reset_path_size(self):
        """
        Resets the path size
        """
        self._size = self.default_size
        self.set_path_size(self.default_size)

    def reset_intersection_opacity(self):
        """
        Resets the intersection vertex opacity
        :return:
        """
        self._opacity = self.default_opacity
        self.set_intersection_opacity(self.default_opacity)
        
    def reset_intersection_size(self):
        """
        Resets the intersection vertex size
        """
        self._size = self.default_size
        self.set_intersection_size(self.default_size)

    def clear_ne(self, renderer):
        """
        Clear next event estimation ray
        :param renderer:
        :return:
        """
        renderer.RemoveActor(self._ne)
        self._is_ne_visible = False

    def clear_wi(self, renderer):
        """
        Clear incoming ray
        :param renderer:
        :return:
        """
        renderer.RemoveActor(self._wi)
        self._is_wi_visible = False

    def clear_wo(self, renderer):
        """
        Clear outgoing ray
        :param renderer:
        :return:
        """
        renderer.RemoveActor(self._wo)
        self._is_wo_visible = False

    def clear_its(self, renderer):
        """
        Clear intersection
        :param renderer:
        :return:
        """
        renderer.RemoveActor(self._its)

    def clear_envmap(self, renderer):
        """
        Clear outgoing ray if its a ray ending in the environment map
        :param renderer:
        :return:
        """
        if self._wo:
            if self._wo.is_envmap:
                renderer.RemoveActor(self._wo)

    def clear_path(self, renderer):
        """
        Clears incoming, outgoing and next event estimation ray
        :param renderer:
        :return:
        """
        renderer.RemoveActor(self._wi)
        renderer.RemoveActor(self._wo)
        renderer.RemoveActor(self._ne)

    def clear_all(self, renderer):
        """
        Clears all including, incoming, outgoing, next event estimation and the intersection vertex
        :param renderer:
        :return:
        """
        renderer.RemoveActor(self._wi)
        renderer.RemoveActor(self._wo)
        renderer.RemoveActor(self._ne)
        renderer.RemoveActor(self._its)
