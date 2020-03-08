import OpenEXR
import Imath
from PIL import Image
from PIL.ImageQt import ImageQt as PilImageQt
from PyQt5.QtGui import QPixmap
import array
import logging
import os
import time
import numpy as np
import matplotlib.pyplot as plt
import io
import threading

class HDRImage(object):

    """
        HDRImage
        Class representing a HDR (exr) image
    """

    def __init__(self, filepath=None, falsecolor=False):

        if isinstance(filepath, io.BytesIO):
            logging.info("Loading EXR from bytestream.")
            self._filepath = filepath
        else:
            if filepath:
                self._path, self._extension = os.path.splitext(filepath)

            if self._path.endswith(".exr"):
                self._filepath = self._path
            else:
                self._filepath = self._path + self._extension

            logging.info("Filepath: {}".format(self._filepath))

        self._exr = None
        self._pixmap = None
        self._exposure = 0.0
        self._falsecolor = falsecolor

        self.load_exr(self._filepath)

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

    def load_exr(self, filepath):
        """
        Loads an exr file with OpenEXR
        :param filepath: string
        :return:
        """
        self._exr = OpenEXR.InputFile(filepath)

    def apply_exposure(self, r, g, b):
        if self._exposure == 0.0:
            return (r, g, b)

        factor = np.power(2.0, self._exposure)

        r_exp = r*factor
        g_exp = g*factor
        b_exp = b*factor

        return (r_exp, g_exp, b_exp)

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
