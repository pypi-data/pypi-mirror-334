import math

def coulomb_force(q1: float, q2: float, r: float, k: float = 8.9875517873681764e9) -> float:
    """
    Calculates the electrostatic force using Coulomb's law: F = k * q1 * q2 / r².

    Args:
        q1 (float): Charge 1 (Coulombs).
        q2 (float): Charge 2 (Coulombs).
        r (float): Distance between charges (m).
        k (float, optional): Coulomb's constant (N·m²/C²). Default is 8.99 × 10⁹ N·m²/C².

    Returns:
        float: Electrostatic force (N).
    
    Raises:
        ValueError: If distance is non-positive.
    """
    if r <= 0:
        raise ValueError("Distance must be positive.")
    return k * q1 * q2 / r**2

def electric_field(force: float, charge: float) -> float:
    """
    Calculates the electric field strength using E = F/q.

    Args:
        force (float): Electrostatic force (N).
        charge (float): Charge (Coulombs).

    Returns:
        float: Electric field strength (N/C).
    
    Raises:
        ValueError: If charge is zero.
    """
    if charge == 0:
        raise ValueError("Charge must be nonzero.")
    return force / charge

def electric_field_spherical(q: float, r: float, k: float = 8.9875517873681764e9) -> float:
    """
    Calculates the electric field outside a spherically symmetric charge distribution: E = kQ/r².

    Args:
        q (float): Charge (Coulombs).
        r (float): Distance from charge (m).
        k (float, optional): Coulomb's constant (N·m²/C²). Default is 8.99 × 10⁹ N·m²/C².

    Returns:
        float: Electric field strength (N/C).
    
    Raises:
        ValueError: If distance is non-positive.
    """
    if r <= 0:
        raise ValueError("Distance must be positive.")
    return k * q / r**2

def electric_potential_energy(q1: float, q2: float, r: float, k: float = 8.9875517873681764e9) -> float:
    """
    Calculates the electric potential energy of a charge system: U = k*q1*q2 / r.

    Args:
        q1 (float): Charge 1 (Coulombs).
        q2 (float): Charge 2 (Coulombs).
        r (float): Distance between charges (m).
        k (float, optional): Coulomb's constant (N·m²/C²). Default is 8.99 × 10⁹ N·m²/C².

    Returns:
        float: Electric potential energy (J).
    
    Raises:
        ValueError: If distance is non-positive.
    """
    if r <= 0:
        raise ValueError("Distance must be positive.")
    return k * q1 * q2 / r

def electric_potential(voltage_a: float, voltage_b: float) -> float:
    """
    Calculates the potential difference between two points: U_AB = V_B - V_A.

    Args:
        voltage_a (float): Electric potential at point A (V).
        voltage_b (float): Electric potential at point B (V).

    Returns:
        float: Electric potential difference (V).
    """
    return voltage_b - voltage_a

def voltage_uniform_field(electric_field: float, distance: float) -> float:
    """
    Calculates the voltage in a uniform electric field: U = E * d.

    Args:
        electric_field (float): Electric field strength (N/C or V/m).
        distance (float): Distance in the field (m).

    Returns:
        float: Voltage (V).
    
    Raises:
        ValueError: If distance is non-positive.
    """
    if distance <= 0:
        raise ValueError("Distance must be positive.")
    return electric_field * distance

import math

def electric_field_parallel_plates(charge: float, area: float, epsilon_0: float = 8.854e-12) -> float:
    """
    Calculates the electric field between parallel plates: E = σ / ε₀, where σ = Q / ΔS.

    Args:
        charge (float): Charge on the plates (C).
        area (float): Surface area of the plates (m²).
        epsilon_0 (float, optional): Permittivity of free space (F/m). Default is 8.854 × 10⁻¹² F/m.

    Returns:
        float: Electric field strength (N/C or V/m).
    
    Raises:
        ValueError: If charge or area is non-positive.
    """
    if charge <= 0 or area <= 0:
        raise ValueError("Charge and area must be positive.")
    sigma = charge / area
    return sigma / epsilon_0

def electric_field_dielectric(e_external: float, relative_permittivity: float) -> float:
    """
    Calculates the electric field inside a dielectric: E = E₀ / εᵣ.

    Args:
        e_external (float): External electric field (N/C or V/m).
        relative_permittivity (float): Relative permittivity of the dielectric.

    Returns:
        float: Electric field inside the dielectric (N/C or V/m).
    
    Raises:
        ValueError: If relative permittivity is non-positive.
    """
    if relative_permittivity <= 0:
        raise ValueError("Relative permittivity must be positive.")
    return e_external / relative_permittivity

def capacitance(q: float, voltage: float) -> float:
    """
    Calculates the capacitance of a capacitor: C = Q / U.

    Args:
        q (float): Charge stored in the capacitor (C).
        voltage (float): Voltage across the capacitor (V).

    Returns:
        float: Capacitance (F).
    
    Raises:
        ValueError: If voltage is zero or negative.
    """
    if voltage <= 0:
        raise ValueError("Voltage must be positive.")
    return q / voltage

def capacitance_parallel_plate(relative_permittivity: float, epsilon_0: float, area: float, distance: float) -> float:
    """
    Calculates the capacitance of a parallel plate capacitor with a dielectric: C = εᵣ * ε₀ * S / d.

    Args:
        relative_permittivity (float): Relative permittivity of the dielectric.
        epsilon_0 (float): Permittivity of free space (F/m).
        area (float): Surface area of the plates (m²).
        distance (float): Separation between plates (m).

    Returns:
        float: Capacitance (F).
    
    Raises:
        ValueError: If any input is non-positive.
    """
    if relative_permittivity <= 0 or epsilon_0 <= 0 or area <= 0 or distance <= 0:
        raise ValueError("All parameters must be positive.")
    return (relative_permittivity * epsilon_0 * area) / distance

def capacitor_energy(q: float, capacitance: float) -> float:
    """
    Calculates the stored energy in a capacitor: W = Q² / (2C).

    Args:
        q (float): Charge stored in the capacitor (C).
        capacitance (float): Capacitance of the capacitor (F).

    Returns:
        float: Energy stored (J).
    
    Raises:
        ValueError: If capacitance is zero or negative.
    """
    if capacitance <= 0:
        raise ValueError("Capacitance must be positive.")
    return (q**2) / (2 * capacitance)

def capacitor_energy_voltage(voltage: float, capacitance: float) -> float:
    """
    Calculates the stored energy in a capacitor using voltage: W = 1/2 * U² * C.

    Args:
        voltage (float): Voltage across the capacitor (V).
        capacitance (float): Capacitance of the capacitor (F).

    Returns:
        float: Energy stored (J).
    
    Raises:
        ValueError: If capacitance is zero or negative.
    """
    if capacitance <= 0:
        raise ValueError("Capacitance must be positive.")
    return 0.5 * capacitance * voltage**2