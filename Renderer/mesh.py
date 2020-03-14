import vtk
import logging
import time


class Mesh(vtk.vtkActor):

    """
        Mesh
        Represents a Mesh object within the 3D scene as vtkActor
    """

    def __init__(self, mesh, opacity):
        vtk.vtkActor.__init__(self)

        self._default_opacity = opacity
        self._is_selected = False

        start = time.time()

        vertices = vtk.vtkPoints()
        vertexFloatArray = vtk.vtkFloatArray()
        vertexFloatArray.SetArray(mesh.vertices, mesh.vertex_count*3, True)
        vertexFloatArray.SetNumberOfComponents(3)
        vertexFloatArray.SetNumberOfTuples(mesh.vertex_count)
        vertices.SetData(vertexFloatArray)

        triangles = vtk.vtkCellArray()
        triangleIdArray = vtk.vtkIdTypeArray()
        triangleIdArray.SetArray(mesh.triangles, mesh.triangle_count*4, True)
        triangles.SetCells(mesh.triangle_count, triangleIdArray)

        # remember we got the alpha channel!
        specular_color = mesh.specular_color
        diffuse_color = mesh.diffuse_color

        self.init_mapper(vertices, triangles)
        self.init_properties(diffuse_color, specular_color)

        self._default_color = self.GetProperty().GetColor()

        logging.info('processed mesh containing {} vertices and {} triangles in: {:.3}s' \
            .format(mesh.vertex_count, mesh.triangle_count, time.time() - start))

    @property
    def is_selected(self):
        """
        Returns if the mesh is selected
        :return: boolean
        """
        return self._is_selected

    def init_mapper(self, vertices, triangles):
        """
        Initialise the mesh (vtkActor)
        :param vertices:
        :param triangles:
        :return:
        """
        # mesh poly data
        mesh_poly_data = vtk.vtkPolyData()
        mesh_poly_data.SetPoints(vertices)
        mesh_poly_data.SetPolys(triangles)

        # mapper
        mapper = vtk.vtkPolyDataMapper()
        if vtk.VTK_MAJOR_VERSION <= 5:
            mapper.SetInput(mesh_poly_data)
        else:
            mapper.SetInputData(mesh_poly_data)

        self.SetMapper(mapper)

    def init_properties(self, diffuse_color, specular_color):
        """
        Initialise the properties
        :param diffuse_color:
        :param specular_color:
        :return:
        """
        self.GetProperty().SetLighting(True)
        self.GetProperty().LightingOn()
        self.GetProperty().SetShading(True)
        self.GetProperty().ShadingOn()
        self.GetProperty().SetDiffuseColor(diffuse_color[0], diffuse_color[1], diffuse_color[2])
        self.GetProperty().SetSpecularColor(specular_color[0], specular_color[1], specular_color[2])
        self.GetProperty().SetDiffuse(1)
        self.GetProperty().SetSpecular(1)
        self.GetProperty().SetAmbient(0)
        self.GetProperty().SetOpacity(self._default_opacity)

    def set_selected(self, selected):
        """
        Highlight the mesh object as selected
        :param selected: boolean
        :return:
        """
        if selected:
            self.GetProperty().SetColor(0.3, 0, 0.2)
        else:
            self.GetProperty().SetColor(self._default_color)
        self._is_selected = selected

    @property
    def opacity(self):
        """
        Returns the opacity of the mesh object
        :return: float[0,1]
        """
        return self.GetProperty().GetOpacity()

    @property
    def color(self):
        """
        Returns the color of the mesh object
        :return: vtkColor
        """
        return self.GetProperty().GetColor()

    @property
    def default_opacity(self):
        """
        Returns the default opacity value 1.0
        :return:
        """
        return self._default_opacity

    def set_opacity(self, value):
        """
        Sets the opacity of the mesh object
        :param value: float[0,1]
        :return:
        """
        self.GetProperty().SetOpacity(value)

    def set_color(self, color):
        """
        Sets the color of the mesh object
        :param color: vtkColor
        :return:
        """
        self.GetProperty().SetColor(color)

    def reset(self):
        """
        Resets the mesh opacity and color to default
        :return:
        """
        if self.is_selected:
            self.GetProperty().SetColor(self._default_color)
        self.GetProperty().SetOpacity(self._default_opacity)
        self._is_selected = False
