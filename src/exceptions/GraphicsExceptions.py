class GraphicsException(Exception):
    """
    Template for implementing GraphicsExceptions
    """
    pass

class PointDimensionException(GraphicsException):
    def __init__(self, message="Point dimension mismatch."):
        super().__init__(message)

class PointImplementationError(GraphicsException):
        def __init__(self, message="Point subclass constructor defined incorrectly. Should support required style: Point(x, y, z, w, ...)"):
            super().__init__(message)

class PolygonVertexError(GraphicsException):
     def __init__(self, message="Polygon vertices of incorrect or inconsistent type"):
          super().__init__(message)

class PolygonFaceError(GraphicsException):
     def __init__(self, message="Polygon3D faces of incorrect or inconsistent type"):
          super().__init__(message)