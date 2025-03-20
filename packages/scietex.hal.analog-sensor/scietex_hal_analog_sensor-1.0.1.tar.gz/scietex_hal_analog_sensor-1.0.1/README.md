# scietex.hal.analog_sensor

The `scietex.hal.analog_sensor` package is a Python library for interfacing with and processing
data from analog sensors. It provides an abstract base class (`AnalogSensorInterface`) and concrete
implementations for converting analog voltage readings into physical quantities (e.g., temperature,
pressure) using linear transformations and advanced interpolation techniques.

## Features
- Abstract base class (`AnalogSensorInterface`) for consistent sensor implementations.
- Support for single `float` values and NumPy arrays (`NDArray[np.float64]`) for batch processing.
- Linear sensor models:
  - `LinearSensor`: Basic linear transformation (`gain * voltage + offset`).
  - `LinearLimitedSensor`: Linear transformation with voltage clamping.
- Interpolation-based sensors for non-linear data:
  - `LinearInterpolatorSensor`: Linear interpolation using NumPy.
  - `CubicSplineInterpolatorSensor`: Cubic spline interpolation with configurable boundary
     conditions.
  - `AkimaInterpolatorSensor`: Akima interpolation for smooth curves with less overshoot.
  - `PchipInterpolatorSensor`: PCHIP interpolation for shape-preserving curves.
- Extensible design for custom sensor models.
- Built on NumPy and SciPy for efficient numerical and interpolation operations.

## Installation
Install the package via pip (assuming it’s published to PyPI):
```bash
pip install scietex.hal.analog_sensor
```

Alternatively, clone the repository and install locally:
```bash
git clone https://github.com/bond-anton/scietex.hal.analog_sensor.git
cd scietex.hal.analog_sensor
pip install .
```

## Requirements

 - Python 3.9 or higher.
 - `numpy` (for array operations and linear interpolation).
 - `scipy` (for cubic spline, Akima, and PCHIP interpolation).

## Usage
The package uses AnalogSensorInterface as a base class, requiring subclasses to implement
`convert_voltage`. 
Linear sensors use a simple gain-offset model, while interpolation-based sensors require
calibration data.

Basic example with a linear sensor:
```python
from scietex.hal.analog_sensor import LinearSensor

# Linear sensor: output = gain * voltage + offset
sensor = LinearSensor(model_name="PressureSensor", gain=0.5, offset=10)

# Convert a voltage
value = sensor.convert_voltage(100)
print(f"Physical value: {value}")  # Output: 60.0
```

Using cubic spline interpolation:

```python
import numpy as np
from scietex.hal.analog_sensor import CubicSplineInterpolatorSensor

# Calibration data: [voltage, physical value]
data = np.array([[0, 0], [50, 25], [100, 50]])
sensor = CubicSplineInterpolatorSensor(
    model_name="LightSensor", data=data, bc="natural"
)

# Convert an array of voltages
voltages = np.array([25, 75])
values = sensor.convert_voltage(voltages)
print(f"Physical values: {values}")  # Output depends on spline fit
```

## Modules
 - **`AnalogSensorInterface`** (in `interface.py`):
   - Abstract base class requiring `convert_voltage` implementation.
   - Attributes: `model_name` (str) for sensor identification.
   - Supports single float or NumPy array inputs/outputs.
 - **`LinearSensor`** (in `linear.py`):
   - Linear transformation: `gain * voltage + offset`.
   - Args: `model_name`, `gain`, `offset` (optional, default 0.0).
 - **`LinearLimitedSensor`** (in `linear.py`):
   - Linear transformation with voltage clamping between `v_min` and `v_max`.
   - Args: `v_min`, `v_max`, `model_name`, `gain`, `offset` (optional, default 0.0).
 - **`LinearInterpolatorSensor`** (in `interpolation.py`):
   - Linear interpolation using `np.interp`.
   - Args: `model_name`, `data` (2D array: voltage, physical value), `extrapolate` (optional).
 - **`CubicSplineInterpolatorSensor`** (in `interpolation.py`):
   - Cubic spline interpolation via `scipy.interpolate.CubicSpline`.
   - Args: `model_name`, `data`, `bc` (e.g., "natural", "clamped"), `extrapolate` (optional).
 - **`AkimaInterpolatorSensor`** (in `interpolation.py`):
   - Akima interpolation via `scipy.interpolate.Akima1DInterpolator`.
   - Args: `model_name`, `data`, `extrapolate` (optional, SciPy 1.14+).
 - **`PchipInterpolatorSensor`** (in `interpolation.py`):
   - PCHIP interpolation via `scipy.interpolate.PchipInterpolator`.
   - Args: `model_name`, `data`, `extrapolate` (optional).
 
## Contributing

Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/YourFeature`).
3. Commit your changes (`git commit -m "Add your message"`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Open a Pull Request.

Please include tests (if applicable) and follow PEP 8 style guidelines.

## License

This project is licensed under the **MIT License** - see the LICENSE file for details.
