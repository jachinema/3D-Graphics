from exceptions.GraphicsExceptions import PointDimensionException, PointImplementationError
from utils.functions import depth_attenuation
from constants import VIEWPORT_RESOLUTION
import math

class Point:
    def dist(self, other):
        """
        Returns euclidean distance between self and other
        """
        if isinstance(other, Point):
            p1, p2 = self.coords, other.coords
            p1_dim, p2_dim = len(p1), len(p2)

            if p1_dim != p2_dim: raise PointDimensionException(f"Point dimension mismatch in distance operation: {p1} and {p2}")

            return math.sqrt(sum( (p1[pos] - p2[pos])**2 for pos in range(p1_dim) ))
        else:
            raise ValueError(f"Distance calculation between Point and non-Point: dist({self}, {other})")

    def __add__(self, other):
        if isinstance(other, Point):
            p1, p2 = self.coords, other.coords
            p1_dim, p2_dim = len(p1), len(p2)
            cls = type(self) # We record the class here so that any subclass of Point can add with itself so long as it is defined in the expected format.
            
            if p1_dim != p2_dim: raise PointDimensionException(f"Point dimension mismatch in addition operation: {p1} and {p2}")

            try:
                new = cls(*tuple(p1[pos] + p2[pos] for pos in range(p1_dim)))
                return new 
            except TypeError:
                raise PointImplementationError
        else:
            raise ValueError(f"Addition for Point objects only supported between other Point objects: attempted {self} + {other}")

    def __sub__(self, other):
        if isinstance(other, Point):
            p1, p2 = self.coords, other.coords
            p1_dim, p2_dim = len(p1), len(p2)
            cls = type(self) # We record the class here so that any subclass of Point can add with itself so long as it is defined in the expected format.
            
            if p1_dim != p2_dim: raise PointDimensionException(f"Point dimension mismatch in subtraction operation: {p1} and {p2}")
    
            try:
                new = cls(*tuple(p1[pos] - p2[pos] for pos in range(p1_dim)))
                return new 
            except TypeError:
                raise PointImplementationError
        else:
            raise ValueError(f"Subtraction for Point objects only supported between other Point objects: attempted {self} - {other}")
    
    def __rsub__(self, other):
        """
        This should only be called in cases like 3 - Point(...). If left-hand is a Point, this should not be raised unless overriden poorly.
        """
        raise ValueError(f"Subtraction for Point objects only supported between other Point objects: attempted {other} - {self}")
    
    def __mul__(self, other):
        if isinstance(other, Point):
            raise ValueError(f"Multiplication and division not supported between two Point objects. Did you mean to use a scalar? Attempted: {self} * {other}")
        elif isinstance(other, (int, float)):
            cls = type(self)
            try:
                new = cls(*tuple(other * component for component in self.coords))
                return new
            except TypeError:
                return PointImplementationError
        else:
            # NotImplemented is raised to support Point() * ClientType behavior (so long as ClientType implements __rmul__)
            raise NotImplemented
    
    def __rmul__(self, other):
        return self * other

    def __div__(self, other):
        if isinstance(other, Point):
            raise ValueError(f"Multiplication and division not supported between two Point objects. Did you mean to use a scalar? Attempted: {self} / {other}")
        elif isinstance(other, (int, float)):
            return self * (1/other)
        else:
            # NotImplemented is raised to support Point() * ClientType behavior (so long as ClientType implements __rdiv__)
            raise NotImplemented
    
    def __rdiv__(self, other):
        raise ValueError(f"Only multiplication supported on left side of expression with Point objects due to ambiguity of meaning for expressions of form: x / Point")

    def __pow__(self, other):
        raise ValueError(f"Exponentiation not supported for Point objects: {self}**{other}")

    def __neg__(self):
        cls = type(self)
        try:
            new = cls(*tuple(-component for component in self.coords))
            return new 
        except TypeError:
            raise PointImplementationError
    
    def __getitem__(self, key):
        if isinstance(key, int):
            return self.coords[key]
        elif isinstance(key, slice):
            return self.coords[key.start:key.stop:key.step]
        else:
            raise TypeError(f"Point indices can only be int or slice, got {type(key)} instead.")
    
    def __str__(self):
        classname = type(self).__name__ 
        return f'{classname}{self.coords}'
    
    def setx(self, val):
        self.x = val 
        
        coords = list(self.coords)
        coords[0] = val 

        self.coords = tuple(coords)
    
    def sety(self, val):
        self.y = val 
        
        coords = list(self.coords)
        coords[1] = val 

        self.coords = tuple(coords)

class Point2D(Point):
    def __init__(self, x: float, y: float) -> 'Point2D':
        self.x = x
        self.y = y 
    
        self.coords = (x, y)
    
    def direction(self, other: 'Point2D'):
        """
        Returns Point object as an abstract representation of a 2D Vector.
        """
        if not isinstance(other, Point2D): raise NotImplemented

        dy = other.y - self.y 
        dx = other.x - self.x

        if dx == 0:
            dx += 1e-7
        
        angle = math.atan(dy/dx)

        return Point2D(math.cos(angle), math.sin(angle))
    
class Point3D(Point):
    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

        self.coords = (x, y, z)

    def setz(self, val):
        self.z = val 
        
        coords = list(self.coords)
        coords[2] = val 

        self.coords = tuple(coords)

    def to_2D(self: 'Point3D') -> Point2D:
        flattened = Point2D(self.x, self.y)

        viewport_width, viewport_height = VIEWPORT_RESOLUTION
        center_x, center_y = viewport_width/2, viewport_height/2
        vanishing_point = Point2D(center_x, center_y)

        dx = vanishing_point.x - flattened.x
        dy = vanishing_point.y - flattened.y 

        if dx != 0:
            sign = dx / abs(dx)
        else:
            sign = -(dy / abs(dy))

        return flattened + depth_attenuation(self.z) * flattened.dist(vanishing_point) * (flattened.direction(vanishing_point) * sign)
        