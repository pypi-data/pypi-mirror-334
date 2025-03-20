"""
Sensor Interpolation Module.

This module provides concrete implementations of the AnalogSensorInterface using various
interpolation methods for converting voltage readings to physical quantities. Each class
implements a different interpolation technique suitable for different types of sensor data.

Classes:
    LinearInterpolatorSensor: Uses linear interpolation between data points.
    CubicSplineInterpolatorSensor: Uses cubic spline interpolation with configurable boundary
        conditions.
    AkimaInterpolatorSensor: Uses Akima interpolation for smooth curves with less overshoot.
    PchipInterpolatorSensor: Uses PCHIP (Piecewise Cubic Hermite Interpolating Polynomial)
        interpolation.
"""

from typing import Union, Optional, Literal
import numpy as np
from numpy.typing import NDArray
from scipy.interpolate import CubicSpline, Akima1DInterpolator, PchipInterpolator  # type: ignore

from .interface import AnalogSensorInterface


def _validate_data_array(data: NDArray[np.float64]) -> NDArray[np.float64]:
    if not (len(data.shape) == 2 and data.shape[1] == 2):
        raise ValueError("Wrong data array shape")
    return data


# pylint: disable=too-few-public-methods
class LinearInterpolatorSensor(AnalogSensorInterface):
    """
    A sensor class that uses linear interpolation to convert voltage readings.

    This class implements the AnalogSensorInterface using NumPy's linear interpolation
    to convert voltage readings to physical quantities based on provided calibration data.

    Attributes:
        model_name (str): The name or model identifier of the sensor.
        data (NDArray[np.float64]): 2D array where first column is voltage values and second column
            is corresponding physical quantities.
    """

    def __init__(
        self,
        model_name: str,
        data: NDArray[np.float64],
        extrapolate: Optional[bool] = None,
    ):
        """
        Initialize the LinearInterpolatorSensor.

        Args:
            model_name (str): The name or model identifier of the sensor.
            data (NDArray[np.float64]): 2D array with shape (n, 2) containing voltage values
                in first column and corresponding physical quantities in second column.
        """
        super().__init__(model_name)
        self.data = _validate_data_array(data)

        _ = extrapolate

    def convert_voltage(
        self, voltage: Union[float, NDArray[np.float64]]
    ) -> Union[float, NDArray[np.float64]]:
        """
        Convert voltage readings to physical quantities using linear interpolation.

        Args:
            voltage (Union[float, NDArray[np.float64]]): Voltage value(s) to convert,
                either a single float or NumPy array.

        Returns:
            Union[float, NDArray[np.float64]]: Converted physical quantity(ies),
                matching the input type (float or array).
        """
        return np.interp(voltage, self.data[:, 0], self.data[:, 1])


# pylint: disable=too-few-public-methods
class CubicSplineInterpolatorSensor(AnalogSensorInterface):
    """
    A sensor class that uses cubic spline interpolation to convert voltage readings.

    This class implements the AnalogSensorInterface using SciPy's CubicSpline
    interpolation, offering smooth curves with configurable boundary conditions.

    Attributes:
        model_name (str): The name or model identifier of the sensor.
        data (NDArray[np.float64]): 2D array where first column is voltage values and second column
            is corresponding physical quantities.
        spl (CubicSpline): The cubic spline interpolation object.
    """

    BC = Literal["not-a-knot", "periodic", "clamped", "natural"]

    def __init__(
        self,
        model_name: str,
        data: NDArray[np.float64],
        bc: Optional[BC] = None,
        extrapolate: Optional[bool] = None,
    ):
        """
        Initialize the CubicSplineInterpolatorSensor.

        Args:
            model_name (str): The name or model identifier of the sensor.
            data (NDArray[np.float64]): 2D array with shape (n, 2) containing voltage values
                in first column and corresponding physical quantities in second column.
            bc (Optional[BC]): Boundary condition type for the spline. One of
                "not-a-knot", "periodic", "clamped", or "natural". Defaults to None.
            extrapolate (Optional[bool]): Whether to extrapolate beyond data points.
                Defaults to None (SciPy default behavior).
        """
        super().__init__(model_name)
        self.data = _validate_data_array(data)
        self.spl = CubicSpline(
            self.data[:, 0], self.data[:, 1], bc_type=bc, extrapolate=extrapolate
        )

    def convert_voltage(
        self, voltage: Union[float, NDArray[np.float64]]
    ) -> Union[float, NDArray[np.float64]]:
        """
        Convert voltage readings to physical quantities using cubic spline interpolation.

        Args:
            voltage (Union[float, NDArray[np.float64]]): Voltage value(s) to convert,
                either a single float or NumPy array.

        Returns:
            Union[float, NDArray[np.float64]]: Converted physical quantity(ies),
                float if input is float, array if input is array.
        """
        result = self.spl(voltage)
        if isinstance(voltage, float):
            return float(result)
        return result


