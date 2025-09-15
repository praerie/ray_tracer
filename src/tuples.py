from __future__ import annotations
from src.utils.math_utils import equal
from dataclasses import dataclass
import math


@dataclass(frozen=True)
class Tuple:
    """A 4D tuple used to represent points, vectors, and colors in 3D space.

    The w component determines whether the tuple is a point (w=1.0)
    or a vector (w=0.0). Other values of w generally do not
    correspond to meaningful geometry.
    """
    x: float
    y: float
    z: float
    w: float

    # --- properties ---

    @property
    def is_point(self) -> bool:
        """Return True if this tuple represents a point (w ≈ 1.0)."""
        return equal(self.w, 1.0)
    
    @property
    def is_vector(self) -> bool:
        """Return True if this tuple represents a vector (w ≈ 0.0)."""
        return equal(self.w, 0.0)
    
    @property
    def is_unit_vector(self) -> bool:
        """Returns True if this tuple is a unit vector, i.e. has a magnitude of 1. 
        
        Note: Vectors with magnitudes of 1 are called unit vectors,
        which are useful in computing view matrix, determining the direction perpendicular 
        to a surface, and when generating rays to cast into scene."""
        return self.is_vector and equal(self.magnitude(), 1.0)
    
    @property
    def is_color(self) -> bool:
        # treat anything created via color() as a color
        return self.w == 0.0 and hasattr(self, "red")
    
    # --- color channel aliases ---
    
    @property
    def red(self) -> float: return self.x

    @property
    def green(self) -> float: return self.y

    @property
    def blue(self) -> float: return self.z
        
    # --- factories --- 

    @staticmethod
    def point(x: float, y: float, z: float) -> "Tuple":
        """Create a point at (x, y, z) in 3D space.
        A point has w = 1.0, distinguishing it from a vector or color."""
        return Tuple(x, y, z, 1.0)

    @staticmethod
    def vector(x: float, y: float, z: float) -> "Tuple":
        """Create a vector with components (x, y, z).
        A vector has w = 0.0, representing direction and magnitude
        but no fixed position."""
        return Tuple(x, y, z, 0.0)

    @staticmethod
    def color(red: float, green: float, blue: float) -> "Tuple":
        """Create a color using normalized floats (0-1).
        Values may be outside [0,1] during calculations."""
        return Tuple(red, green, blue, 0.0)

    # --- arithmetic ---
        
    def __add__(self, other: Tuple) -> Tuple:
        """Add two tuples component-wise.

        - Point + Vector -> Point
        - Vector + Vector -> Vector
        - Point + Point -> invalid (w=2), neither point nor vector
        """
        if not isinstance(other, Tuple):
            raise NotImplemented
        return Tuple(
            self.x + other.x,
            self.y + other.y,
            self.z + other.z,
            self.w + other.w
        )
    
    def __sub__(self, other: Tuple) -> Tuple:
        """Subtract two tuples component-wise.

        - Point - Point -> Vector (direction from other to self)
        - Point - Vector -> Point
        - Vector - Vector -> Vector
        - Vector - Point -> invalid (w=-1), neither point nor vector
        """
        if not isinstance(other, Tuple):
            raise NotImplemented
        return Tuple(
            self.x - other.x,
            self.y - other.y,
            self.z - other.z,
            self.w - other.w,
        )
    
    def __eq__(self, other: Tuple) -> bool:
        """Compare tuples with EPSILON tolerance.

        Returns True if all components are equal within a small margin
        of error. This avoids issues with floating-point precision.
        """
        if not isinstance(other, Tuple):
            raise NotImplemented
        return (equal(self.x, other.x)
                and equal(self.y, other.y)
                and equal(self.z, other.z)
                and equal(self.w, other.w))
    
    def __neg__(self) -> Tuple:
        """Return a new Tuple with all components negated."""
        return Tuple(
            -self.x,
            -self.y,
            -self.z,
            -self.w
        )
    
    def __mul__(self, scalar: float) -> Tuple:
        """Multiply all components of the tuple by a scalar."""
        return Tuple(
            self.x * scalar,
            self.y * scalar,
            self.z * scalar,
            self.w * scalar
        )

    def __truediv__(self, scalar: float) -> Tuple:
        """Divide all components of the tuple by a scalar."""
        return Tuple(
            self.x / scalar,
            self.y / scalar, 
            self.z / scalar,
            self.w / scalar
        )
    
    # --- vector operations ---

    def magnitude(self) -> float:
        """Return the magnitude (length) of the vector."""
        return math.sqrt(
            self.x**2 + self.y**2 + self.z**2 + self.w**2
        )
    
    def normalize(self) -> "Tuple":
        """Return a unit vector in the same direction as this vector.
        Normalization is achieved by dividing each component by its magnitude."""
        if not self.is_vector:
            raise ValueError("Normalize is only defined for vectors.")
        mag = self.magnitude()
        if equal(mag, 0.0):
            raise ValueError("A zero vector cannot be normalized.")
        return Tuple(self.x/mag, self.y/mag, self.z/mag, 0.0)

    def dot(self, other: Tuple) -> float:
        """Return dot product, AKA scalar product or inner product, of two tuples.
        
        Notes:
            - The dot product of two unit vectors is the cosine of the angle between them.
            - Geometrically, encodes angles and alignment between two directions
            - Defined on direction (not position), so w is unneeded; a point is in invalid parameter.
            - The smaller the dot product, the larger the angle between the vectors.
            - Useful for rays intersecting with objects and when computing shading on a surface.
            - Applies to vectors of any dimension, not just 3. 

        Examples:
            - Dot product of perpendicular unit vectors = 0
            - Dot product of parallel (identical) unit vectors = 1 
            - Dot product of opposite unit vectors = -1
        """
        if not isinstance(other, Tuple):
            raise NotImplemented
        if not self.is_vector:
            raise ValueError("Dot product cannot be performed on points.")
        return (
                self.x * other.x +
                self.y * other.y +
                self.z * other.z +
                self.w * other.w
            )
        
    def cross(self, other: Tuple) -> Tuple:
        """Return the cross product of two vectors.

        Notes:
            - Cross product of two vectors: a vector that is perpendicular 
            to both a and b, and thus normal to the plane containing them.
            - Order is important: x cross y = z, but y cross x = -z.
            - Relevant for viewing transformations and rendering triangles.
            - Magnitude of the cross-product = area of the parallelogram 
            spanned by original two vectors.
        """
        if not isinstance(other, Tuple):
            raise NotImplemented
        if not (self.is_vector and other.is_vector):
            raise ValueError("Cross product is only defined for vectors.")
        else:
            return Tuple(
                self.y * other.z - self.z * other.y,
                self.z * other.x - self.x * other.z,
                self.x * other.y - self.y * other.x,
                0.0
            )


# helper functions 

def to_rgb(c: Tuple) -> tuple[int, int, int]:
    """Clamp and convert a Tuple color to 0-255 RGB integers."""
    return (
        int(max(0, min(255, round(c.x * 255)))),
        int(max(0, min(255, round(c.y * 255)))),
        int(max(0, min(255, round(c.z * 255))))
    )



