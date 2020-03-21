"""
    This file is part of EMCA, an explorer of Monte-Carlo based Algorithms.
    Copyright (c) 2019-2020 by Christoph Kreisl and others.
    EMCA is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License Version 3
    as published by the Free Software Foundation.
    EMCA is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
    GNU General Public License for more details.
    You should have received a copy of the GNU General Public License
    along with this program. If not, see <http://www.gnu.org/licenses/>.
"""

import OpenEXR
import Imath
from PIL import Image
from PIL.ImageQt import ImageQt as PilImageQt
from PyQt5.QtGui import QPixmap
import array
import logging
import os
import numpy as np
import matplotlib.pyplot as plt


class HDRImage(object):

    """
        HDRImage
        Class representing a HDR (exr) image
    """

    def __init__(self):
        self._filepath = None
        self._extension = None
        self._exr = None
        self._pixmap = None
        self._exposure = 0.0
        self._falsecolor = False

    def load_exr_from_bytestream(self, bytestream, falsecolor=False):
        logging.info("Loading EXR from bytestream.")
        if self._pixmap:
            del self._pixmap
            self._pixmap = None
        self._filepath = bytestream
        self._falsecolor = falsecolor
        self.load_exr(bytestream)

    def load_exr_from_filepath(self, filepath, falsecolor=False):
        logging.info("Loading EXR from filepath")
        if self._pixmap:
            del self._pixmap
            self._pixmap = None
        self._filepath = filepath
        self._falsecolor = falsecolor
        self.load_exr(filepath)

    def load_exr(self, filepath):
        """
        Loads an exr file with OpenEXR
        :param filepath: string or bytestream
        :return:
        """
        self._exr = OpenEXR.InputFile(filepath)

    @property
    def exr_image(self):
        """
        Returns the exr image
        :return: OpenEXR
        """
        return self._exr

    @property
    def pixmap(self):
        """
        Returns the render image as pixmap
        :return: QPixmap
        """
        if self._pixmap is None:
            #update pixmap if needed
            try:
                pt = Imath.PixelType(Imath.PixelType.FLOAT)

                r_str = self._exr.channel('R', pt)
                g_str = self._exr.channel('G', pt)
                b_str = self._exr.channel('B', pt)

                r = np.array(array.array('f', r_str), 'f')
                g = np.array(array.array('f', g_str), 'f')
                b = np.array(array.array('f', b_str), 'f')

                (r_exp, g_exp, b_exp) = self.apply_exposure(r, g, b)

                if self._falsecolor:
                    self._pixmap = self.create_pixmap_fc(r_exp, g_exp, b_exp)
                else:
                    self._pixmap = self.create_pixmap_srgb(r_exp, g_exp, b_exp)
            except Exception as e:
                logging.error("Error " + str(e))

        return self._pixmap

    @property
    def exposure(self):
        return self._exposure

    @exposure.setter
    def exposure(self, exposure):
        if self._exposure != exposure:
            self._pixmap = None
        self._exposure = exposure

    @property
    def falsecolor(self):
        return self._falsecolor

    @falsecolor.setter
    def falsecolor(self, falsecolor):
        if self._falsecolor != falsecolor:
            self._pixmap = None
        self._falsecolor = falsecolor

    def apply_exposure(self, r, g, b):
        if self._exposure == 0.0:
            return r, g, b

        factor = np.power(2.0, self._exposure)

        r_exp = r*factor
        g_exp = g*factor
        b_exp = b*factor

        return r_exp, g_exp, b_exp

    def create_pixmap_srgb(self, r_exp, g_exp, b_exp):
        """
        Converts an srgb image to a pixmap
        :param r_exp:
        :param g_exp:
        :param b_exp:
        :return: QPixmap
        """

        #even though this is 2.4, this corresponds to a gamma value of 2.2
        invSRGBGamma = 1.0/2.4

        r_gamma = np.where(r_exp > 0.0031308, ((255.0 * 1.055) * np.power(r_exp, invSRGBGamma) - 0.055), r_exp * (12.92 * 255.0))
        g_gamma = np.where(g_exp > 0.0031308, ((255.0 * 1.055) * np.power(g_exp, invSRGBGamma) - 0.055), g_exp * (12.92 * 255.0))
        b_gamma = np.where(b_exp > 0.0031308, ((255.0 * 1.055) * np.power(b_exp, invSRGBGamma) - 0.055), b_exp * (12.92 * 255.0))

        dw = self._exr.header()['dataWindow']
        size = (dw.max.x - dw.min.x + 1, dw.max.y - dw.min.y + 1)

        srgb = np.uint8([np.uint8(np.clip(r_gamma, 0.0, 255.0)),
                         np.uint8(np.clip(g_gamma, 0.0, 255.0)),
                         np.uint8(np.clip(b_gamma, 0.0, 255.0))]).transpose().reshape([size[1], size[0], 3])

        q_img = PilImageQt(Image.fromarray(srgb, 'RGB'))
        return QPixmap.fromImage(q_img).copy()

    def create_pixmap_fc(self, r_exp, g_exp, b_exp):

        #max_intensity = np.max([r_exp,g_exp,b_exp], axis=0)
        avg_intensity = (r_exp+g_exp+b_exp)/3
        log_intensity = np.where(avg_intensity > 0.0, np.log2(avg_intensity), -float('inf'))/10.0+0.5

        cmap = plt.get_cmap('viridis')

        dw = self._exr.header()['dataWindow']
        size = (dw.max.x - dw.min.x + 1, dw.max.y - dw.min.y + 1)

        srgb = np.uint8(np.array(cmap(log_intensity))[:,:3]*255.0).reshape([size[1], size[0], 3])
        q_img = PilImageQt(Image.fromarray(srgb, 'RGB'))
        return QPixmap.fromImage(q_img).copy()

    def save(self, filename):
        """
        Saves the current exr image under the given filename
        (wrong gamma?! currently problems in saving exr images)
        :param filename: string
        :return:
        """
        dw = self._exr.header()['dataWindow']
        size = (dw.max.x - dw.min.x + 1, dw.max.y - dw.min.y + 1)

        # Read the three color channels as 32-bit floats
        FLOAT = Imath.PixelType(Imath.PixelType.FLOAT)
        (R, G, B) = [array.array('f', self._exr.channel(Chan, FLOAT)).tolist() for Chan in ("R", "G", "B")]

        """
        # Normalize so that brightest sample is 1
        brightest = max(R + G + B)
        R = [i / brightest for i in R]
        G = [i / brightest for i in G]
        B = [i / brightest for i in B]
        """

        (Rs, Gs, Bs) = [array.array('f', Chan).tostring() for Chan in (R, G, B)]

        out = OpenEXR.OutputFile(filename, OpenEXR.Header(size[0], size[1]))
        out.writePixels({'R': Rs, 'G': Gs, 'B': Gs})
