EPSILON = 1e-6  # tiny tolerance for float comparisons

def equal(a: float, b: float, eps: float = EPSILON) -> bool:
    """Return True if a and b are within eps of each other."""
    return abs(a - b) < eps
