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

from Types.factory import TypeFactory
from xml.etree import ElementTree
from xml.dom import minidom
import xml.etree.cElementTree as ET
import logging
import time


class XMLParser(object):

    """
        XMLParser
        Parses the current state of a selected pixel with its Render Data within a xml file,
        or can load the current state from a xml file.
    """

    def __init__(self):
        pass

    def add_pixel_info_to_xml_data(self, root, pixel_info):
        """
        Adds the pixel information to the xml file
        :param root:
        :param pixel_info:
        :return:
        """
        pixel = ET.SubElement(root, "pixel")
        ET.SubElement(pixel, "point2i", name="pixelPos").text = TypeFactory.to_string(pixel_info.pixel_pos_point2i)
        ET.SubElement(pixel, "color3f", name="pixelColor").text = TypeFactory.to_string(pixel_info.pixel_color_color3f)

    def add_render_info_to_xml_data(self, root, render_info):
        """
        Adss the render info to the xml file
        :param root:
        :param render_info:
        :return:
        """
        scene = ET.SubElement(root, "scene")
        ET.SubElement(scene, "string", name="name").text = str(render_info.scene_name)
        ET.SubElement(scene, "string", name="filepath").text = str(render_info.output_filepath)
        ET.SubElement(scene, "string", name="extension").text = str(render_info.file_extension)
        ET.SubElement(scene, "integer", name="sampleCount").text = str(render_info.sample_count)

    def add_camera_info_to_xml_data(self, root, camera_data):
        """
        Adds the camera information to the xml file
        :param root:
        :param camera_data:
        :return:
        """
        camera = ET.SubElement(root, "camera")
        ET.SubElement(camera, "float", name="nearClip").text = str(camera_data.near_clip)
        ET.SubElement(camera, "float", name="farClip").text = str(camera_data.far_clip)
        ET.SubElement(camera, "float", name="focusDist").text = str(camera_data.focus_dist)
        ET.SubElement(camera, "float", name="fov").text = str(camera_data.fov)
        ET.SubElement(camera, "vec3f", name="viewUp").text = TypeFactory.to_string(camera_data.up)
        ET.SubElement(camera, "vec3f", name="viewDirection").text = TypeFactory.to_string(camera_data.direction)
        ET.SubElement(camera, "point3f", name="origin").text = TypeFactory.to_string(camera_data.origin)

    def add_mesh_data_to_xml_data(self, root, mesh_data):
        """
        Adds all mesh scene information to the xml file
        :param root:
        :param mesh_data:
        :return:
        """
        meshes = ET.SubElement(root, "meshes")
        ET.SubElement(meshes, "integer", name="meshCount").text = str(mesh_data.mesh_count)

        for mesh_obj in mesh_data.meshes:
            mesh = ET.SubElement(meshes, "mesh")
            ET.SubElement(mesh, "integer", name='vertexCount').text = str(mesh_obj.vertex_count)
            for vert in mesh_obj.vertices:
                ET.SubElement(mesh, "point3f", name="vertex").text = TypeFactory.to_string(vert)
            ET.SubElement(mesh, "integer", name="triangleCount").text = str(mesh_obj.triangle_count)
            for tri in mesh_obj.triangles:
                ET.SubElement(mesh, "point3i", name="triangleIndices").text = TypeFactory.to_string(tri)
            ET.SubElement(mesh, "color3f", name="specular").text = TypeFactory.to_string(mesh_obj.specular_color)
            ET.SubElement(mesh, "color3f", name="diffuse").text = TypeFactory.to_string(mesh_obj.diffuse_color)

    def add_render_data_to_xml_data(self, root, render_data):
        """
        Adds the render data to the xml file
        :param root:
        :param render_data:
        :return:
        """
        data = ET.SubElement(root, "data")
        ET.SubElement(data, "integer", name="pathCount").text = str(render_data.sample_count)

        for path_key, path_data in render_data.dict_paths.items():
            path = ET.SubElement(data, "path")
            self.add_path_data_to_xml_data(path, path_data)
            self.add_user_data_to_xml_data(path, path_data)
            for vert_key, vert_data in path_data.dict_vertices.items():
                vertex = ET.SubElement(path, "vertex")
                self.add_vertex_data_to_xml_data(vertex, vert_data)
                self.add_user_data_to_xml_data(vertex, vert_data)

    def add_path_data_to_xml_data(self, parent, path_data):
        """
        Adds the path data to the xml file
        :param parent:
        :param path_data:
        :return:
        """
        ET.SubElement(parent, "integer", name="pathIndex").text = str(path_data.sample_idx)
        ET.SubElement(parent, "integer", name="pathDepth").text = str(path_data.path_depth)
        ET.SubElement(parent, "point3f", name="origin").text = TypeFactory.to_string(path_data.path_origin)
        ET.SubElement(parent, "color3f", name="finalEstimate").text = TypeFactory.to_string(path_data.final_estimate)
        ET.SubElement(parent, "boolean", name="showPath").text = str(path_data.is_show_path)
        ET.SubElement(parent, "boolean", name="showNE").text = str(path_data.is_show_ne)
        ET.SubElement(parent, "integer", name="vertexCount").text = str(path_data.vertex_count)

    def add_vertex_data_to_xml_data(self, parent, vert_data):
        """
        Adds the vertex data to the xml file
        :param parent:
        :param vert_data:
        :return:
        """
        ET.SubElement(parent, "integer", name="vertexIndex").text = str(vert_data.depth_idx)
        ET.SubElement(parent, "point3f", name="pos").text = TypeFactory.to_string(vert_data.pos)
        ET.SubElement(parent, "boolean", name="setPos").text = str(vert_data.is_pos_set)
        ET.SubElement(parent, "point3f", name="posNE").text = TypeFactory.to_string(vert_data.pos_ne)
        ET.SubElement(parent, "boolean", name="setNE").text = str(vert_data.is_ne_set)
        ET.SubElement(parent, "boolean", name="occludedNE").text = str(vert_data.is_ne_occluded)
        ET.SubElement(parent, "point3f", name="posEnvmap").text = TypeFactory.to_string(vert_data.pos_envmap)
        ET.SubElement(parent, "boolean", name="setEnvmap").text = str(vert_data.is_envmap_set)
        ET.SubElement(parent, "color3f", name="estimate").text = TypeFactory.to_string(vert_data.li)
        ET.SubElement(parent, "boolean", name="setEstimate").text = str(vert_data.is_li_set)

    def add_user_data_to_xml_data(self, parent, user_data):
        """
        Adds user data to the xml file
        :param parent:
        :param user_data:
        :return:
        """
        user_data_tag = ET.SubElement(parent, "userdata")
        self._add_user_data_helper(user_data_tag, user_data.dict_bool, "boolean")
        self._add_user_data_helper(user_data_tag, user_data.dict_float, "float")
        self._add_user_data_helper(user_data_tag, user_data.dict_double, "double")
        self._add_user_data_helper(user_data_tag, user_data.dict_int, "integer")
        self._add_user_data_helper(user_data_tag, user_data.dict_point2i, "point2i")
        self._add_user_data_helper(user_data_tag, user_data.dict_point2f, "point2f")
        self._add_user_data_helper(user_data_tag, user_data.dict_point3i, "point3i")
        self._add_user_data_helper(user_data_tag, user_data.dict_point3f, "point3f")
        self._add_user_data_helper(user_data_tag, user_data.dict_color3f, "color3f")

    def _add_user_data_helper(self, parent, data_dict, type_str):
        """
        Helper function to add the user data to the xml file
        :param parent:
        :param data_dict:
        :param type_str:
        :return:
        """
        if type_str in ["point2i", "point2f", "point3f", "point3i", "color3f"]:
            for key, value in data_dict.items():
                size = len(value)
                ET.SubElement(parent, type_str, name=key, size=str(size)).text = TypeFactory.to_string(value[0])
        else:
            for key, value in data_dict.items():
                size = len(value)
                ET.SubElement(parent, type_str, name=key, size=str(size)).text = str(value[0])

    @staticmethod
    def prettify(elem):
        """
        Pretty output for xml tree
        :param elem:
        :return:
        """
        rough_string = ElementTree.tostring(elem, 'utf-8')
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="    ")

    def read_xml(self, filepath, dataset):
        """
        Reads a xml file from a filepath and deserialize all data within the dataset
        :param filepath:
        :param dataset:
        :return:
        """
        start = time.time()

        tree = ET.parse(filepath)
        root = tree.getroot()

        # deserialize all data within the model (dataset)
        dataset.pixel_info.deserialize_xml(root.find("pixel"))
        dataset.render_info.deserialize_xml(root.find("scene"))
        dataset.camera_data.deserialize_xml(root.find("camera"))
        dataset.mesh_data.deserialize_xml(root.find("meshes"))
        dataset.render_data.deserialize_xml(root.find("data"))

        logging.info('time to read data from xml file runtime: {}ms'.format(time.time() - start))

    def write_xml(self, output_name, dataset):
        """
        Creates a xml file and saves all information from the dataset within it
        :param output_name:
        :param dataset:
        :return:
        """
        start = time.time()

        if output_name == "":
            return

        root = ET.Element("root")
        self.add_pixel_info_to_xml_data(root, dataset.pixel_info)
        self.add_render_info_to_xml_data(root, dataset.render_info)
        self.add_camera_info_to_xml_data(root, dataset.camera_data)
        self.add_mesh_data_to_xml_data(root, dataset.mesh_data)
        self.add_render_data_to_xml_data(root, dataset.render_data)

        # add filetype to file
        if not output_name.endswith(".xml"):
            output_name += ".xml"

        # write created xml node into file
        with open(output_name, "w") as xml_file:
            xml_file.write(self.prettify(root))

        logging.info('time to create xml save file runtime: {}ms'.format(time.time() - start))

