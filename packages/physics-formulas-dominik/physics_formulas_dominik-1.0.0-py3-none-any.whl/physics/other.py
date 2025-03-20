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

def relativistic_energy(m, v, c=3e8):
    """
    Calculates total relativistic energy of an object.
    :param m: Mass (kg)
    :param v: Velocity (m/s)
    :param c: Speed of light (m/s)
    :return: Total energy (Joules)
    """
    return m * c**2 / math.sqrt(1 - v**2 / c**2)

def mass_energy_equivalence(m, c=3e8):
    """
    E=mc^2 equation.
    :param m: Mass (kg)
    :param c: Speed of light (m/s)
    :return: Energy (Joules)
    """
    return m * c**2

def de_broglie_wavelength(h, p):
    """
    Calculates the De Broglie wavelength of a particle.
    :param h: Planck's constant (J·s)
    :param p: Momentum (kg·m/s)
    :return: Wavelength (meters)
    """
    return h / p

def photoelectric_energy(h, f, W):
    """
    Calculates the maximum kinetic energy of an ejected photoelectron.
    :param h: Planck's constant (J·s)
    :param f: Frequency of incoming light (Hz)
    :param W: Work function of the material (Joules)
    :return: Maximum kinetic energy (Joules)
    """
    return h * f - W

def total_energy(m, v, c=3e8):
    """
    Calculates the total energy of a moving body in relativistic mechanics.
    E = mc^2 / sqrt(1 - v^2/c^2)
    """
    return m * c**2 / math.sqrt(1 - v**2 / c**2)

def rest_energy(m, c=3e8):
    """
    Calculates the rest energy of a body.
    E0 = mc^2
    """
    return m * c**2

def energy_mass_relation(dE, c=3e8):
    """
    Relates the change in mass to the emitted energy.
    ΔE = Δm * c^2
    """
    return dE / c**2

def relativistic_momentum(m, v, c=3e8):
    """
    Calculates relativistic momentum.
    p = mv / sqrt(1 - v^2/c^2)
    """
    return m * v / math.sqrt(1 - v**2 / c**2)

def relativistic_energy_invariant(E, p, c=3e8):
    """
    Calculates the relativistic invariant.
    E^2 = E0^2 + (pc)^2
    """
    return math.sqrt(E**2 - (p * c)**2)

def kinetic_energy(E, E0):
    """
    Calculates kinetic energy.
    E_kin = E - E0
    """
    return E - E0

def planck_energy(f, h=6.626e-34):
    """
    Calculates photon energy using Planck's equation.
    E = hf
    """
    return h * f

def de_broglie_wavelength(h, p):
    """
    Calculates De Broglie wavelength.
    λ = h / p
    """
    return h / p

def radioactive_decay(N0, t, T_half):
    """
    Computes the remaining number of radioactive atoms.
    N(t) = N0 * (1/2)^(t/T_half)
    """
    return N0 * (0.5) ** (t / T_half)
