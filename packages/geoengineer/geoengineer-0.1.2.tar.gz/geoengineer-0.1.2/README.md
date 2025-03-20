# GeoEngineer

A simple Python package for geotechnical engineering calculations.

## Installation

```bash
pip install geoengineer
```

## Usage

```python
from geoengineer import effective_stress

# Calculate effective stress
sigma_prime = effective_stress(total_stress=100, pore_water_pressure=40)
print(f"Effective stress: {sigma_prime} kPa")  # Output: Effective stress: 60 kPa
```

## Features

- Calculate effective stress in soil

## License

This project is licensed under the MIT License - see the LICENSE file for details. 