from src.utils.math_utils import equal
import src.tuples as tuples

def test_point():
    """A tuple with w=1.0 is a point."""
    p = tuples.point(1, 2, 3)
    assert equal(p.x, 1)
    assert equal(p.y, 2)
    assert equal(p.z, 3)
    assert equal(p.w, 1.0)
    assert p.is_point
    assert not p.is_vector

def test_vector():
    """A tuple with w=0.0 is a vector."""
    v = tuples.vector(4, 5, 6)
    assert equal(v.x, 4)
    assert equal(v.y, 5)
    assert equal(v.z, 6)
    assert equal(v.w, 0.0)
    assert v.is_vector
    assert not v.is_point

def test_tuple_equality():
    """Tuples with the same values should be equal."""
    t1 = tuples.point(1, 2, 3)
    t2 = tuples.point(1, 2, 3)
    t3 = tuples.vector(1, 2, 3)
    t4 = tuples.vector(4, 5, 6)

    assert t1 == t2
    assert not t1 == t3
    assert not t3 == t4