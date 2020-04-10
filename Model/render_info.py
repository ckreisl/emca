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

from Core.messages import ServerMsg
import logging


class RenderInfo(object):

    """
        RenderInfo
        Holds general information about the rendered scene,
        such as scene name, sample count and the path where the final rendered result is saved
    """

    def __init__(self):
        self._scene_name = None
        self._output_filepath = None
        self._extension = None
        self._sample_count = None

    def deserialize(self, stream):
        """
        Deserialize a Render Info object from the socket stream
        :param stream:
        :return:
        """
        self._scene_name = self.is_valid_str(stream.read_string())
        self._output_filepath = self.is_valid_str(stream.read_string())
        self._extension = self.is_valid_str(stream.read_string())
        self._sample_count = stream.read_int()

    def serialize(self, stream):
        """
        Only send new sample count to server,
        since we can currently only change this value in our view
        :param stream:
        :return:
        """
        stream.write_short(ServerMsg.EMCA_SEND_RENDER_INFO.value)
        stream.write_int(self._sample_count)

    def deserialize_xml(self, node):
        """
        Deserialize a Render Info object from a xml file
        :param node:
        :return:
        """
        for item in list(node):
            if item.tag == "string" and item.attrib["name"] == "name":
                self._scene_name = item.text
            elif item.tag == "string" and item.attrib["name"] == "filepath":
                self._output_filepath = item.text
            elif item.tag == "string" and item.attrib["name"] == "extension":
                self._extension = item.text
            elif item.tag == "integer" and item.attrib["name"] == "sampleCount":
                self._sample_count = int(item.text)
            else:
                logging.info("Could not parse item (tag, attrib, text): {}".format(item.tag,
                                                                                   item.attrib,
                                                                                   item.text))

    @staticmethod
    def is_valid_str(s):
        """
        Checks if the string is valid != "not set'
        :param s: string
        :return: boolean
        """
        if s == "":
            return "not set"
        else:
            return s

    @property
    def scene_name(self):
        """
        Returns the scene name
        :return:
        """
        return self._scene_name

    @property
    def output_filepath(self):
        """
        Returns the filepath to the rendered output file
        :return:
        """
        return self._output_filepath

    @property
    def file_extension(self):
        """
        Returns the information about the file extension (.exr, ...)
        :return:
        """
        return self._extension

    @property
    def sample_count(self):
        """
        Returns the amount of used samples to render the scene
        :return:
        """
        if self._sample_count:
            return self._sample_count
        else:
            return 0

    def filepath(self):
        """
        Returns the filepath to the output rendered image,
        adds .exr at the ending if extension is missing
        :return:
        """
        if self._output_filepath.endswith(".exr"):
            return self._output_filepath
        else:
            return self._output_filepath + ".exr"

    def set_scene_name(self, name):
        """
        Setter function, sets the scene name
        :param name: string
        :return:
        """
        self._scene_name = name

    def set_output_filepath(self, path):
        """
        Setter function, sets the rendered output filepath
        :param path: string
        :return:
        """
        self._output_filepath = path

    def set_sample_count(self, count):
        """
        Setter function, sets the sample count
        :param count: integer
        :return:
        """
        self._sample_count = count

    def to_string(self):
        """
        Returns a string containing information about the class
        :return:
        """
        return 'scene_name = {} \n' \
               'filepath = {} \n' \
               'extension = {} \n' \
               'sampleCount = {}'.format(self._scene_name,
                                         self._output_filepath,
                                         self._extension,
                                         self._sample_count)
