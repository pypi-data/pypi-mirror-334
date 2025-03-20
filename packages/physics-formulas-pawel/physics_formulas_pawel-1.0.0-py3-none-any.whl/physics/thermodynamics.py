import math

def first_law_thermodynamics(heat: float, work: float) -> float:
    """
    Applies the first law of thermodynamics: ΔU = Q + W.

    Args:
        heat (float): Heat energy added to the system (J).
        work (float): Work done on the system (J).

    Returns:
        float: Change in internal energy (J).
    """
    return heat + work

def work_done(pressure: float, delta_volume: float) -> float:
    """
    Calculates the work done by a gas under constant pressure.

    Args:
        pressure (float): Pressure of the gas (Pa).
        delta_volume (float): Change in volume (m³).

    Returns:
        float: Work done (J).
    
    Raises:
        ValueError: If pressure or volume change is non-positive.
    """
    if pressure <= 0 or delta_volume <= 0:
        raise ValueError("Pressure and volume change must be positive.")
    return pressure * delta_volume

def specific_heat(Q: float, mass: float, delta_T: float) -> float:
    """
    Calculates the specific heat capacity.

    Args:
        Q (float): Heat energy (J).
        mass (float): Mass of the substance (kg).
        delta_T (float): Change in temperature (K).

    Returns:
        float: Specific heat capacity (J/kg·K).
    
    Raises:
        ValueError: If mass or temperature change is non-positive.
    """
    if mass <= 0 or delta_T <= 0:
        raise ValueError("Mass and temperature change must be positive.")
    return Q / (mass * delta_T)

def molar_heat(Q: float, n_moles: float, delta_T: float) -> float:
    """
    Calculates the molar heat capacity.

    Args:
        Q (float): Heat energy (J).
        n_moles (float): Number of moles.
        delta_T (float): Change in temperature (K).

    Returns:
        float: Molar heat capacity (J/mol·K).
    
    Raises:
        ValueError: If number of moles or temperature change is non-positive.
    """
    if n_moles <= 0 or delta_T <= 0:
        raise ValueError("Number of moles and temperature change must be positive.")
    return Q / (n_moles * delta_T)

def phase_change_heat(Q: float, mass: float) -> float:
    """
    Calculates the heat energy required for a phase change.

    Args:
        Q (float): Heat energy (J).
        mass (float): Mass of the substance (kg).

    Returns:
        float: Latent heat (J/kg).
    
    Raises:
        ValueError: If mass is non-positive.
    """
    if mass <= 0:
        raise ValueError("Mass must be positive.")
    return Q / mass

def ideal_gas_law(n_moles: float, temperature: float, volume: float) -> float:
    """
    Calculates pressure using the ideal gas law: pV = nRT.

    Args:
        n_moles (float): Number of moles.
        temperature (float): Temperature in Kelvin (K).
        volume (float): Volume of gas (m³).

    Returns:
        float: Pressure (Pa).
    
    Raises:
        ValueError: If any input is non-positive.
    """
    R = 8.314  # Universal gas constant (J/mol·K)
    if n_moles <= 0 or temperature <= 0 or volume <= 0:
        raise ValueError("Number of moles, temperature, and volume must be positive.")
    return (n_moles * R * temperature) / volume

def efficiency(heat_in: float, heat_out: float) -> float:
    """
    Calculates the efficiency of a heat engine.

    Args:
        heat_in (float): Heat energy absorbed (J).
        heat_out (float): Heat energy rejected (J).

    Returns:
        float: Efficiency (decimal form, e.g., 0.4 for 40%).
    
    Raises:
        ValueError: If heat input is non-positive.
    """
    if heat_in <= 0:
        raise ValueError("Heat input must be positive.")
    return (heat_in - heat_out) / heat_in
