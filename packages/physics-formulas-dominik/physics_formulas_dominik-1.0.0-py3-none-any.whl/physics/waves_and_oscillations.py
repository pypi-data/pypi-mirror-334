import math

def harmonic_motion(position: float, amplitude: float, omega: float, phase: float, time: float) -> float:
    """
    Calculates the position of an object in simple harmonic motion.

    Args:
        position (float): Initial position (m).
        amplitude (float): Amplitude of motion (m).
        omega (float): Angular frequency (rad/s).
        phase (float): Initial phase (rad).
        time (float): Time (s).

    Returns:
        float: Position at time t (m).
    """
    return amplitude * math.sin(omega * time + phase)

def velocity_harmonic(amplitude: float, omega: float, phase: float, time: float) -> float:
    """
    Calculates the velocity in simple harmonic motion.

    Args:
        amplitude (float): Amplitude of motion (m).
        omega (float): Angular frequency (rad/s).
        phase (float): Initial phase (rad).
        time (float): Time (s).

    Returns:
        float: Velocity at time t (m/s).
    """
    return amplitude * omega * math.cos(omega * time + phase)

def acceleration_harmonic(amplitude: float, omega: float, phase: float, time: float) -> float:
    """
    Calculates the acceleration in simple harmonic motion.

    Args:
        amplitude (float): Amplitude of motion (m).
        omega (float): Angular frequency (rad/s).
        phase (float): Initial phase (rad).
        time (float): Time (s).

    Returns:
        float: Acceleration at time t (m/s²).
    """
    return -amplitude * omega**2 * math.sin(omega * time + phase)

def harmonic_force(mass: float, omega: float, displacement: float) -> float:
    """
    Calculates the harmonic restoring force.

    Args:
        mass (float): Mass of the object (kg).
        omega (float): Angular frequency (rad/s).
        displacement (float): Displacement from equilibrium (m).

    Returns:
        float: Restoring force (N).
    """
    return -mass * omega**2 * displacement

def angular_frequency_spring(mass: float, spring_constant: float) -> float:
    """
    Calculates angular frequency for a mass-spring system.

    Args:
        mass (float): Mass of the object (kg).
        spring_constant (float): Spring constant (N/m).

    Returns:
        float: Angular frequency (rad/s).
    """
    if mass <= 0 or spring_constant <= 0:
        raise ValueError("Mass and spring constant must be positive.")
    return math.sqrt(spring_constant / mass)

def angular_frequency_pendulum(length: float, gravity: float = 9.81) -> float:
    """
    Calculates angular frequency for a simple pendulum.

    Args:
        length (float): Length of the pendulum (m).
        gravity (float, optional): Acceleration due to gravity (m/s²). Default is 9.81 m/s².

    Returns:
        float: Angular frequency (rad/s).
    """
    if length <= 0:
        raise ValueError("Length must be positive.")
    return math.sqrt(gravity / length)

def total_energy_harmonic(mass: float, amplitude: float, omega: float) -> float:
    """
    Calculates the total energy in a simple harmonic oscillator.

    Args:
        mass (float): Mass of the object (kg).
        amplitude (float): Amplitude of motion (m).
        omega (float): Angular frequency (rad/s).

    Returns:
        float: Total mechanical energy (J).
    """
    return 0.5 * mass * amplitude**2 * omega**2

def wave_speed(wavelength: float, frequency: float) -> float:
    """
    Calculates the speed of a wave using the relationship v = λf.

    Args:
        wavelength (float): Wavelength of the wave (m).
        frequency (float): Frequency of the wave (Hz).

    Returns:
        float: Wave speed (m/s).
    
    Raises:
        ValueError: If wavelength or frequency is non-positive.
    """
    if wavelength <= 0 or frequency <= 0:
        raise ValueError("Wavelength and frequency must be positive.")
    return wavelength * frequency

def period_from_frequency(frequency: float) -> float:
    """
    Calculates the period of a wave from its frequency using T = 1/f.

    Args:
        frequency (float): Frequency of the wave (Hz).

    Returns:
        float: Period of the wave (s).
    
    Raises:
        ValueError: If frequency is non-positive.
    """
    if frequency <= 0:
        raise ValueError("Frequency must be positive.")
    return 1 / frequency

def wave_phase(x: float, t: float, wavelength: float, period: float, initial_phase: float = 0) -> float:
    """
    Calculates the phase of a wave at position x and time t using φ(t) = (2π/T) t - (2π/λ) x + φ₀.

    Args:
        x (float): Position along the wave (m).
        t (float): Time (s).
        wavelength (float): Wavelength of the wave (m).
        period (float): Period of the wave (s).
        initial_phase (float, optional): Initial phase φ₀ (rad). Default is 0.

    Returns:
        float: Phase of the wave (rad).
    
    Raises:
        ValueError: If wavelength or period is non-positive.
    """
    if wavelength <= 0 or period <= 0:
        raise ValueError("Wavelength and period must be positive.")
    return (2 * math.pi / period) * t - (2 * math.pi / wavelength) * x + initial_phase

