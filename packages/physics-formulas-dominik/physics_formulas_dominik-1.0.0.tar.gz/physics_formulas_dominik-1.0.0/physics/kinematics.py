import math

def speed(delta_r: float, delta_t: float) -> float:
    """
    Calculates speed as the change in position over time.

    Args:
        delta_r (float): Change in position (m).
        delta_t (float): Change in time (s).

    Returns:
        float: Speed (m/s).
    """
    return delta_r / delta_t

def acceleration(delta_v: float, delta_t: float) -> float:
    """
    Calculates acceleration as the change in velocity over time.

    Args:
        delta_v (float): Change in velocity (m/s).
        delta_t (float): Change in time (s).

    Returns:
        float: Acceleration (m/s²).
    """
    return delta_v / delta_t

def angular_velocity(delta_alpha: float, delta_t: float) -> float:
    """
    Calculates angular velocity as the change in angular displacement over time.

    Args:
        delta_alpha (float): Change in angular displacement (rad).
        delta_t (float): Change in time (s).

    Returns:
        float: Angular velocity (rad/s).
    """
    return delta_alpha / delta_t

def angular_linear_velocity_values(w: float, r: float) -> float:
    """
    Calculates linear velocity from angular velocity and radius.

    Args:
        w (float): Angular velocity (rad/s).
        r (float): Radius (m).

    Returns:
        float: Linear velocity (m/s).
    """
    return w * r

def angular_velocity_and_period(frequency: float = None, period: float = None) -> tuple[float, float]:
    """
    Calculates angular velocity and period given frequency or period.

    Args:
        frequency (float, optional): Frequency in Hz.
        period (float, optional): Period in seconds.

    Returns:
        tuple: (angular velocity (rad/s), period (s)).
    
    Raises:
        ValueError: If neither frequency nor period is provided.
    """
    if frequency is not None:
        T = 1 / frequency
        omega = 2 * math.pi / T
    elif period is not None:
        T = period
        omega = 2 * math.pi / T
    else:
        raise ValueError("Frequency or period is required.")
    
    return omega, T

def centripetal_acceleration(v: float = None, r: float = None, omega: float = None) -> float:
    """
    Calculates centripetal acceleration.

    Args:
        v (float, optional): Linear velocity (m/s).
        r (float, optional): Radius (m).
        omega (float, optional): Angular velocity (rad/s).

    Returns:
        float: Centripetal acceleration (m/s²).
    
    Raises:
        ValueError: If insufficient parameters are provided.
    """
    if v is not None and r is not None:
        return v**2 / r
    elif omega is not None and r is not None:
        return omega**2 * r
    elif v is not None and omega is not None:
        return v * omega
    else:
        raise ValueError("Provide at least two parameters (v, r, omega).")

def angular_acceleration(delta_omega: float, delta_t: float) -> float:
    """
    Calculates angular acceleration as the change in angular velocity over time.

    Args:
        delta_omega (float): Change in angular velocity (rad/s).
        delta_t (float): Time interval (s).

    Returns:
        float: Angular acceleration (rad/s²).
    """
    return delta_omega / delta_t

def tangential_acceleration(epsilon: float, r: float) -> float:
    """
    Calculates tangential acceleration as the product of angular acceleration and radius.

    Args:
        epsilon (float): Angular acceleration (rad/s²).
        r (float): Radius (m).

    Returns:
        float: Tangential acceleration (m/s²).
    """
    return epsilon * r

def linear_velocity(v0: float, a: float, t: float) -> float:
    """
    Calculates velocity in uniformly accelerated motion.

    Args:
        v0 (float): Initial velocity (m/s).
        a (float): Acceleration (m/s²).
        t (float): Time (s).

    Returns:
        float: Final velocity (m/s).
    """
    return v0 + a * t

def linear_distance(v0: float, a: float, t: float) -> float:
    """
    Calculates distance traveled in uniformly accelerated motion.

    Args:
        v0 (float): Initial velocity (m/s).
        a (float): Acceleration (m/s²).
        t (float): Time (s).

    Returns:
        float: Distance (m).
    """
    return v0 * t + 0.5 * a * t**2
