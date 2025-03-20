import math

def vector_add(v1, v2):
    """
    Adds two vectors.
    
    :param v1: First vector (tuple or list of numbers).
    :param v2: Second vector (tuple or list of numbers).
    :return: Sum of vectors as a tuple.
    """
    return tuple(v1[i] + v2[i] for i in range(len(v1)))

def vector_subtract(v1, v2):
    """
    Subtracts two vectors.
    
    :param v1: First vector.
    :param v2: Second vector.
    :return: Difference of vectors.
    """
    return tuple(v1[i] - v2[i] for i in range(len(v1)))

def vector_dot_product(v1, v2):
    """
    Computes the dot product of two vectors.
    
    :param v1: First vector.
    :param v2: Second vector.
    :return: Scalar result of the dot product.
    """
    return sum(v1[i] * v2[i] for i in range(len(v1)))

def vector_cross_product(v1, v2):
    """
    Computes the cross product of two 3D vectors.
    
    :param v1: First vector (3-element tuple).
    :param v2: Second vector (3-element tuple).
    :return: Cross product as a vector.
    """
    return (v1[1] * v2[2] - v1[2] * v2[1],
            v1[2] * v2[0] - v1[0] * v2[2],
            v1[0] * v2[1] - v1[1] * v2[0])

def vector_magnitude(v):
    """
    Computes the magnitude (length) of a vector.
    
    :param v: Vector.
    :return: Magnitude of the vector (scalar).
    """
    return math.sqrt(sum(x**2 for x in v))

def momentum(m, v):
    """
    Computes linear momentum.
    
    :param m: Mass of the object (kg).
    :param v: Velocity vector (m/s).
    :return: Momentum as a vector.
    """
    return tuple(m * vi for vi in v)

def newtons_second_law(m, a):
    """
    Computes force using Newton's Second Law.
    
    :param m: Mass (kg).
    :param a: Acceleration vector (m/s²).
    :return: Force as a vector.
    """
    return tuple(m * ai for ai in a)

def force_from_momentum_change(dp, dt):
    """
    Computes force as the rate of change of momentum.
    
    :param dp: Change in momentum (vector).
    :param dt: Time change (s).
    :return: Force as a vector.
    """
    return tuple(dpi / dt for dpi in dp)

def angular_momentum(r, p):
    """
    Computes angular momentum.
    
    :param r: Position vector (m).
    :param p: Linear momentum vector (kg·m/s).
    :return: Angular momentum as a vector.
    """
    return vector_cross_product(r, p)

def torque(r, F):
    """
    Computes torque (moment of force).
    
    :param r: Position vector (m).
    :param F: Force vector (N).
    :return: Torque as a vector.
    """
    return vector_cross_product(r, F)

def moment_of_inertia(mass_radii):
    """
    Computes the moment of inertia for a system of point masses.
    
    :param mass_radii: List of tuples (mass, radius).
    :return: Moment of inertia (kg·m²).
    """
    return sum(m * r**2 for m, r in mass_radii)

def angular_momentum_from_rotation(I, omega):
    """
    Computes angular momentum using the moment of inertia and angular velocity.
    
    :param I: Moment of inertia (kg·m²).
    :param omega: Angular velocity vector (rad/s).
    :return: Angular momentum as a vector.
    """
    return tuple(I * wi for wi in omega)

def rotational_newtons_second_law(I, alpha):
    """
    Computes torque in rotational motion.
    
    :param I: Moment of inertia (kg·m²).
    :param alpha: Angular acceleration vector (rad/s²).
    :return: Torque as a vector.
    """
    return tuple(I * ai for ai in alpha)

def work_from_force(F, dr):
    """
    Computes the work done by a force.
    
    :param F: Force vector (N).
    :param dr: Displacement vector (m).
    :return: Work (J).
    """
    return vector_dot_product(F, dr)

def work_from_torque(M, dalpha):
    """
    Computes the work done by torque.
    
    :param M: Torque (Nm).
    :param dalpha: Change in angular displacement (rad).
    :return: Work (J).
    """
    return vector_dot_product(M, dalpha)

def power(W, dt):
    """
    Computes power as work per unit time.
    
    :param W: Work done (J).
    :param dt: Time (s).
    :return: Power (W).
    """
    return W / dt

def kinetic_energy_translational(m, v):
    """
    Computes the kinetic energy of translational motion.
    
    :param m: Mass (kg).
    :param v: Velocity vector (m/s).
    :return: Kinetic energy (J).
    """
    return 0.5 * m * vector_magnitude(v)**2

def kinetic_energy_rotational(I, omega):
    """
    Computes the kinetic energy of rotational motion.
    
    :param I: Moment of inertia (kg·m²).
    :param omega: Angular velocity vector (rad/s).
    :return: Rotational kinetic energy (J).
    """
    return 0.5 * I * vector_magnitude(omega)**2
