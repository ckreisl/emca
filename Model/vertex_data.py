from Model.user_data import UserData
from Types.factory import TypeFactory
import logging


class VertexData(UserData):

    """
        VertexData
        Represents one intersection point of a traced path through the scene.
        Holds information about the intersection, more precisely the vertex position, the vertex index,
        if a next event estimation was set, if a vertex position was set and current estimate information at this point.
    """

    def __init__(self):
        UserData.__init__(self)
        self._depth_idx = None
        self._pos = None
        self._set_pos = None
        self._occluded_ne = None
        self._set_ne = None
        self._pos_ne = None
        self._occluded_ne = None
        self._pos_envmap = None
        self._set_envmap = None
        self._li = None
        self._set_li = None

    def deserialize(self, stream):
        """
        Deserialize a VertexData object from the socket stream
        :param stream:
        :return:
        """
        super().deserialize(stream)
        self._depth_idx = stream.read_int()

        self._pos = None
        self._set_pos = stream.read_bool()
        if self._set_pos:
            self._pos = stream.read_point3f()

        self._pos_ne = None
        self._occluded_ne = None
        self._set_ne = stream.read_bool()
        if self._set_ne:
            self._pos_ne = stream.read_point3f()
            self._occluded_ne = stream.read_bool()

        self._pos_envmap = None
        self._set_envmap = stream.read_bool()
        if self._set_envmap:
            self._pos_envmap = stream.read_point3f()

        self._li = None
        self._set_li = stream.read_bool()
        if self._set_li:
            self._li = stream.read_color3f()

    def deserialize_xml(self, node):
        """
        Deserialize a VertexData object from a xml file
        :param node:
        :return:
        """
        for item in list(node):
            if item.tag == "integer" and item.attrib["name"] == "vertexIndex":
                self._depth_idx = int(item.text)
            elif item.tag == "point3f" and item.attrib["name"] == "pos":
                self._pos = TypeFactory.create_point3f_from_str(item.text)
            elif item.tag == "boolean" and item.attrib["name"] == "setPos":
                self._set_pos = TypeFactory.create_boolean_from_str(item.text)
            elif item.tag == "point3f" and item.attrib["name"] == "posNE":
                self._pos_ne = TypeFactory.create_point3f_from_str(item.text)
            elif item.tag == "boolean" and item.attrib["name"] == "setNE":
                self._set_ne = TypeFactory.create_boolean_from_str(item.text)
            elif item.tag == "boolean" and item.attrib["name"] == "occludedNE":
                self._occluded_ne = TypeFactory.create_boolean_from_str(item.text)
            elif item.tag == "point3f" and item.attrib["name"] == "posEnvmap":
                self._pos_envmap = TypeFactory.create_point3f_from_str(item.text)
            elif item.tag == "boolean" and item.attrib["name"] == "setEnvmap":
                self._set_envmap = TypeFactory.create_boolean_from_str(item.text)
            elif item.tag == "color3f" and item.attrib["name"] == "estimate":
                self._li = TypeFactory.create_color3f_from_str(item.text)
            elif item.tag == "boolean" and item.attrib["name"] == "setEstimate":
                self._set_li = TypeFactory.create_boolean_from_str(item.text)
            elif item.tag == "userdata":
                super().deserialize_xml(item)

    @property
    def depth_idx(self):
        """
        Returns the current depth index (vertex index)
        :return: integer
        """
        return self._depth_idx

    @property
    def is_pos_set(self):
        """
        Returns if a intersection position was set on the server side
        :return: boolean
        """
        return self._set_pos

    @property
    def is_ne_set(self):
        """
        Returns if a next event estimation was set on the server side
        :return: boolean
        """
        return self._set_ne

    @property
    def is_ne_occluded(self):
        """
        Returns if the next estimation is occluded
        :return: boolean
        """
        return self._occluded_ne

    @property
    def is_envmap_set(self):
        """
        Returns of a environment map position was set on the server
        :return: boolean
        """
        return self._set_envmap

    @property
    def is_li_set(self):
        """
        Returns if a current estimate at this position was set on the server
        :return: color3f
        """
        return self._set_li

    @property
    def pos(self):
        """
        Returns the vertex / intersection position
        :return: point3f
        """
        return self._pos

    @property
    def pos_ne(self):
        """
        Returns the position of the next event estimation
        :return: point3f
        """
        return self._pos_ne

    @property
    def pos_envmap(self):
        """
        Returns the position on the environment map
        :return:
        """
        return self._pos_envmap

    @property
    def li(self):
        """
        Returns the current estimate at this intersection / path position
        :return:
        """
        return self._li

