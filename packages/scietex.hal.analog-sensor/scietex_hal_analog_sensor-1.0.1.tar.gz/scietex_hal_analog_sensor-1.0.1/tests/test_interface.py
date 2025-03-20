"""Interface class testing."""

from abc import ABC
from typing import Union
import pytest
import numpy as np
from numpy.typing import NDArray

try:
    from src.scietex.hal.analog_sensor import AnalogSensorInterface
except ImportError:
    from scietex.hal.analog_sensor import AnalogSensorInterface


# pylint: disable=too-few-public-methods
class DummySensor(AnalogSensorInterface):
    """Test implementation."""

    def convert_voltage(
        self, voltage: Union[float, NDArray[np.float64]]
    ) -> Union[float, NDArray[np.float64]]:
        # Simple test conversion: multiply voltage by 2
        return voltage * 2


def test_cannot_instantiate_abstract_class():
    """Test that the abstract base class cannot be instantiated directly."""
    with pytest.raises(TypeError, match="Can't instantiate abstract class"):
        # pylint: disable=abstract-class-instantiated
        AnalogSensorInterface("test_model")


def test_model_name_attribute():
    """Test that model_name is properly set during initialization."""
    sensor = DummySensor("test_model_123")
    assert sensor.model_name == "test_model_123"
    assert isinstance(sensor.model_name, str)


def test_convert_voltage_single_value():
    """Test convert_voltage with a single float value."""
    sensor = DummySensor("test_model")
    result = sensor.convert_voltage(2.5)
    assert isinstance(result, float)
    assert result == 5.0  # 2.5 * 2


def test_convert_voltage_numpy_array():
    """Test convert_voltage with a numpy array."""
    sensor = DummySensor("test_model")
    input_array = np.array([1.0, 2.0, 3.0], dtype=np.float64)
    result = sensor.convert_voltage(input_array)

    assert isinstance(result, np.ndarray)
    assert result.dtype == np.float64
    np.testing.assert_array_equal(result, np.array([2.0, 4.0, 6.0]))


def test_convert_voltage_invalid_implementation():
    """Test that a subclass without proper implementation raises TypeError."""

    # pylint: disable=too-few-public-methods
    class BadSensor(AnalogSensorInterface):
        """Bad abstract class implementation"""

    with pytest.raises(TypeError):
        _ = BadSensor("bad_model")


@pytest.mark.parametrize(
    "model_name",
    [
        "sensor_1",
        "TEMP_SENSOR_2000",
        "",  # Empty string should still work
    ],
)
def test_valid_model_names(model_name):
    """Test initialization with various valid model names."""
    sensor = DummySensor(model_name)
    assert sensor.model_name == model_name


def test_interface_is_abc():
    """Test that AnalogSensorInterface is an abstract base class."""
    assert issubclass(AnalogSensorInterface, ABC)
    assert hasattr(AnalogSensorInterface, "convert_voltage")
    assert AnalogSensorInterface.convert_voltage.__isabstractmethod__


if __name__ == "__main__":
    pytest.main()
