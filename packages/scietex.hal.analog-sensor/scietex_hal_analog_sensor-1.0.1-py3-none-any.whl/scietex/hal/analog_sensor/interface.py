"""
Analog Sensor Interface Module.

This module defines an abstract base class (`AnalogSensorInterface`) for analog sensor
implementations. The class provides a foundation for creating sensor models that convert analog
voltage readings into meaningful physical quantities (e.g., pressure, temperature, etc.).

Classes:
    - AnalogSensorInterface: An abstract base class for analog sensor implementations.
"""

from typing import Union
from abc import ABC, abstractmethod
import numpy as np
from numpy.typing import NDArray


# pylint: disable=too-few-public-methods
class AnalogSensorInterface(ABC):
    """
    Abstract base class for analog sensor implementations.

    This class defines the interface for analog sensors, requiring subclasses to implement
    the `convert_voltage` method. It is designed to be inherited by specific sensor models
    that convert analog voltage readings into physical quantities.

    Attributes:
        model_name (str): The name or model identifier of the sensor.

    Methods:
        convert_voltage(voltage: Union[float, np.ndarray[float]])
            -> Union[float, np.ndarray[float]]:
            Converts analog voltage readings into physical quantities. This method must be
            implemented by subclasses.
    """

    def __init__(self, model_name: str):
        """
        Initializes the AnalogSensorInterface instance.

        Args:
            model_name (str): The name or model identifier of the sensor.
        """
        self.model_name: str = model_name

    @abstractmethod
    def convert_voltage(
        self, voltage: Union[float, NDArray[np.float64]]
    ) -> Union[float, NDArray[np.float64]]:
        """
        Converts analog voltage readings into physical quantities.

        This method must be implemented by subclasses to provide sensor-specific conversion logic.
        It supports both single voltage values and arrays of voltage values for batch processing.

        Args:
            voltage (Union[float, NDArray[np.float64]]): The analog voltage reading(s) to convert.
                Can be a single float or a NumPy array of floats.

        Returns:
            Union[float, NDArray[np.float64]]: The converted physical quantity (e.g., pressure,
                temperature). The return type matches the input type (single value or array).

        Raises:
            NotImplementedError: If the method is not implemented by a subclass.
        """
