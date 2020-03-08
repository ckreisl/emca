from Model.path_data import PathData
import numpy as np
import logging


class RenderData(object):

    """
        DataView
        Represents information about one pixel.
        The data is computed on the server side in the pixel re-rendering step.
        Containing all information about all traced paths through this pixel with all user added information.
    """

    def __init__(self):
        # amount of used samples per pixel
        self._sample_count = None
        # {sample_index / path_index : PathData}
        self._dict_paths = {}

    def deserialize(self, stream):
        """
        Deserialize a DataView object from the socket stream
        :param stream:
        :return:
        """
        self._sample_count = stream.read_uint()
        self._dict_paths.clear()
        logging.info("SampleCount: {}".format(self._sample_count))
        # deserialize the amount of paths which were traced through the selected pixel
        for sample in range(0, self._sample_count):
            path_data = PathData()
            path_data.deserialize(stream)
            # append deserialized path to dict
            self._dict_paths[path_data.sample_idx] = path_data

    def deserialize_xml(self, node):
        """
        Deserialize a DataView object from a xml file
        :param node:
        :return:
        """
        self._dict_paths.clear()
        for item in list(node):
            if item.tag == "integer" and item.attrib["name"] == "pathCount":
                self._sample_count = int(item.text)
            elif item.tag == "path":
                path_data = PathData()
                path_data.deserialize_xml(item)
                self._dict_paths[path_data.sample_idx] = path_data

    @property
    def dict_paths(self):
        """
        Returns a dict containing all traced paths through the pixel
        :return: dict{path_idx : PathData, ...}
        """
        return self._dict_paths

    @property
    def sample_count(self):
        """
        Returns the sample count
        :return: integer
        """
        return self._sample_count

    def valid_sample_count(self):
        """
        Checks if the sample count is valid != 0
        :return:
        """
        return self._sample_count != 0

    def get_indices(self):
        """
        Returns all path indices as numpy array
        :return: numpy array
        """
        return np.array(list(self._dict_paths.keys()))

    def to_string(self):
        """
        Returns a string with class information
        :return: string
        """
        return 'sampleCount = {} \n' \
               'dictPathsSize = {}'.format(self._sample_count, len(self._dict_paths))

    def clear(self):
        """
        Clears the data
        :return:
        """
        self._sample_count = None
        self._dict_paths.clear()
