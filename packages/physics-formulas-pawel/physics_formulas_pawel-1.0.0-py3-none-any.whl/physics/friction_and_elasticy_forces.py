import math

def kinetic_friction(mu_k: float, normal_force: float) -> float:
    """
    Calculates kinetic friction force.

    Args:
        mu_k (float): Coefficient of kinetic friction.
        normal_force (float): Normal force (N).

    Returns:
        float: Kinetic friction force (N).
    """
    return mu_k * normal_force

def static_friction(mu_s: float, normal_force: float) -> float:
    """
    Calculates maximum static friction force.

    Args:
        mu_s (float): Coefficient of static friction.
        normal_force (float): Normal force (N).

    Returns:
        float: Maximum static friction force (N).
    """
    return mu_s * normal_force

def elastic_force(k: float, x: float) -> float:
    """
    Calculates the elastic force based on Hooke's Law.

    Args:
        k (float): Spring constant (N/m).
        x (float): Displacement from equilibrium (m).

    Returns:
        float: Elastic force (N).
    """
    return -k * x

def elastic_potential_energy(k: float, x: float) -> float:
    """
    Calculates the potential energy stored in a spring.

    Args:
        k (float): Spring constant (N/m).
        x (float): Displacement from equilibrium (m).

    Returns:
        float: Elastic potential energy (J).
    """
    return 0.5 * k * x**2
