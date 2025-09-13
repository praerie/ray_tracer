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

def test_add_two_tuples():
    """Addition rules:
    - Point (w=1) + Vector (w=0) → Point (w=1)
    - Vector (w=0) + Vector (w=0) → Vector (w=0)
    - Point (w=1) + Point (w=1) → invalid (w=2), neither point nor vector
    """
    p = tuples.point(-7, 8, 9)
    v = tuples.vector(4, -5, -6)

    expected = tuples.point(-3, 3, 3)
    
    assert p + v == expected
    assert expected.is_point
    assert tuples.equal(expected.w, 1.0)

def test_subtract_two_points():
    """Subtracting two points (w=1 - w=1) yields a vector (w=0),
    representing the direction from the second point to the first.
    """
    p1 = tuples.point(-7, 8, 9)
    p2 = tuples.point(4, -5, -6)

    expected = tuples.vector(-11, 13, 15)

    assert p1 - p2 == expected
    assert expected.is_vector
    assert tuples.equal(expected.w, 0.0)

def test_subtract_two_vectors():
    """Subtracting two vectors (w=0 - w=0) yields another vector (w=0),
    representing the change in direction between them.
    """
    v1 = tuples.vector(1, 2, 3)
    v2 = tuples.vector(7, 8, 9)

    expected = tuples.vector(-6, -6, -6)

    assert v1 - v2 == expected
    assert expected.is_vector
    assert tuples.equal(expected.w, 0.0)

def test_subtract_vector_from_point():
    """Subtracting a vector (w=0) from a point (w=1) yields another point (w=1),
    conceptually moving the point backward by the given vector.
    """
    p = tuples.point(4, 5, 6)
    v = tuples.vector(1, 2, 3)

    expected = tuples.point(3, 3, 3)

    assert p - v == expected
    assert expected.is_point
    assert tuples.equal(expected.w, 1.0)

def test_negate_tuple():
    """Each component of the tuple should be negated, including w."""
    p = tuples.point(1, 2, 3)  # w=1.0
    v = tuples.vector(4, 5, 6) # w=0.0

    negated_p = tuples.Tuple(-1, -2, -3, -1) 
    negated_v = tuples.Tuple(-4, -5, -6, 0) 

    assert -p == negated_p
    assert -v == negated_v

def test_multiply_tuple_by_scalar():
    """Multiplying a tuple by a scalar scales each component."""
    p = tuples.point(1, 2, 9)
    scalar = 3.27 

    expected = tuples.Tuple(3.27, 6.54, 29.43, 3.27)

    assert p * scalar == expected

def test_multiply_tuple_by_fraction():
    """Multiplying a tuple by a fraction scales each component."""
    p = tuples.point(1, 2, 9)
    fraction = 0.7

    expected = tuples.Tuple(0.7, 1.4, 6.3, 0.7)

    assert p * fraction == expected

def test_divide_tuple_by_fraction():
    """Dividing a tuple by a fraction scales each component by its reciprocal."""
    p = tuples.point(8, -6, 4) 
    scalar = 2

    expected = tuples.Tuple(4, -3, 2, 0.5)

    assert p / scalar == expected

# The magnitude (length) of a vector is the square root of the sum of squares.

def test_magnitude_of_unit_x():
    v = tuples.vector(1, 0, 0)
    assert tuples.equal(v.magnitude(), 1.0)
    assert v.is_unit_vector

def test_magnitude_of_unit_y():
    v = tuples.vector(0, 1, 0)
    assert tuples.equal(v.magnitude(), 1.0)
    assert v.is_unit_vector

def test_magnitude_of_unit_z():
    v = tuples.vector(0, 0, 1)
    assert tuples.equal(v.magnitude(), 1.0)
    assert v.is_unit_vector

def test_magnitude_of_negative_vector():
    v = tuples.vector(-1, -2, -3)
    expected = 14 ** 0.5
    assert tuples.equal(v.magnitude(), expected)

def test_normalize_to_unit_vector():
    """Normalized vectors have magnitudes of 1."""
    v = tuples.vector(3, 6, 9)
    unit = v.normalize()

    assert unit.is_unit_vector

    mag = v.magnitude()
    expected = tuples.Tuple(3/mag, 6/mag, 9/mag, 0)

    assert unit == expected

def test_dot_product():
    """The dot product of two vectors equals the cosine of the angle between them.

    Examples:
    - Dot product of perpendicular unit vectors = 0
    - Dot product of parallel unit vectors = 1
    - Dot product of opposite unit vectors = -1
    """
    v1 = tuples.vector(1, 0, 0)  # unit x
    v2 = tuples.vector(0, 1, 0)  # unit y
    v3 = tuples.vector(1, 0, 0)  # same as v1
    v4 = tuples.vector(-1, 0, 0) # opposite direction

    assert tuples.equal(v1.dot_product(v2), 0.0)   # perpendicular
    assert tuples.equal(v1.dot_product(v3), 1.0)   # parallel
    assert tuples.equal(v1.dot_product(v4), -1.0)  # opposite
