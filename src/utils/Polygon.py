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
    
    def center(self):
        tx = 0
        ty = 0
        tz = 0

        for point in self.vertices:
            tx += point.x
            ty += point.y 
            tz += point.z 

        tx /= len(self.vertices)
        ty /= len(self.vertices)
        tz /= len(self.vertices)

        return Point3D(tx, ty, tz)

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
            if type(face) is not Face:
                raise PolygonFaceError

        self.faces = faces 

        histogram = dict()
        for face in faces:
            for point in face.vertices:
                histogram[str(point)] = histogram.setdefault(str(point), 0) + 1
        
        for key in histogram:
            if histogram[key] < 2:
                raise PolygonFaceError("Unclosed Polygon3D, one or more faces has at least one free-hanging vertex.")

class Prism(Polygon3D):
    def __init__(self, origin: Point3D, xedge: float, yedge: float, zedge: float):
        left, top, front = origin.coords

        front_face = Face([
            Point3D(left, top, front),
            Point3D(left, top+yedge, front),
            Point3D(left+xedge, top+yedge, front),
            Point3D(left+xedge, top, front)
        ])

        back_face = Face([
            Point3D(left, top, front+zedge),
            Point3D(left, top+yedge, front+zedge),
            Point3D(left+xedge, top+yedge, front+zedge),
            Point3D(left+xedge, top, front+zedge)
        ])

        left_face = Face([
            Point3D(left, top, front+zedge),
            Point3D(left, top+yedge, front+zedge),
            Point3D(left, top+yedge, front),
            Point3D(left, top, front)
        ], (255, 255, 0))

        right_face = Face([
            Point3D(left+xedge, top, front+zedge),
            Point3D(left+xedge, top+yedge, front+zedge),
            Point3D(left+xedge, top+yedge, front),
            Point3D(left+xedge, top, front)
        ], (255, 255, 0))

        top_face = Face([
            Point3D(left, top, front+zedge),
            Point3D(left, top, front),
            Point3D(left+xedge, top, front),
            Point3D(left+xedge, top, front+zedge)
        ], (255, 0, 0))

        bottom_face = Face([
            Point3D(left, top+yedge, front+yedge),
            Point3D(left, top+yedge, front),
            Point3D(left+yedge, top+yedge, front),
            Point3D(left+yedge, top+yedge, front+yedge)
        ], (255, 0, 0))

        faces = [back_face, left_face, front_face, right_face, top_face, bottom_face]
        super().__init__(faces)
    
    def center(self) -> tuple[int]:
        centers = []
        for face in self.faces:
            centers.append(face.center())

        # This is not a "real" Face, but it is quite convenient to consider
        # the list of center-points for each Face, as a Face itself, 
        # because we can use this temporary Face to calculate the center of the centers easily.
        abstract = Face(centers) 

        return abstract.center()

class Cube(Prism):
    def __init__(self, origin: Point3D, edge: float):
        super().__init__(origin, edge, edge, edge)

class CompositeShape:
    """
    This class acts in a similar way to Polygon3D. 
    Instead of stitching Faces to create simple objects, this stiches objects to create more interesting ones. 
    """
    def __init__(self, components: list[Polygon3D]):
        self.components = components
        self.all_faces = []

        for component in components:
            self.all_faces.extend(component.faces)
            
