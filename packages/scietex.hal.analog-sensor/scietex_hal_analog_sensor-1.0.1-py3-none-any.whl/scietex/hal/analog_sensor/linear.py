"""
Linear Sensor Module.

This module provides implementations of linear analog sensors, which convert analog voltage
readings into physical quantities using a linear transformation. It includes two classes:
    - LinearSensor: A basic linear sensor implementation.
    - LinearLimitedSensor: A linear sensor with voltage limits to clamp the output.

Classes:
    - LinearSensor: Implements a linear transformation for voltage-to-physical quantity conversion.
    - LinearLimitedSensor: Extends LinearSensor to include voltage limits for clamping.
"""

from typing import Union
import numpy as np
from numpy.typing import NDArray

from .interface import AnalogSensorInterface


# pylint: disable=too-few-public-methods
class LinearSensor(AnalogSensorInterface):
    """
    A basic linear sensor implementation.

    This class converts analog voltage readings into physical quantities using a linear
    transformation: `output = voltage * gain + offset`. It inherits from `AnalogSensorInterface`
    and implements the `convert_voltage` method.

    Attributes:
        model_name (str): The name or model identifier of the sensor.
        gain (float): The gain factor for the linear transformation.
        offset (float): The offset for the linear transformation. Defaults to 0.0.

    Methods:
        convert_voltage(voltage: Union[float, NDArray[np.float64]])
            -> Union[float, NDArray[np.float64]]:
            Converts analog voltage readings into physical quantities using a linear
            transformation.
    """

    def __init__(self, model_name: str, gain: float, offset: float = 0.0):
        """
        Initializes the LinearSensor instance.

        Args:
            model_name (str): The name or model identifier of the sensor.
            gain (float): The gain factor for the linear transformation.
            offset (float, optional): The offset for the linear transformation. Defaults to 0.0.
        """
        super().__init__(model_name)
        self.gain: float = gain
        self.offset: float = offset

    def convert_voltage(
        self, voltage: Union[float, NDArray[np.float64]]
    ) -> Union[float, NDArray[np.float64]]:
        """
        Converts analog voltage readings into physical quantities using a linear transformation.

        The conversion formula is: `output = voltage * gain + offset`.

        Args:
            voltage (Union[float, NDArray[np.float64]]): The analog voltage reading(s) to convert.
                Can be a single float or a NumPy array of floats.

        Returns:
            Union[float, NDArray[np.float64]]: The converted physical quantity.
                The return type matches the input type (single value or array).
        """
        return voltage * self.gain + self.offset


# pylint: disable=too-few-public-methods
class LinearLimitedSensor(LinearSensor):
    """
    A linear sensor implementation with voltage limits.

    This class extends `LinearSensor` to include voltage limits (`v_min` and `v_max`). If the input
    voltage is outside these limits, the output is clamped to the value corresponding to the
    nearest limit. This ensures that the output remains within a specified range.

    Attributes:
        model_name (str): The name or model identifier of the sensor.
        gain (float): The gain factor for the linear transformation.
        offset (float): The offset for the linear transformation. Defaults to 0.0.
        v_min (float): The minimum allowed voltage. Inputs below this value are clamped.
        v_max (float): The maximum allowed voltage. Inputs above this value are clamped.

    Methods:
        convert_voltage(voltage: Union[float, NDArray[np.float64]])
            -> Union[float, NDArray[np.float64]]:
            Converts analog voltage readings into physical quantities, clamping the output if the
            input voltage is outside the specified limits.
    """

    # pylint: disable=too-many-arguments,too-many-positional-arguments
    def __init__(
        self,
        v_min: float,
        v_max: float,
        model_name: str,
        gain: float,
        offset: float = 0.0,
    ):
        """
        Initializes the LinearLimitedSensor instance.

        Args:
            v_min (float): The minimum allowed voltage. Inputs below this value are clamped.
            v_max (float): The maximum allowed voltage. Inputs above this value are clamped.
            model_name (str): The name or model identifier of the sensor.
            gain (float): The gain factor for the linear transformation.
            offset (float, optional): The offset for the linear transformation. Defaults to 0.0.
        """
        super().__init__(model_name, gain, offset)
        self.v_min = min(v_min, v_max)
        self.v_max = max(v_min, v_max)

    def convert_voltage(
        self, voltage: Union[float, NDArray[np.float64]]
    ) -> Union[float, NDArray[np.float64]]:
        """
        Converts analog voltage readings into physical quantities, clamping the output if the
        input voltage is outside the specified limits.

        The conversion formula is: `output = voltage * gain + offset`. If the input voltage is
        below `v_min` or above `v_max`, the output is clamped to the value corresponding to `v_min`
        or `v_max`, respectively.

        Args:
            voltage (Union[float, NDArray[np.float64]]): The analog voltage reading(s) to convert.
                Can be a single float or a NumPy array of floats.

        Returns:
            Union[float, NDArray[np.float64]]: The converted physical quantity, clamped to the
                specified limits. The return type matches the input type (single value or array).
        """
        voltage_array = np.asarray(voltage)
        clamped_voltage = np.clip(voltage_array, self.v_min, self.v_max)
        result = super().convert_voltage(clamped_voltage)
        if isinstance(voltage, float):
            return float(result)
        return result
