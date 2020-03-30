from Core.highlighter_base import HighlighterBase
import numpy as np
import logging


class Highlighter3D(HighlighterBase):

    def __init__(self, figure, axes, callback):
        HighlighterBase.__init__(self, figure, axes, callback)
        self.y = np.array([])
        self.z = np.array([])

    def init_data(self, **kwargs):
        self.x = kwargs['x']
        self.y = kwargs['y']
        self.z = kwargs['z']
        # todo rectangle selector possible?

    def update_all(self, mask):
        pass
