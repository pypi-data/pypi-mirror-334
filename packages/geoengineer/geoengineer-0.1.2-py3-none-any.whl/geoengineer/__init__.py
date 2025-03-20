"""
GeoEngineer - The official Python library for the GeoEngineerAI API.

This package provides functions for geotechnical engineering calculations.
"""

from .version import __version__
from .soil_mechanics import effective_stress

__all__ = ["effective_stress"] 