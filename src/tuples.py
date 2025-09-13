from __future__ import annotations
from src.utils.math_utils import equal
from dataclasses import dataclass

@dataclass(frozen=True)
class Tuple:
    x: float
    y: float
    z: float
    w: float

    @property
    def is_point(self) -> bool:
        return equal(self.w, 1.0)
    
    @property
    def is_vector(self) -> bool:
        return equal(self.w, 0.0)
    
    def __add__(self, other: Tuple) -> Tuple:
        """Add two tuples together by summing corresponding elements."""
        if not isinstance(other, Tuple):
            return NotImplemented
        return Tuple(
            self.x + other.x,
            self.y + other.y,
            self.z + other.z,
            self.w + other.w
        )
    
    def __sub__(self, other: Tuple) -> Tuple:
        if not isinstance(other, Tuple):
            return NotImplemented
        return Tuple(
            self.x - other.x,
            self.y - other.y,
            self.z - other.z,
            self.w - other.w,
        )
    
    # equality with EPSILON tolerance
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Tuple):
            return NotImplemented
        return (equal(self.x, other.x)
                and equal(self.y, other.y)
                and equal(self.z, other.z)
                and equal(self.w, other.w))
    
def point(x, y, z) -> Tuple:
    return Tuple(x, y, z, 1.0)

def vector(x, y, z) -> Tuple:
    return Tuple(x, y, z, 0.0)



