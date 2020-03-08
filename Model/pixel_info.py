from Types.factory import TypeFactory
from Types.point2 import Point2i
from Types.color3 import Color3f
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QImage
from PyQt5.QtGui import QColor
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QPoint
import logging


class PixelInfo(object):

    """
        PixelInfo
        Represents and holds information about a selected pixel
        Pixel color, the position. Is used to display the selected pixel as icon in the view
    """

    def __init__(self):
        self._pixel_icon = QIcon()
        self._pixel_pos = QPoint()
        self._color = QColor()
        self._pixmap = QPixmap(16, 16)

    @property
    def icon(self):
        """
        Returns the pixel icon
        :return: QIcon
        """
        return self._pixel_icon

    @property
    def pixel_pos(self):
        """
        Returns the pixel position
        :return: QPoint
        """
        return self._pixel_pos

    @property
    def pixel_pos_point2i(self):
        """
        Transforms the QPoint pixel position into a Point2i and returns the data type
        :return: Point2i
        """
        return Point2i(self._pixel_pos.x(), self._pixel_pos.y())

    @property
    def pixel_color_color3f(self):
        """
        Transform a QColor into a Color3f object with the pixel color information
        :return: Color3f
        """
        return Color3f(self._color.red(), self._color.green(), self._color.blue(), self._color.alpha())

    def deserialize_xml(self, node):
        """
        Deserializes pixel info information from a xml file
        :param node:
        :return:
        """
        for item in list(node):
            if item.tag == "point2i" and item.attrib["name"] == "pixelPos":
                pos = TypeFactory.create_point2i_from_str(item.text)
                self._pixel_pos = QPoint(pos.x, pos.y)
            elif item.tag == "color3f" and item.attrib["name"] == "pixelColor":
                color = TypeFactory.create_color3f_from_str(item.text)
                self._color = QColor(color.red, color.green, color.blue, color.alpha)
                self._pixmap.fill(self._color)
                self._pixel_icon.addPixmap(self._pixmap)

    def set_pixel(self, pixmap, pixel):
        """
        Sets the pixel position and the icon with the pixmap
        :param pixmap: QPixmap
        :param pixel: QPoint
        :return:
        """
        self._pixel_pos = pixel
        self._color = QColor(QImage(pixmap).pixel(pixel.x(), pixel.y()))
        self._pixmap.fill(self._color)
        self._pixel_icon.addPixmap(self._pixmap)

    def get_pixel_str(self):
        """
        Returns a string with class information
        :return:
        """
        return '({},{})'.format(self._pixel_pos.x(),
                                self._pixel_pos.y())


