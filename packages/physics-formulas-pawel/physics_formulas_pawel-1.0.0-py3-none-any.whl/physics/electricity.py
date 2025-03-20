import math

def current_intensity(Q, delta_t):
    """
    Calculates the electric current intensity.
    :param Q: Charge (Coulombs)
    :param delta_t: Time interval (seconds)
    :return: Current (Amperes)
    """
    return Q / delta_t

def electrical_resistance(U, I):
    """
    Calculates the resistance of a conductor.
    :param U: Voltage (Volts)
    :param I: Current (Amperes)
    :return: Resistance (Ohms)
    """
    return U / I

def wire_resistance(rho, l, S):
    """
    Calculates the resistance of a wire.
    :param rho: Resistivity (Ohm meter)
    :param l: Length of the wire (meters)
    :param S: Cross-sectional area (square meters)
    :return: Resistance (Ohms)
    """
    return rho * l / S

def power_dissipated(U, I, R):
    """
    Calculates power dissipated in a resistor.
    :param U: Voltage (Volts)
    :param I: Current (Amperes)
    :param R: Resistance (Ohms)
    :return: Power (Watts)
    """
    return (U * I, I**2 * R, U**2 / R)

def resistance_temperature(R0, alpha, delta_T):
    """
    Calculates the resistance of a material at a different temperature.
    :param R0: Initial resistance (Ohms)
    :param alpha: Temperature coefficient of resistance (1/K)
    :param delta_T: Change in temperature (Kelvin)
    :return: Resistance at new temperature (Ohms)
    """
    return R0 * (1 + alpha * delta_T)

def kirchhoff_voltage_law(emfs, voltages):
    """
    Applies Kirchhoff's Voltage Law.
    :param emfs: List of electromotive forces (Volts)
    :param voltages: List of voltage drops (Volts)
    :return: Sum of EMFs and voltage drops should be zero
    """
    return sum(emfs) - sum(voltages)

def lorentz_force(q, v, B, alpha):
    """
    Calculates the Lorentz force.
    :param q: Charge (Coulombs)
    :param v: Velocity (m/s)
    :param B: Magnetic field (Tesla)
    :param alpha: Angle between velocity and magnetic field (degrees)
    :return: Force (Newtons)
    """
    return q * v * B * math.sin(math.radians(alpha))

def magnetic_field_straight_wire(I, r, mu_0=4 * math.pi * 1e-7):
    """
    Calculates the magnetic field around a long straight current-carrying wire.
    :param I: Current (Amperes)
    :param r: Distance from the wire (meters)
    :param mu_0: Permeability of free space (default 4π × 10⁻⁷ Tm/A)
    :return: Magnetic field strength (Tesla)
    """
    return mu_0 * I / (2 * math.pi * r)

def magnetic_flux(B, S, alpha):
    """
    Calculates the magnetic flux through a surface.
    :param B: Magnetic field strength (Tesla)
    :param S: Surface area (square meters)
    :param alpha: Angle between the field and the normal to the surface (degrees)
    :return: Magnetic flux (Weber)
    """
    return B * S * math.cos(math.radians(alpha))

def induced_emf(delta_flux, delta_t):
    """
    Calculates the induced electromotive force (Faraday's Law).
    :param delta_flux: Change in magnetic flux (Weber)
    :param delta_t: Change in time (seconds)
    :return: Induced EMF (Volts)
    """
    return -delta_flux / delta_t

def transformer_voltage_current(U1, U2, N1, N2, I1, I2):
    """
    Calculates transformer voltage and current relations.
    :param U1: Primary voltage (Volts)
    :param U2: Secondary voltage (Volts)
    :param N1: Primary coil turns
    :param N2: Secondary coil turns
    :param I1: Primary current (Amperes)
    :param I2: Secondary current (Amperes)
    :return: Transformer relationships
    """
    return U1 / U2 == N1 / N2, I1 * U1 == I2 * U2