def interference_maximum(phase1: float, phase2: float) -> bool:
    """
    Determines if two waves interfere constructively based on phase difference.
    Maximum interference occurs when φ₂ - φ₁ = 2πn.

    Args:
        phase1 (float): Phase of wave 1 (rad).
        phase2 (float): Phase of wave 2 (rad).

    Returns:
        bool: True if constructive interference occurs, False otherwise.
    """
    return math.isclose((phase2 - phase1) % (2 * math.pi), 0, abs_tol=1e-6)

def interference_minimum(phase1: float, phase2: float) -> bool:
    """
    Determines if two waves interfere destructively based on phase difference.
    Minimum interference occurs when φ₂ - φ₁ = 2π(n + 1/2).

    Args:
        phase1 (float): Phase of wave 1 (rad).
        phase2 (float): Phase of wave 2 (rad).

    Returns:
        bool: True if destructive interference occurs, False otherwise.
    """
    return math.isclose((phase2 - phase1) % (2 * math.pi), math.pi, abs_tol=1e-6)

def wave_intensity(energy: float, area: float, time: float) -> float:
    """
    Calculates wave intensity using the formula I = E / (SΔt).

    Args:
        energy (float): Energy carried by the wave (J).
        area (float): Area the wave passes through (m²).
        time (float): Time interval (s).

    Returns:
        float: Wave intensity (W/m²).
    
    Raises:
        ValueError: If energy, area, or time is non-positive.
    """
    if energy <= 0 or area <= 0 or time <= 0:
        raise ValueError("Energy, area, and time must be positive.")
    return energy / (area * time)

def wave_intensity_distance(intensity_initial: float, distance_initial: float, distance_final: float) -> float:
    """
    Calculates the wave intensity at a new distance using the inverse square law: I ~ 1/r².

    Args:
        intensity_initial (float): Initial wave intensity (W/m²).
        distance_initial (float): Initial distance from the source (m).
        distance_final (float): Final distance from the source (m).

    Returns:
        float: New wave intensity (W/m²).
    
    Raises:
        ValueError: If any input is non-positive.
    """
    if intensity_initial <= 0 or distance_initial <= 0 or distance_final <= 0:
        raise ValueError("Intensity and distances must be positive.")
    return intensity_initial * (distance_initial / distance_final) ** 2

def refraction_angle(n1: float, n2: float, angle1: float) -> float:
    """
    Calculates the refraction angle using Snell's Law: sin(α₁) / sin(α₂) = v₁ / v₂ = n₂ / n₁.

    Args:
        n1 (float): Refractive index of medium 1.
        n2 (float): Refractive index of medium 2.
        angle1 (float): Incident angle in degrees.

    Returns:
        float: Refraction angle (degrees).
    
    Raises:
        ValueError: If refractive indices are non-positive or sin(angle1) > 1.
    """
    if n1 <= 0 or n2 <= 0:
        raise ValueError("Refractive indices must be positive.")
    angle1_rad = math.radians(angle1)
    sin_angle2 = (n1 / n2) * math.sin(angle1_rad)
    if abs(sin_angle2) > 1:
        raise ValueError("Total internal reflection occurs; no refraction angle.")
    return math.degrees(math.asin(sin_angle2))

def doppler_effect_source_moving_observer_stationary(source_speed: float, wave_speed: float, frequency_source: float) -> float:
    """
    Calculates the observed frequency when the source moves and the observer is stationary.

    Args:
        source_speed (float): Speed of the source (m/s).
        wave_speed (float): Speed of the wave (m/s).
        frequency_source (float): Frequency of the source (Hz).

    Returns:
        float: Observed frequency (Hz).
    
    Raises:
        ValueError: If wave speed is non-positive or source speed is greater than or equal to wave speed.
    """
    if wave_speed <= 0 or abs(source_speed) >= wave_speed:
        raise ValueError("Wave speed must be positive and greater than source speed.")
    return frequency_source * (wave_speed / (wave_speed - source_speed))

def doppler_effect_observer_moving_source_stationary(observer_speed: float, wave_speed: float, frequency_source: float) -> float:
    """
    Calculates the observed frequency when the observer moves and the source is stationary.

    Args:
        observer_speed (float): Speed of the observer (m/s).
        wave_speed (float): Speed of the wave (m/s).
        frequency_source (float): Frequency of the source (Hz).

    Returns:
        float: Observed frequency (Hz).
    
    Raises:
        ValueError: If wave speed is non-positive.
    """
    if wave_speed <= 0:
        raise ValueError("Wave speed must be positive.")
    return frequency_source * ((wave_speed + observer_speed) / wave_speed)

def relativistic_doppler_effect(source_speed: float, speed_of_light: float, frequency_source: float) -> float:
    """
    Calculates the relativistic Doppler effect for a moving source.

    Args:
        source_speed (float): Speed of the source relative to the observer (m/s).
        speed_of_light (float): Speed of light in vacuum (m/s).
        frequency_source (float): Frequency of the source (Hz).

    Returns:
        float: Observed frequency (Hz).
    
    Raises:
        ValueError: If speed of light is non-positive or source speed is greater than or equal to the speed of light.
    """
    if speed_of_light <= 0 or abs(source_speed) >= speed_of_light:
        raise ValueError("Speed of light must be positive and greater than source speed.")
    doppler_factor = math.sqrt((1 - source_speed / speed_of_light) / (1 + source_speed / speed_of_light))
    return frequency_source * doppler_factor
