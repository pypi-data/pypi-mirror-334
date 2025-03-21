import vtk
import numpy as np

def visualize_simplified_point_cloud(point_cloud: np.ndarray):
    # 创建 VTK 点数据集
    points = vtk.vtkPoints()
    scalars = vtk.vtkFloatArray()

    for point in point_cloud:
        points.InsertNextPoint(point)
        # 假设 y 坐标是 point[1]（根据实际情况调整）
        scalars.InsertNextValue(point[1])

    polydata = vtk.vtkPolyData()
    polydata.SetPoints(points)
    polydata.GetPointData().SetScalars(scalars)

    # 创建顶点单元
    vertices = vtk.vtkCellArray()
    for i in range(point_cloud.shape[0]):
        vertices.InsertNextCell(1)
        vertices.InsertCellPoint(i)
    polydata.SetVerts(vertices)

    # 创建查找表
    lookup_table = vtk.vtkLookupTable()
    lookup_table.SetNumberOfColors(256)
    lookup_table.Build()
    lookup_table.SetHueRange(0.667, 0.0)  # 从蓝色到红色的颜色映射
    lookup_table.SetValueRange(1.0, 1.0)
    lookup_table.SetSaturationRange(1.0, 1.0)

    # 创建映射器和演员
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputData(polydata)
    mapper.SetLookupTable(lookup_table)
    mapper.SetScalarRange(scalars.GetRange())

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetPointSize(2)  # 设置点的大小

    # 创建渲染器、渲染窗口和交互器
    renderer = vtk.vtkRenderer()
    renderer.AddActor(actor)
    renderer.SetBackground(0.1, 0.2, 0.3)  # 设置背景颜色

    render_window = vtk.vtkRenderWindow()
    render_window.AddRenderer(renderer)

    interactor = vtk.vtkRenderWindowInteractor()
    interactor.SetRenderWindow(render_window)

    # 启动交互
    render_window.Render()
    interactor.Start()
