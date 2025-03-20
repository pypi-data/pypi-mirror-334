"""
Soil mechanics module for geotechnical calculations.
"""

def effective_stress(total_stress: float, pore_water_pressure: float) -> float:
    """
    Calculate the effective stress in soil.
    
    Parameters:
        total_stress (float): The total stress (kPa).
        pore_water_pressure (float): The pore water pressure (kPa).
    
    Returns:
        float: The effective stress (kPa).
    
    Example:
        >>> effective_stress(100, 40)
        60
    """
    return total_stress - pore_water_pressure 