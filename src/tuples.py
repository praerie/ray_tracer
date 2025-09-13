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
    
def point(x, y, z) -> Tuple:
    return Tuple(x, y, z, 1.0)

def vector(x, y, z) -> Tuple:
    return Tuple(x, y, z, 0.0)

def tuple_equal(t1, t2) -> bool:
    return(equal(t1.x, t2.x),
           equal(t1.y, t2.y),
           equal(t1.z, t2.z),
           equal(t1.w, t2.w))



