import configparser
import os
import logging


class OptionsConfig(object):

    def __init__(self):
        self._config = configparser.ConfigParser()
        self._path_resources = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Resources'))
        self._filename = 'options.ini'
        self._filepath = os.path.join(self._path_resources, self._filename)
        self._config.read(self._filepath)

    def get_theme(self):
        return self._config['Theme']['theme']

    def set_theme(self, theme):
        if theme == 'dark' or theme == 'light':
            self._config['Theme']['theme'] = theme
        else:
            logging.error("Wrong theme type...(dark|light)")

    def get_option_auto_connect(self):
        try:
            val = self._config['Options']['auto_connect']
            return val == 'True'
        except Exception as e:
            logging.error(e)
            return False

    def set_options_auto_connect(self, value):
        self._config['Options']['auto_connect'] = str(value)

    def get_option_auto_scene_load(self):
        try:
            val = self._config['Options']['auto_scene_load']
            return val == 'True'
        except Exception as e:
            logging.error(e)
            return False

    def set_option_auto_scene_load(self, value):
        self._config['Options']['auto_scene_load'] = str(value)

    def get_option_auto_image_load(self):
        try:
            val = self._config['Options']['auto_rendered_image_load']
            return val == 'True'
        except Exception as e:
            logging.error(e)
            return False

    def set_option_auto_image_load(self, value):
        self._config['Options']['auto_rendered_image_load'] = str(value)

    def get_last_hostname(self):
        return self._config['Last']['hostname']

    def set_last_hostname(self, hostname):
        self._config['Last']['hostname'] = str(hostname)

    def get_last_port(self):
        return int(self._config['Last']['port'])

    def set_last_port(self, port):
        self._config['Last']['port'] = str(port)

    def set_last_hostname_and_port(self, hostname, port):
        if self.get_last_hostname() != hostname:
            self.set_last_hostname(hostname)
        if self.get_last_port() != str(port):
            self.set_last_port(port)

    def get_last_rendered_image_filepath(self):
        return self._config['Last']['rendered_image_filepath']

    def set_last_rendered_image_filepath(self, filepath):
        self._config['Last']['rendered_image_filepath'] = str(filepath)

    def is_last_hostname_set(self):
        return self._config['Last']['hostname'] != ""

    def is_last_port_set(self):
        return self._config['Last']['port'] != ""

    def is_last_rendered_image_filepath_set(self):
        return self._config['Last']['rendered_image_filepath'] != ""

    def save(self):
        with open(self._filepath, 'w') as configfile:
            self._config.write(configfile)
