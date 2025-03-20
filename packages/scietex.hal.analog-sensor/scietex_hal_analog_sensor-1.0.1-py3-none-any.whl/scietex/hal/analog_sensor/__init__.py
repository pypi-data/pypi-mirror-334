"""
This package provides interfaces and implementations for handling analog sensor data,
including linear sensors, limited range sensors, and various interpolation methods
for sensor readings.

Version:
    __version__: The current version of the package.

Available Classes:
    AnalogSensorInterface: Abstract base class defining the interface for analog sensors.
    LinearSensor: Implementation of a basic linear sensor.
    LinearLimitedSensor: Linear sensor with defined range limits.
    LinearInterpolatorSensor: Sensor using linear interpolation between data points.
    CubicSplineInterpolatorSensor: Sensor using cubic spline interpolation.
    Akima1DInterpolator: Sensor using Akima interpolation method.
    PchipInterpolator: Sensor using PCHIP (Piecewise Cubic Hermite Interpolating Polynomial).

Exports:
    __version__: Package version string
    AnalogSensorInterface: Base sensor interface
    LinearSensor: Linear sensor class
    LinearLimitedSensor: Limited range linear sensor class
    LinearInterpolatorSensor: Linear interpolation sensor class
    CubicSplineInterpolatorSensor: Cubic spline interpolation sensor class
    Akima1DInterpolator: Akima interpolation sensor class
    PchipInterpolator: PCHIP interpolation sensor class
"""

from .version import __version__

from .interface import AnalogSensorInterface
from .linear import LinearSensor, LinearLimitedSensor
from .interpolation import (
    LinearInterpolatorSensor,
    CubicSplineInterpolatorSensor,
    Akima1DInterpolator,
    PchipInterpolator,
)
