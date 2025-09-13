from __future__ import annotations
from src.utils.math_utils import equal
from dataclasses import dataclass
import math


@dataclass(frozen=True)
class Tuple:
    """A 4D tuple used to represent points and vectors in 3D space.

    The w component determines whether the tuple is a point (w=1.0)
    or a vector (w=0.0). Other values of w generally do not
    correspond to meaningful geometry.
    """
    x: float
    y: float
    z: float
    w: float

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
    
    def __add__(self, other: Tuple) -> Tuple:
        """Add two tuples component-wise.

        - Point + Vector -> Point
        - Vector + Vector -> Vector
        - Point + Point -> invalid (w=2), neither point nor vector
        """
        if not isinstance(other, Tuple):
            return NotImplemented
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
            return NotImplemented
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
            return NotImplemented
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
    
    def magnitude(self) -> float:
        """Return the magnitude (length) of the vector."""
        return math.sqrt(
            self.x**2 + self.y**2 + self.z**2 + self.w**2
        )

    def normalize(self) -> Tuple:
        """Return a unit vector in the same direction as this vector.
        Normalization is achieved by dividing each component by its magnitude."""
        mag = self.magnitude()
        return Tuple(
            self.x / mag,
            self.y / mag,
            self.z / mag,
            self.w / mag
        )

    
def point(x, y, z) -> Tuple:
    """Create a point at coordinates (x, y, z)."""
    return Tuple(x, y, z, 1.0)

def vector(x, y, z) -> Tuple:
    """Create a vector at coordinates (x, y, z)."""
    return Tuple(x, y, z, 0.0)



