import math

def critical_angle(n1: float, n2: float) -> float:
    """
    Calculates the critical angle for light passing from medium 2 to medium 1.

    Args:
        n1 (float): Refractive index of medium 1.
        n2 (float): Refractive index of medium 2.

    Returns:
        float: Critical angle in degrees.
    
    Raises:
        ValueError: If n1 > n2 (total internal reflection condition) or if indices are non-positive.
    """
    if n1 <= 0 or n2 <= 0:
        raise ValueError("Refractive indices must be positive.")
    if n1 > n2:
        raise ValueError("Total internal reflection occurs; no critical angle.")
    return math.degrees(math.asin(n1 / n2))

def brewster_angle(n1: float, n2: float) -> float:
    """
    Calculates Brewster's angle for polarization at reflection.

    Args:
        n1 (float): Refractive index of medium where light originates.
        n2 (float): Refractive index of medium where light is transmitted.

    Returns:
        float: Brewster's angle in degrees.
    
    Raises:
        ValueError: If indices are non-positive.
    """
    if n1 <= 0 or n2 <= 0:
        raise ValueError("Refractive indices must be positive.")
    return math.degrees(math.atan(n2 / n1))

def lens_equation(x: float, y: float) -> float:
    """
    Calculates the focal length using the lens equation.

    Args:
        x (float): Object distance (m).
        y (float): Image distance (m).

    Returns:
        float: Focal length (m).
    
    Raises:
        ValueError: If distances are zero or negative.
    """
    if x <= 0 or y <= 0:
        raise ValueError("Object and image distances must be positive.")
    return 1 / ((1 / x) + (1 / y))

def lens_focal_length(n_lens: float, n_medium: float, R1: float, R2: float) -> float:
    """
    Calculates the focal length of a lens using the lens maker's formula.

    Args:
        n_lens (float): Refractive index of the lens material.
        n_medium (float): Refractive index of the surrounding medium.
        R1 (float): Radius of curvature of the first surface (m).
        R2 (float): Radius of curvature of the second surface (m).

    Returns:
        float: Focal length (m).
    
    Raises:
        ValueError: If refractive indices or radii are non-positive.
    """
    if n_lens <= 0 or n_medium <= 0:
        raise ValueError("Refractive indices must be positive.")
    if R1 == 0 or R2 == 0:
        raise ValueError("Radii of curvature cannot be zero.")
    return 1 / ((n_lens / n_medium - 1) * (1 / R1 + 1 / R2))