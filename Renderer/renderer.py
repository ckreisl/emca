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

from Renderer.interactor_rubberband import RubberBandInteractor
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from Renderer.meshes import Meshes
from Renderer.camera import Camera
from Renderer.path import Path
from Renderer.vertex import Vertex
from PyQt5.QtWidgets import QFrame
import vtk
import time
import logging
import numpy as np
import threading


class Renderer(object):

    """
        SceneView
        Represents the render which visualizes all 3D objects within the 3D viewer
        Therefore, a vtkRenderer is used.
        Handles all interactions and visualizations.
    """

    def __init__(self):
        # widget
        self._frame = QFrame()
        self._vtkWidget = QVTKRenderWindowInteractor(self._frame)

        # widget update timer
        self._vtk_update_timer = None
        self._vtk_update_timer_running = False

        # renderer
        self._renderer = vtk.vtkRenderer()
        self._renderer.SetBackground(0.7, 0.7, 0.7)

        # Overall scene light
        light_kit = vtk.vtkLightKit()
        light_kit.SetKeyLightIntensity(1.0)
        light_kit.SetKeyLightWarmth(0.5)
        light_kit.AddLightsToRenderer(self._renderer)

        self._vtkWidget.GetRenderWindow().AddRenderer(self._renderer)
        self._iren = self._vtkWidget.GetRenderWindow().GetInteractor()

        #style = MouseInteractor(parent=self)
        style = RubberBandInteractor(parent=self)
        style.SetDefaultRenderer(self._renderer)
        self._iren.SetInteractorStyle(style)

        # set picket to allow rubber band picker (rectangle 3D selection)
        area_picker = vtk.vtkAreaPicker()
        area_picker.AddObserver(vtk.vtkCommand.EndPickEvent, self.area_picker_event)
        self._iren.SetPicker(area_picker)

        self._camera = None
        self._meshes = Meshes()

        self._paths = {}
        self._path_indices = np.array([], dtype=np.int32)
        self._selected_path = False
        self._selected_path_index = -1
        self._selected_vertex = False
        self._selected_vertex_tpl = ()

        self._all_paths_visible = False
        self._all_verts_visible = False

        self._iren.Initialize()
        self._iren.Start()

    def vtkWidget_update_from_timer(self):
        self._vtkWidget.update()
        self._vtk_update_timer_running = False

    @property
    def widget(self):
        """
        Returns the widget containing the renderer view
        :return: vtkWidget
        """
        return self._vtkWidget

    def send_update_path(self, indices, add_item):
        """
        Gets overwritten by view render scene
        :param indices:
        :param add_item:
        :return:
        """
        pass

    def send_select_path(self, index):
        """
        Gets overwritten by view render scene
        :param index:
        :return:
        """
        pass

    def send_select_vertex(self, tpl):
        """
        Gets overwritten by view render scene
        :param tpl:
        :return:
        """
        pass

    def area_picker_event(self, picker, event):
        """
        Handles the rubber band selector,
        check if items gets selected and informs the controller about it
        :param picker:
        :param event:
        :return:
        """
        props = picker.GetProp3Ds()
        props.InitTraversal()
        picked = props.GetNumberOfItems()
        for i in range(0, picked):
            prop = props.GetNextProp3D()
            if isinstance(prop, Vertex):
                tpl = prop.get_index_tpl()
                if tpl[0] in self._path_indices:
                    # same path select vertex
                    if tpl[0] != self._selected_path_index:
                        self.send_select_path(tpl[0])
                    self.send_select_vertex(tpl)
                    break
                else:
                    # some other path is selected update whole view
                    self.send_update_path(np.array([tpl[0]]), False)
                    self.send_select_path(tpl[0])
                    self.send_select_vertex(tpl)
                    break

    def load_camera(self, camera_data):
        """
        Loads the camera data from the Model,
        initialises the vtkCamera
        :param camera_data: CameraData Model
        :return:
        """
        self._camera = Camera(camera_data)
        self._renderer.SetActiveCamera(self._camera)
        self._vtkWidget.update()

    def load_mesh(self, mesh_data):
        """
        Loads a mesh from the models mesh data,
        initialise a mesh as vtkActor for visualization
        :param mesh_data: MeshData
        :return:
        """
        self._meshes.add_mesh(mesh_data)
        self._renderer.AddActor(self._meshes.meshes[-1])
        #updating the QT widget is expensive, delay the update using a timer
        #self._vtkWidget.update()
        if not self._vtk_update_timer_running:
            self._vtk_update_timer_running = True
            self._vtkUpdateTimer = threading.Timer(0.1, self.vtkWidget_update_from_timer)
            self._vtkUpdateTimer.start()

    def load_scene(self, camera_data, mesh_data):
        """
        Loads the whole scene with all meshes and camera information from the models data.
        Visualizes all mesh objects within the scene.
        :param camera_data: CameraData
        :param mesh_data: MeshesData
        :return:
        """
        self.clear_scene_objects()
        self._camera = Camera(camera_data)
        self._meshes.load_from_mesh_data(mesh_data)
        self._renderer.SetActiveCamera(self._camera)
        for mesh in self._meshes.meshes:
            self._renderer.AddActor(mesh)
        self._vtkWidget.update()

    def load_traced_paths(self, render_data):
        """
        Initialises the 3D path structure from the render data of the model.
        Necessary for path visualization.
        :param render_data: DataView
        :return:
        """
        start = time.time()
        self.clear_paths()
        try:
            for key, path in render_data.dict_paths.items():
                self._paths[key] = Path(idx=key,
                                        origin=path.path_origin,
                                        path_data=path)
        except Exception as e:
            logging.error(e)
        logging.info("creating traced paths runtime: {}ms".format(time.time() - start))

    def prepare_new_data(self):
        """
        Prepare render view for new incoming render data,
        is called if a new pixel is clicked and its corresponding data is computed.
        :return:
        """
        self.clear_paths()
        self._paths.clear()
        self._path_indices = np.array([], dtype=np.int32)
        self._selected_path = False
        self._selected_path_index = -1
        self._selected_vertex = False
        self._selected_vertex_tpl = ()
        self._all_paths_visible = False
        self._all_verts_visible = False

    def reset_scene(self):
        """
        Resets the camera view to its default position and view
        :return:
        """
        if self._camera:
            self._camera.reset()
            self._vtkWidget.update()

    def take_screenshot(self, filename):
        """
        Takes a screenshot of the vtkRenderer view and saves it under the given filename
        :param filename: string
        :return:
        """
        w2if = vtk.vtkWindowToImageFilter()
        w2if.SetInput(self._vtkWidget.GetRenderWindow())
        w2if.Update()
        writer = vtk.vtkPNGWriter()
        writer.SetFileName(filename)
        writer.SetInputConnection(w2if.GetOutputPort())
        writer.Write()

    def clear_scene_objects(self):
        """
        Clears all scene / mesh objects within the scene view
        :return:
        """
        if self._meshes:
            for mesh in self._meshes.meshes:
                self._renderer.RemoveActor(mesh)
            self._vtkWidget.update()

    def clear_paths(self):
        """
        Clears all paths within the scene view
        :return:
        """
        if self._paths:
            for key, path in self._paths.items():
                path.clear_all(self._renderer)
            self._paths.clear()
            self._vtkWidget.update()

    def clear_paths_by_indices(self, indices):
        """
        Clears a subset of paths from the scene.
        All paths whose index is within indices will be cleared
        :param indices: numpy array containing path indices
        :return:
        """
        if self._paths:
            for i in indices:
                self._paths[i].clear_path(self._renderer)
            self._vtkWidget.update()

    def clear_verts_by_indices(self, indices):
        """
        Clears a subset of vertices from the scene.
        All vertices whose index is within indices will be cleared
        :param indices: numpy array containing vertices indices
        :return:
        """
        if self._paths:
            for i in indices:
                self._paths[i].clear_verts(self._renderer)
            self._vtkWidget.update()

    def set_camera_focus(self, pos):
        """
        Sets the camera focus to position pos.
        If no camera is set nothing will happen.
        :param pos: point3f
        :return:
        """
        if self._camera:
            self._camera.set_focal_point(pos)
            self._vtkWidget.update()

    def display_traced_paths(self, indices):
        """
        Display traced paths within the 3D scene viewer.
        All paths which are within the indices list will be displayed.
        :param indices: numpy array containing path indices
        :return:
        """
        # clear paths which are not visible anymore
        # and reset path opacity if a path was selected with others
        if np.size(self._path_indices) > 0:
            if self._selected_path:
                self.reset_path_opacity(self._path_indices)
                self._selected_path = False
            if self._selected_vertex:
                self.reset_vertex_opacity(self._path_indices)
                self._selected_vertex = False
            diff = np.setdiff1d(self._path_indices, indices)
            if not self._all_paths_visible:
                self.clear_paths_by_indices(diff)
            if not self._all_verts_visible:
                self.clear_verts_by_indices(diff)
        # update indices list
        self._path_indices = indices
        # draw selected paths with indices list
        if self._paths:
            for i in self._path_indices:
                self._paths[i].draw_path(self._renderer)
                self._paths[i].draw_verts(self._renderer)
            self._vtkWidget.update()

    def display_traced_verts(self, indices):
        """
        Displays vertices within the 3D scene viewer.
        All vertices which are within the indices list will be displayed
        :param indices: numpy array with vertices indices
        :return:
        """
        # clear paths which are not visible anymore
        if np.size(self._path_indices) > 0:
            if self._selected_vertex:
                self.reset_vertex_opacity(self._path_indices)
                self._selected_vertex = False
            diff = np.setdiff1d(self._path_indices, indices)
            self.clear_paths_by_indices(diff)
        # update indices list
        self._path_indices = indices
        # draw selected paths with indices list
        if self._paths:
            for i in self._path_indices:
                self._paths[i].draw_verts(self._renderer)
            self._vtkWidget.update()

    def select_path(self, index):
        """
        Select one path by its index.
        The opacity of all other visible paths will be reduced.
        :param index: integer - path index
        :return:
        """
        for i in self._path_indices:
            if i == index:
                path = self._paths[i]
                if path.is_ne_visible:
                    path.draw_ne(self._renderer)
                if path.opacity == path.default_opacity:
                    continue
                self._paths[i].set_path_opacity(path.default_opacity)
                continue
            self._paths[i].set_path_opacity(0.25)
        self._selected_path = True
        self._selected_path_index = index
        self._vtkWidget.update()

    def select_vertex(self, tpl):
        """
        Selects a vertex, highlights it.
        :param tpl: tuple(path_index, vertex_index)
        :return:
        """
        # tpl = (path_idx, vertex_idx)
        if not self._selected_vertex:
            self._selected_vertex = True
        if self._selected_vertex_tpl:
            path = self._paths[self._selected_vertex_tpl[0]]
            vert = path.its_dict[self._selected_vertex_tpl[1]]
            vert.set_selected(False)
        self._selected_vertex_tpl = tpl
        path = self._paths[tpl[0]]
        vert = path.its_dict[tpl[1]]
        if vert.is_ne_visible:
            vert.draw_ne(self._renderer)
        if vert.is_wi_visible:
            vert.draw_wi(self._renderer)
        if vert.is_wo_visible:
            vert.draw_wo(self._renderer)
        # check if clipping is enabled
        if self._camera:
            if self._camera.auto_clipping:
                self.set_camera_focus(vert.pos)
        vert.set_selected(True)
        self._vtkWidget.update()

    def reset_path_opacity(self, indices):
        """
        Resets the path opacity of all paths whose index is within indices
        :param indices: numpy array with path indices
        :return:
        """
        for i in indices:
            self._paths[i].reset_path_opacity()

    def reset_vertex_opacity(self, indices):
        """
        Resets all vertices opacity of all vertices whose index is within indices
        :param indices: numpy array with vertex indices
        :return:
        """
        for i in indices:
            self._paths[i].reset_vertex_opacity()

    # Render Options functions

    def camera_clipping(self):
        """
        Returns if camera view clipping to a vertex is enabled
        :return: boolean
        """
        return self._camera.auto_clipping

    def get_camera_motion_speed(self):
        """
        Returns the camera motion speed
        :return: float
        """
        return self._camera.motion_speed

    def get_scene_opacity(self):
        """
        Returns the scene opacity (default 0.25)
        :return:
        """
        return self._meshes.opacity

    def update_camera_motion_speed(self, speed):
        """
        Sets the camera motion speed
        :param speed: float
        :return:
        """
        self._camera.motion_speed = speed

    def update_camera_clipping(self, state):
        """
        Sets the camera clipping
        :param state: boolean
        :return:
        """
        self._camera.auto_clipping = state

    def reset_camera_motion_speed(self):
        """
        Resets the camera motion speed to its default 1.0
        :return:
        """
        self._camera.reset_motion_speed()

    def update_scene_opacity(self, opacity):
        """
        Updates the scene opacity containing all objects
        :param opacity: float[0,1]
        :return:
        """
        self._meshes.set_opacity(opacity)
        self._vtkWidget.update()

    def reset_scene_opacity(self):
        """
        Resets the scene opacits to its default value 0.25
        :return:
        """
        self._meshes.reset_opacity()
        self._vtkWidget.update()

    # General Settings

    def show_all_nees(self, state):
        """
        Depending on state, displays all next event estimation paths within the 3D viewer
        :param state: boolean
        :return:
        """
        if state:
            for key, path in self._paths.items():
                path.draw_ne(self._renderer)
                path.is_ne_visible = True
        else:
            for key, path in self._paths.items():
                path.clear_ne(self._renderer)
                path.is_ne_visible = False
        self._vtkWidget.update()

    def show_all_paths(self, state):
        """
        Depending on state, displays all traced paths
        :param state: boolean
        :return:
        """
        if state:
            for key, path in self._paths.items():
                path.draw_path(self._renderer)
                path.is_visible = True
        else:
            for key, path in self._paths.items():
                if key not in self._path_indices:
                    path.clear_path(self._renderer)
                    path.is_visible = False
        self._vtkWidget.update()

    def show_all_verts(self, state):
        """
        Depending on state, displays all vertices
        :param state:
        :return:
        """
        if state:
            for key, path in self._paths.items():
                path.draw_verts(self._renderer)
        else:
            for key, path in self._paths.items():
                if key not in self._path_indices:
                    path.clear_verts(self._renderer)
        self._vtkWidget.update()

    # Path settings

    def get_selected_path_index(self):
        """
        Returns the index of the current selected path
        :return: integer
        """
        return self._selected_path_index

    def get_selected_vertex_tpl(self):
        """
        Returns the vertex tuple of the current selected vertex
        :return: tuple(path_index, vertex_index)
        """
        return self._selected_vertex_tpl

    def get_path_opacity(self, index):
        """
        Returns the opacity of the path with index: index
        :param index: integer
        :return:
        """
        return self._paths[index].opacity

    def get_path_size(self, index):
        """
        Return the path size of the path with index: index
        :param index: integer
        :return:
        """
        return self._paths[index].size

    def get_is_visible_path(self, index):
        """
        Returns if the path with its index: index is visible
        :param index: integer
        :return:
        """
        return self._paths[index].is_visible

    def get_is_ne_visible_path(self, index):
        """
        Returns if next event estimations are visible of the path with index: index
        :param index: integer
        :return:
        """
        return self._paths[index].is_ne_visible

    def update_path_opacity(self, opacity):
        """
        Updates the path opacity of the selected path
        :param opacity: float[0,1]
        :return:
        """
        self._paths[self._selected_path_index].set_path_opacity(opacity)
        self._vtkWidget.update()

    def update_path_size(self, size):
        """
        Updates the path size of the selected path
        :param size: float[0,1]
        :return:
        """
        self._paths[self._selected_path_index].set_path_size(size)
        self._vtkWidget.update()

    def reset_path(self):
        """
        Resets size and opacity of the selected path
        :return:
        """
        self._paths[self._selected_path_index].reset_path()
        self._vtkWidget.update()

    def show_traced_path(self, state):
        """
        Depending on state, shows the current selected path
        :param state: boolean
        :return:
        """
        path = self._paths[self._selected_path_index]
        if state:
            if not path.is_visible:
                path.draw_path(self._renderer)
                path.is_visible = True
        else:
            if path.is_visible:
                path.clear_path(self._renderer)
                path.is_visible = False
        self._vtkWidget.update()

    def show_traced_path_nee(self, state):
        """
        Depending on state, shows the next event estimations of the current selected path
        :param state: boolean
        :return:
        """
        for path_key in self._path_indices:
            path = self._paths.get(path_key, None)
            if path:
                if state:
                    if not path.is_ne_visible:
                        path.draw_ne(self._renderer)
                        path.is_ne_visible = True
                else:
                    if path.is_ne_visible:
                        path.clear_ne(self._renderer)
                        path.is_ne_visible = False
        self._vtkWidget.update()

    def show_other_paths(self, state):
        """
        Depending on state, shows all other paths besides the selected one(s)
        :param state: boolean
        :return:
        """
        if state:
            if not self._all_paths_visible:
                for key, path in self._paths.items():
                    if key not in self._path_indices:
                        path.draw_path(self._renderer)
                self._all_paths_visible = not self._all_paths_visible
        else:
            if self._all_paths_visible:
                for key, path in self._paths.items():
                    if key not in self._path_indices:
                        path.clear_path(self._renderer)
                self._all_paths_visible = not self._all_paths_visible
        self._vtkWidget.update()

    # Vertex settings

    def get_vertex_to_tpl(self, tpl):
        """
        Returns the vertex to its tuple
        :param tpl: tuple(path_index, vertex_index)
        :return:
        """
        path = self._paths[tpl[0]]
        return path.its_dict[tpl[1]]

    def is_wi_visible(self, tpl):
        """
        Returns if the incoming ray is visible of the vertex is visible
        :param tpl: tuple(path_index, vertex_index)
        :return:
        """
        vert = self.get_vertex_to_tpl(tpl)
        return vert.is_wi_visible

    def is_wo_visible(self, tpl):
        """
        Returns if the outgoing ray is visible of the vertex is visible
        :param tpl: tuple(path_index, vertex_index)
        :return:
        """
        vert = self.get_vertex_to_tpl(tpl)
        return vert.is_wo_visible

    def is_ne_visible(self, tpl):
        """
        Returns if the next event estimation of the vertex is visible
        :param tpl: tuple(path_index, vertex_index)
        :return:
        """
        vert = self.get_vertex_to_tpl(tpl)
        return vert.is_ne_visible

    def get_vertex_opacity(self, tpl):
        """
        Returns the opacity of the vertex
        :param tpl: tuple(path_index, vertex_index)
        :return:
        """
        vert = self.get_vertex_to_tpl(tpl)
        return vert.opacity

    def get_vertex_size(self, tpl):
        """
        Returns the size of the vertex
        :param tpl: tuple(path_index, vertex_index)
        :return:
        """
        vert = self.get_vertex_to_tpl(tpl)
        return vert.size

    def update_vertex_opacity(self, opacity):
        """
        Updates the opacity of the current selected vertex
        :param opacity: float[0,1]
        :return:
        """
        vert = self.get_vertex_to_tpl(self._selected_vertex_tpl)
        vert.set_vertex_opacity(opacity)
        self._vtkWidget.update()

    def update_vertex_size(self, size):
        """
        Updates the size of the current selected vertex
        :param size: float[0,1]
        :return:
        """
        vert = self.get_vertex_to_tpl(self._selected_vertex_tpl)
        vert.set_vertex_size(size)
        self._vtkWidget.update()

    def reset_vertex(self):
        """
        Resets the opacity and size of the current selected vertex
        :return:
        """
        vert = self.get_vertex_to_tpl(self._selected_vertex_tpl)
        vert.reset_vertex()
        self._vtkWidget.update()

    def show_vertex_omega_i(self, state):
        """
        Depending on state, shows the incoming ray of the vertex (intersection)
        :param state: boolean
        :return:
        """
        vert = self.get_vertex_to_tpl(self._selected_vertex_tpl)
        if state:
            vert.draw_wi(self._renderer)
        else:
            vert.clear_wi(self._renderer)
        self._vtkWidget.update()

    def show_vertex_omega_o(self, state):
        """
        Depending on state, shows the outgoing ray of the vertex (intersection)
        :param state: boolean
        :return:
        """
        vert = self.get_vertex_to_tpl(self._selected_vertex_tpl)
        if state:
            vert.draw_wo(self._renderer)
        else:
            vert.clear_wo(self._renderer)
        self._vtkWidget.update()

    def show_vertex_nee(self, state):
        """
        Depending on state, shows the next event estimation ray of the vertex (intersection)
        :param state: boolean
        :return:
        """
        vert = self.get_vertex_to_tpl(self._selected_vertex_tpl)
        if state:
            vert.draw_ne(self._renderer)
        else:
            vert.clear_ne(self._renderer)
        self._vtkWidget.update()

    def show_other_verts(self, state):
        """
        Depending on state, shows all other vertices besides the selected one(s)
        :param state: boolean
        :return:
        """
        if state:
            if not self._all_verts_visible:
                for path_idx, path in self._paths.items():
                    if path_idx not in self._path_indices:
                        for vert_idx, vert in path.its_dict.items():
                            vert.draw_vert(self._renderer)
                self._all_verts_visible = not self._all_verts_visible
        else:
            if self._all_verts_visible:
                for path_idx, path in self._paths.items():
                    if path_idx not in self._path_indices:
                        for vert_idx, vert in path.its_dict.items():
                            vert.clear_vert(self._renderer)
                self._all_verts_visible = not self._all_verts_visible
        self._vtkWidget.update()