# pylint: disable=too-few-public-methods
class AkimaInterpolatorSensor(AnalogSensorInterface):
    """
    A sensor class that uses Akima interpolation to convert voltage readings.

    This class implements the AnalogSensorInterface using SciPy's Akima1DInterpolator,
    providing smooth interpolation with reduced overshoot compared to cubic splines.

    Attributes:
        model_name (str): The name or model identifier of the sensor.
        data (NDArray[np.float64]): 2D array where first column is voltage values and second column
            is corresponding physical quantities.
        akima (Akima1DInterpolator): The Akima interpolation object.
    """

    def __init__(
        self,
        model_name: str,
        data: NDArray[np.float64],
        extrapolate: Optional[bool] = None,
    ):
        """
        Initialize the AkimaInterpolatorSensor.

        Args:
            model_name (str): The name or model identifier of the sensor.
            data (NDArray[np.float64]): 2D array with shape (n, 2) containing voltage values
                in first column and corresponding physical quantities in second column.
            extrapolate (Optional[bool]): Whether to extrapolate beyond data points.
                Defaults to None (SciPy default behavior).
        """
        super().__init__(model_name)
        self.data = _validate_data_array(data)
        try:
            # pylint: disable=unexpected-keyword-arg
            self.akima = Akima1DInterpolator(
                self.data[:, 0], self.data[:, 1], extrapolate=extrapolate
            )
        except TypeError:
            # extrapolate not supported before scipy v1.14
            self.akima = Akima1DInterpolator(self.data[:, 0], self.data[:, 1])

    def convert_voltage(
        self, voltage: Union[float, NDArray[np.float64]]
    ) -> Union[float, NDArray[np.float64]]:
        """
        Convert voltage readings to physical quantities using Akima interpolation.

        Args:
            voltage (Union[float, NDArray[np.float64]]): Voltage value(s) to convert,
                either a single float or NumPy array.

        Returns:
            Union[float, NDArray[np.float64]]: Converted physical quantity(ies),
                float if input is float, array if input is array.
        """
        result = self.akima(voltage)
        if isinstance(voltage, float):
            return float(result)
        return result


# pylint: disable=too-few-public-methods
class PchipInterpolatorSensor(AnalogSensorInterface):
    """
    A sensor class that uses PCHIP interpolation to convert voltage readings.

    This class implements the AnalogSensorInterface using SciPy's PchipInterpolator,
    providing shape-preserving interpolation with continuous first derivatives.

    Attributes:
        model_name (str): The name or model identifier of the sensor.
        data (NDArray[np.float64]): 2D array where first column is voltage values and second column
            is corresponding physical quantities.
        pchip (PchipInterpolator): The PCHIP interpolation object.
    """

    def __init__(
        self,
        model_name: str,
        data: NDArray[np.float64],
        extrapolate: Optional[bool] = None,
    ):
        """
        Initialize the PchipInterpolatorSensor.

        Args:
            model_name (str): The name or model identifier of the sensor.
            data (NDArray[np.float64]): 2D array with shape (n, 2) containing voltage values
                in first column and corresponding physical quantities in second column.
            extrapolate (Optional[bool]): Whether to extrapolate beyond data points.
                Defaults to None (SciPy default behavior).
        """
        super().__init__(model_name)
        self.data = _validate_data_array(data)
        self.pchip = PchipInterpolator(
            self.data[:, 0], self.data[:, 1], extrapolate=extrapolate
        )

    def convert_voltage(
        self, voltage: Union[float, NDArray[np.float64]]
    ) -> Union[float, NDArray[np.float64]]:
        """
        Convert voltage readings to physical quantities using PCHIP interpolation.

        Args:
            voltage (Union[float, NDArray[np.float64]]): Voltage value(s) to convert,
                either a single float or NumPy array.

        Returns:
            Union[float, NDArray[np.float64]]: Converted physical quantity(ies),
                float if input is float, array if input is array.
        """
        result = self.pchip(voltage)
        if isinstance(voltage, float):
            return float(result)
        return result
