from __future__ import annotations
from exceptions.GraphicsExceptions import PointDimensionException, PointImplementationError
from utils.functions import depth_attenuation
from constants import VIEWPORT_RESOLUTION
import math

class Point:
    def __init__(self, x: int | float, y: int | float, *higher: int | float):
        self.coords = (x, y, *higher)


    def dist(self, other: Point) -> float:
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

    def __add__(self, other: Point) -> Point:
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

    def __sub__(self, other: Point) -> Point:
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
    
    def __mul__(self, other: Point | int | float) -> Point:
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
    
    def __rmul__(self, other) -> Point:
        return self * other

    def __div__(self, other: int | float) -> Point:
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

    def __neg__(self) -> Point:
        cls = type(self)
        try:
            new = cls(*tuple(-component for component in self.coords))
            return new 
        except TypeError:
            raise PointImplementationError
    
    def __getitem__(self, key: int | slice):
        if isinstance(key, int):
            return self.coords[key]
        elif isinstance(key, slice):
            return self.coords[key.start:key.stop:key.step]
        else:
            raise TypeError(f"Point indices can only be int or slice, got {type(key)} instead.")
    
    def __iter__(self):
        return iter(self.coords)

    def __str__(self) -> str:
        classname = type(self).__name__ 
        return f'{classname}{self.coords}'
    
    def setx(self, val):
        """
        There is opportunity for bad values here, but we cannot catch them in the parent class.
        Point subclasses that contain coordinates of external types (Decimal for example), or types that dont exist yet
        can't be tested here. I prefer to allow that functionality without overriding, at the cost of allowing bad values.
        """

        self.x = val 
        
        coords = list(self.coords)
        coords[0] = val 

        self.coords = tuple(coords)
    
    def sety(self, val):
        """
        There is opportunity for bad values here, but we cannot catch them in the parent class.
        Point subclasses that contain coordinates of external types (Decimal for example), or types that dont exist yet
        can't be tested here. I prefer to allow that functionality without overriding, at the cost of allowing bad values.
        """

        self.y = val 
        
        coords = list(self.coords)
        coords[1] = val 

        self.coords = tuple(coords)
    
    def setcoord(self, dim: int, val: int | float):
        """
        There is opportunity for bad values here, but we cannot catch them in the parent class.
        Point subclasses that contain coordinates of external types (Decimal for example), or types that dont exist yet
        can't be tested here. I prefer to allow that functionality without overriding, at the cost of allowing bad values.
        """

        coords = list(self.coords)
        coords[dim] = val 

        self.coords = coords

    def rotate(self, about: Point, angle: int | float, plane: Plane) -> Point:
        """
        Performs an in-place rotation and returns self afterwards.
        """

        if not isinstance(about, Point):
            raise TypeError(f"Expected Point, got {type(about)} instead.")
        elif not isinstance(angle, (int, float)):
            raise TypeError(f"Expected int or float, got {type(angle)} instead.")
        elif not isinstance(plane, Plane):
            raise TypeError(f"Expected Plane, got {type(plane)} instead.")
        
        projection_self = plane.projection(self)
        projection_axis = plane.projection(about)
        projected_distance = projection_self.dist(projection_axis)

        dy, dx = projection_axis.coords[1] - projection_self.coords[1], projection_axis.coords[0] - projection_self.coords[0]
        current_angle = math.atan2(dy, dx)
        target_angle = current_angle + angle

        coordinate1 = projection_axis.coords[0] + projected_distance * math.cos(target_angle)
        coordinate2 = projection_axis.coords[1] + projected_distance * math.sin(target_angle)

        dim1, dim2 = plane.basis

        self.setcoord(dim1, coordinate1)
        self.setcoord(dim2, coordinate2)

        return self

class Plane:
    """
    A type intended to be used as a mask to isolate the coordinates of a point on the given plane.
    Functionality is bare minimum. To implement more complex planes, subclass this type.

    Critically, Plane implements the "projection" operation. By default, also implemented with & operator, but
    can be changed in a subclass. The projection of a Point p on the xz plane for example, is a Point2D(p.x, p.z).

    The "basis" of a plane is a two-element tuple representing which dimensions the plane sits on.
    (0, 1) is the xy plane.
    (0, 2) is the xz plane.
    (1, 2) is the yz plane.

    Larger values in the basis vector is fine but cannot be expected to work unless higher dimensional Point
    classes are also implemented.
    """

    def __init__(self, basis: tuple[int | float]):
        self.basis = basis

        if len(basis) != 2:
            raise ValueError(f"Plane must have exactly 2 dimensions, got {len(basis)} instead")
    
    def projection(self, other: Point) -> Point:
        """
        This will always return a 2-dimensional point, but returns a Point over a Point2D.
        This is because the parent class Point implements rotate, which uses a Plane, and should not depend on its
        own child.

        Additionally, the point returned is abstract, it does not refer to the original space it sits in and should be
        embedded in the original or intended dimension before use.
        """

        if not isinstance(other, Point): raise NotImplemented

        dim1, dim2 = self.basis

        return Point(other.coords[dim1], other.coords[dim2])



class Point2D(Point):
    def __init__(self, x: int | float, y: int | float) -> Point2D:
        super().__init__(x, y)
        self.x = x
        self.y = y

    def direction(self, other: Point2D):
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
    
    def rotate(self, about: Point2D, angle: int | float) -> Point2D:
        if not isinstance(about, Point2D):
            raise TypeError(f"Expected Point2D, got {type(about)} instead.")
        elif not isinstance(angle, (int, float)):
            raise TypeError(f"Expected int or float, got {type(angle)} instead.")

        dx, dy = (self - about).coords 
        r = self.dist(about)
        target_angle = math.atan2(dy, dx) + angle 


        return about + r * Point2D(math.cos(target_angle), math.sin(target_angle))

    def to_3D(self) -> Point3D:
        return Point3D(self.x, self.y, 0)
    
class Point3D(Point):
    def __init__(self, x: int | float, y: int | float, z: int | float):
        super().__init__(x, y, z)
        self.x = x
        self.y = y 
        self.z = z

    def __update_coords(self):
        self.x = self.coords[0]
        self.y = self.coords[1]
        self.z = self.coords[2]

    def setcoord(self, dim: int, val: int | float):
        coords = list(self.coords)
        coords[dim] = val 

        self.coords = coords
        self.__update_coords()

    def setz(self, val):
        self.z = val 
        
        coords = list(self.coords)
        coords[2] = val 

        self.coords = tuple(coords)

    def to_2D(self: Point3D) -> Point2D:
        flattened = Point2D(self.x, self.y)

        viewport_width, viewport_height = VIEWPORT_RESOLUTION
        center_x, center_y = viewport_width/2, viewport_height/2
        vanishing_point = Point2D(center_x, center_y)

        dx = vanishing_point.x - flattened.x
        dy = vanishing_point.y - flattened.y 

        if dx != 0:
            sign = dx / abs(dx)
        elif dy != 0:
            sign = -(dy / abs(dy))
        else:
            sign = 0

        return flattened + depth_attenuation(self.z) * flattened.dist(vanishing_point) * (flattened.direction(vanishing_point) * sign)
    
    def __str__(self) -> str: 
        return f'Point3D{self.coords}'

    def __repr__(self) -> str:
        return str(self)