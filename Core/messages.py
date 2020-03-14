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

from enum import Enum


class ViewMode(Enum):
    CONNECTED       = 1
    XML             = 2


class StateMsg(Enum):
    DISCONNECT          = 0
    CONNECT             = 1
    SERVER_ERROR        = 2
    DATA_IMAGE          = 3
    DATA_RENDER         = 4
    DATA_CAMERA         = 5
    DATA_MESH           = 6
    DATA_INFO           = 7
    DATA_NOT_VALID      = 8
    DATA_SCATTER_PLOT   = 9
    DATA_3D_PATHS       = 10
    DATA_DETECTOR       = 11
    XML_LOADED          = 12
    QUIT                = 13
    UPDATE_TOOL         = 14


class ServerMsg(Enum):

    EMCA_HELLO                   = 0x0001
    EMCA_HEADER_RENDER_INFO      = 0x000A
    EMCA_SEND_RENDER_INFO        = 0x000B
    EMCA_HEADER_IMAGE_DATA       = 0x000D
    EMCA_HEADER_PIXEL_DATA       = 0x000E
    EMCA_HEADER_SCENE_DATA       = 0x000F
    EMCA_HEADER_CAMERA           = 0x0010
    EMCA_NO_VALID_DATA           = 0x01A4
    EMCA_DISCONNECT              = 0x1bcc
    EMCA_QUIT                    = 0x1bcd

    @staticmethod
    def get_server_msg(flag):
        return {
            0x0001: ServerMsg.EMCA_HELLO,
            0x000A: ServerMsg.EMCA_HEADER_RENDER_INFO,
            0x000B: ServerMsg.EMCA_SEND_RENDER_INFO,
            0x000D: ServerMsg.EMCA_HEADER_IMAGE_DATA,
            0x000E: ServerMsg.EMCA_HEADER_PIXEL_DATA,
            0x000F: ServerMsg.EMCA_HEADER_SCENE_DATA,
            0x01A4: ServerMsg.EMCA_NO_VALID_DATA,
            0x0010: ServerMsg.EMCA_HEADER_CAMERA,
            0x1bcc: ServerMsg.EMCA_DISCONNECT,
            0x1bcd: ServerMsg.EMCA_QUIT
        }.get(flag, None)
