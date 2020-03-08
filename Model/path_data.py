from Model.vertex_data import VertexData
from Model.user_data import UserData
from Types.factory import TypeFactory
import logging


class PathData(UserData):

    """
        PathData
        Represents one traced path with added user data
    """

    def __init__(self):
        UserData.__init__(self)

        self._sample_idx = None
        self._path_depth = None
        self._path_origin = None
        self._final_estimate = None
        self._show_path = None
        self._show_ne = None
        self._dict_vertices = {}
        self._vertex_count = None

    def deserialize(self, stream):
        """
        Deserializes one path object from the socket stream
        :param stream:
        :return:
        """
        super().deserialize(stream)
        self._sample_idx = stream.read_int()
        self._path_depth = stream.read_int()
        self._path_origin = stream.read_point3f()

        self._final_estimate = None
        if stream.read_bool():
            self._final_estimate = stream.read_color3f()

        self._show_path = stream.read_bool()
        self._show_ne = stream.read_bool()

        self._dict_vertices.clear()
        self._vertex_count = stream.read_uint()
        for i in range(0, self._vertex_count):
            vertex_idx = stream.read_int()
            vertex = VertexData()
            vertex.deserialize(stream)
            self._dict_vertices[vertex_idx] = vertex

    def deserialize_xml(self, node):
        """
        Deserializes one path object from a xml file
        :param node:
        :return:
        """
        self._dict_vertices.clear()
        for item in list(node):
            if item.tag == "integer" and item.attrib["name"] == "pathIndex":
                self._sample_idx = int(item.text)
            elif item.tag == "integer" and item.attrib["name"] == "pathDepth":
                self._path_depth = int(item.text)
            elif item.tag == "point3f" and item.attrib["name"] == "origin":
                self._path_origin = TypeFactory.create_point3f_from_str(item.text)
            elif item.tag == "color3f" and item.attrib["name"] == "finalEstimate":
                self._final_estimate = TypeFactory.create_color3f_from_str(item.text)
            elif item.tag == "boolean" and item.attrib["name"] == "showPath":
                self._show_path = TypeFactory.create_boolean_from_str(item.text)
            elif item.tag == "boolean" and item.attrib["name"] == "showNE":
                self._show_ne = TypeFactory.create_boolean_from_str(item.text)
            elif item.tag == "integer" and item.attrib["name"] == "vertexCount":
                self._vertex_count = int(item.text)
            elif item.tag == "vertex":
                vertex = VertexData()
                vertex.deserialize_xml(item)
                self._dict_vertices[vertex.depth_idx] = vertex
            elif item.tag == "userdata":
                super().deserialize_xml(item)

    @property
    def final_estimate(self):
        """
        Returns the Final Estimate value of this path
        :return: color3f
        """
        return self._final_estimate

    @property
    def sample_idx(self):
        """
        Returns the samples index which indicates the path index
        :return: integer
        """
        return self._sample_idx

    @property
    def path_origin(self):
        """
        Returns the path origin
        :return: point3f
        """
        return self._path_origin

    @property
    def path_depth(self):
        """
        Returns the path depth (amount of bounces and containing vertices)
        :return: integer
        """
        return self._path_depth

    @property
    def dict_vertices(self):
        """
        Returns the a dict containing all path vertices
        :return: dict{vertex_idx, vertex object}
        """
        return self._dict_vertices

    @property
    def is_show_path(self):
        """
        Returns if intersection points were added
        :return: boolean
        """
        return self._show_path

    @property
    def is_show_ne(self):
        """
        Returns if next event estimation was added
        :return: boolean
        """
        return self._show_ne

    @property
    def vertex_count(self):
        """
        Returns the amount of vertices (intersections)
        :return: integer
        """
        return self._vertex_count

    def valid_depth(self):
        """
        Checks if the path depth is valid (path_depth != -1)
        :return: bool
        """
        return self._path_depth != -1
