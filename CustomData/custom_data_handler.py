import CustomData
import logging


class CustomDataHandler(object):

    """
        CustomDataHandler

        Handles all CustomData types.
        Loads and inits the classes which are imported and defined in CustomData/__init__.py
    """

    def __init__(self):

        # custom data dictionary {custom_data_id : custom_data, ...}
        self._custom_data = {}

        # loads and initialises the custom data
        for custom_data in [(name, cls()) for name, cls in CustomData.__dict__.items() if isinstance(cls, type)]:
            self._custom_data[custom_data[1].id] = custom_data[1]

    def get_custom_data_by_id(self, unique_id):
        """
        Returns the corresponding custom data to the given unique_id.
        If no data is defined None is returned
        :param unique_id: custom_data_id
        :return: returns None if no custom data is found with the given id
        """
        return self._custom_data.get(unique_id, None)
