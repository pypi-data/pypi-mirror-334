import math

def pressure_force(pressure: float, area: float) -> float:
    """
    Calculates the force exerted by a pressure on a surface.

    Args:
        pressure (float): Pressure applied (Pa).
        area (float): Surface area (m²).

    Returns:
        float: Force exerted (N).
    
    Raises:
        ValueError: If pressure or area is non-positive.
    """
    if pressure <= 0 or area <= 0:
        raise ValueError("Pressure and area must be positive.")
    return pressure * area

def hydrostatic_pressure_change(density: float, gravity: float, height: float) -> float:
    """
    Calculates the change in pressure due to a difference in height in a fluid.

    Args:
        density (float): Density of the fluid (kg/m³).
        gravity (float): Gravitational acceleration (m/s²).
        height (float): Height difference (m).

    Returns:
        float: Pressure change (Pa).
    
    Raises:
        ValueError: If any input is non-positive.
    """
    if density <= 0 or gravity <= 0 or height <= 0:
        raise ValueError("Density, gravity, and height must be positive.")
    return density * gravity * height

def buoyant_force(density: float, submerged_volume: float, gravity: float) -> float:
    """
    Calculates the buoyant force exerted on an object submerged in a fluid.

    Args:
        density (float): Density of the fluid (kg/m³).
        submerged_volume (float): Volume of the submerged part of the object (m³).
        gravity (float): Gravitational acceleration (m/s²).

    Returns:
        float: Buoyant force (N).
    
    Raises:
        ValueError: If any input is non-positive.
    """
    if density <= 0 or submerged_volume <= 0 or gravity <= 0:
        raise ValueError("Density, submerged volume, and gravity must be positive.")
    return density * submerged_volume * gravity
