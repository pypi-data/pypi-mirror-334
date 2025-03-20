"""
GeoEngineer - A simple geotechnical engineering package.

This package provides functions for geotechnical engineering calculations.
"""

from .version import __version__
from .soil_mechanics import effective_stress

__all__ = ["effective_stress"] 