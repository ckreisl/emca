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

from enum import Enum


class ViewMode(Enum):
    CONNECTED       = 1


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
    DATA_3D_PATHS       = 9
    DATA_DETECTOR       = 10
    UPDATE_PLUGIN       = 11
    QUIT                = 12


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


class MeshType(Enum):
    TriangleMesh = 0
    SphereMesh = 1
