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