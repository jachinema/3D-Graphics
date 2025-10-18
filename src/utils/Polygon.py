from utils.Point import Point, Point2D, Point3D
from exceptions.GraphicsExceptions import PolygonVertexError, PolygonFaceError

class Polygon:
    def __init__(self, vertices: list[Point], color: tuple[int]):
        """
        Constructs a polygon with given vertices, such that the i'th element of vertices is directly connected to the (i+1)'th element
        and the last is connected to the first.
        """
        if len(vertices) < 3:
            PolygonVertexError("Polygon with fewer than 3 vertices (line, point or empty) cannot be constructed.")

        T = type(vertices[0])

        for vertex in vertices:
            if type(vertex) is not T:
                raise PolygonVertexError
            
        self.vertices = vertices
        self.color = color
    
    def vertices_to_tuple(self) -> tuple[tuple[float]]:
        return tuple(p.coords for p in self.vertices)

class Polygon2D(Polygon):
    def __init__(self, vertices: list[Point2D], color: tuple[int] = (0, 0, 255)):
        if len(vertices) < 3:
            PolygonVertexError("2D Polygon with fewer than 3 vertices (line, point or empty) cannot be constructed.")

        for vertex in vertices:
            if type(vertex) is not Point2D:
                raise PolygonVertexError
        
        self.vertices = vertices
        self.color = color

class Face(Polygon):
    """
    A face is essentially a 2D Polygon positioned in 3D space. Useful and needed for 3D polygons.
    This is also a reason why Polygon3D is not a Polygon subclass, it essentially acts as a manager for Faces instead.
    """
    def __init__(self, vertices: list[Point3D], color: tuple[int] = (0, 0, 255)):
        if len(vertices) < 3:
            PolygonVertexError("Face with fewer than 3 vertices (line, point or empty) cannot be constructed.")

        for vertex in vertices:
            if type(vertex) is not Point3D:
                raise PolygonVertexError
        
        self.vertices = vertices
        self.color = color

class Polygon3D:
    """
    Note that this class is deliberately not a subclass of Polygon (as counterintuitive as that unfortunately is.)
    It is most effective to consider a 3D Polygon as a collection of 2D Polygons as faces in a sort of tree-like structure, which does not
    fit the mold Polygon wants to enforce.
    """

    def __init__(self, faces: list[Face]):

        if len(faces) < 4:
            raise PolygonFaceError("Polygon3D with fewer than 4 faces cannot be constructed.")

        for face in faces:
            if type(face) is not Polygon2D:
                raise PolygonFaceError

        self.faces = faces 

        histogram = dict()
        for face in faces:
            for point in face.vertices:
                histogram[point] = histogram.setdefault(point, 0) + 1
        
        for key in histogram:
            if histogram[key] < 2:
                raise PolygonFaceError("Unclosed Polygon3D, one or more faces has at least one free-hanging vertex.")
            