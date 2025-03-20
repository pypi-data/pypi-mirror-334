"""Tests for interpolation sensors."""

import pytest
import numpy as np
import scipy

try:
    from src.scietex.hal.analog_sensor.interpolation import (
        _validate_data_array,
        LinearInterpolatorSensor,
        CubicSplineInterpolatorSensor,
        AkimaInterpolatorSensor,
        PchipInterpolatorSensor,
    )
except ImportError:
    from scietex.hal.analog_sensor.interpolation import (
        _validate_data_array,
        LinearInterpolatorSensor,
        CubicSplineInterpolatorSensor,
        AkimaInterpolatorSensor,
        PchipInterpolatorSensor,
    )


# Test fixture for sample data
@pytest.fixture
def sample_data():
    """Provide sample calibration data for tests."""
    return np.array(
        [[0.0, 0.0], [1.0, 10.0], [2.0, 20.0], [3.0, 30.0]], dtype=np.float64
    )


# Test fixture for periodic sample data
@pytest.fixture
def sample_data_periodic():
    """Provide sample calibration data for tests."""
    return np.array(
        [[0.0, 0.0], [1.0, 10.0], [2.0, 20.0], [3.0, 0.0]], dtype=np.float64
    )


# Parameterized test data for boundary conditions
bc_types = ["not-a-knot", "periodic", "clamped", "natural"]

# Test classes in a list for parameterized testing
sensor_classes = [
    LinearInterpolatorSensor,
    CubicSplineInterpolatorSensor,
    AkimaInterpolatorSensor,
    PchipInterpolatorSensor,
]


def test_validate_data_array():
    """Test data array validation"""
    # Test case 1: Valid 2D array with 2 columns
    valid_array = np.array([[1.0, 2.0], [3.0, 4.0]], dtype=np.float64)
    result = _validate_data_array(valid_array)
    np.testing.assert_array_equal(result, valid_array)

    # Test case 2: Invalid 1D array
    invalid_1d = np.array([1.0, 2.0], dtype=np.float64)
    with pytest.raises(ValueError, match="Wrong data array shape"):
        _validate_data_array(invalid_1d)

    # Test case 3: Invalid 2D array with 3 columns
    invalid_2d = np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]], dtype=np.float64)
    with pytest.raises(ValueError, match="Wrong data array shape"):
        _validate_data_array(invalid_2d)

    # Test case 4: Invalid 3D array
    invalid_3d = np.array([[[1.0, 2.0], [3.0, 4.0]]], dtype=np.float64)
    with pytest.raises(ValueError, match="Wrong data array shape"):
        _validate_data_array(invalid_3d)

    # Test case 5: Empty 2D array with 2 columns
    valid_empty = np.array([[]], dtype=np.float64).reshape(0, 2)
    result = _validate_data_array(valid_empty)
    np.testing.assert_array_equal(result, valid_empty)


# pylint: disable=redefined-outer-name
def test_initialization(sample_data):
    """Test basic initialization of all sensor classes."""
    for sensor_class in sensor_classes:
        if sensor_class == CubicSplineInterpolatorSensor:
            sensor = sensor_class("test_sensor", sample_data, bc="not-a-knot")
        else:
            sensor = sensor_class("test_sensor", sample_data)

        assert sensor.model_name == "test_sensor"
        assert np.array_equal(sensor.data, sample_data)
        assert isinstance(sensor.data, np.ndarray)


# pylint: disable=redefined-outer-name
def test_linear_interpolation(sample_data):
    """Test LinearInterpolatorSensor voltage conversion."""
    sensor = LinearInterpolatorSensor("linear_sensor", sample_data)

    # Test single value
    result = sensor.convert_voltage(1.5)
    assert isinstance(result, float)
    assert result == 15.0  # Halfway between 10 and 20

    # Test array
    voltages = np.array([0.5, 1.5, 2.5])
    result = sensor.convert_voltage(voltages)
    assert isinstance(result, np.ndarray)
    np.testing.assert_array_almost_equal(result, [5.0, 15.0, 25.0])


# pylint: disable=redefined-outer-name
@pytest.mark.parametrize("bc_type", bc_types)
def test_cubic_spline_interpolation(sample_data_periodic, bc_type):
    """Test CubicSplineInterpolatorSensor voltage conversion with different boundary conditions."""
    sensor = CubicSplineInterpolatorSensor(
        "cubic_sensor", sample_data_periodic, bc=bc_type
    )

    # Test single value
    result = sensor.convert_voltage(1.5)
    assert isinstance(result, float)

    # Test array
    voltages = np.array([0.5, 1.5, 2.5])
    result = sensor.convert_voltage(voltages)
    assert isinstance(result, np.ndarray)
    assert result.shape == voltages.shape


# pylint: disable=redefined-outer-name
def test_akima_interpolation(sample_data):
    """Test AkimaInterpolatorSensor voltage conversion."""
    sensor = AkimaInterpolatorSensor("akima_sensor", sample_data)

    # Test single value
    result = sensor.convert_voltage(1.5)
    assert isinstance(result, float)

    # Test array
    voltages = np.array([0.5, 1.5, 2.5])
    result = sensor.convert_voltage(voltages)
    assert isinstance(result, np.ndarray)
    assert result.shape == voltages.shape


# pylint: disable=redefined-outer-name
def test_pchip_interpolation(sample_data):
    """Test PchipInterpolatorSensor voltage conversion."""
    sensor = PchipInterpolatorSensor("pchip_sensor", sample_data)

    # Test single value
    result = sensor.convert_voltage(1.5)
    assert isinstance(result, float)

    # Test array
    voltages = np.array([0.5, 1.5, 2.5])
    result = sensor.convert_voltage(voltages)
    assert isinstance(result, np.ndarray)
    assert result.shape == voltages.shape


# pylint: disable=redefined-outer-name
@pytest.mark.parametrize("sensor_class", sensor_classes)
def test_extrapolation(sample_data, sensor_class):
    """Test extrapolation behavior with extrapolate=True."""
    kwargs = {"extrapolate": True}
    if sensor_class == CubicSplineInterpolatorSensor:
        kwargs["bc"] = "not-a-knot"

    sensor = sensor_class("test_sensor", sample_data, **kwargs)

    scipy_v = [int(v) for v in scipy.__version__.split(".")]

    # Test value beyond data range
    result = sensor.convert_voltage(4.0)
    assert isinstance(result, float)
    if sensor_class == AkimaInterpolatorSensor:
        if scipy_v[0] == 1 and scipy_v[1] == 13:
            assert np.isnan(result)
    else:
        assert not np.isnan(result)


# pylint: disable=redefined-outer-name
@pytest.mark.parametrize(
    "sensor_class",
    [AkimaInterpolatorSensor, PchipInterpolatorSensor, CubicSplineInterpolatorSensor],
)
def test_no_extrapolation(sample_data, sensor_class):
    """Test behavior when extrapolation is disabled."""
    kwargs = {"extrapolate": False}
    if sensor_class == CubicSplineInterpolatorSensor:
        kwargs["bc"] = "not-a-knot"

    sensor = sensor_class("test_sensor", sample_data, **kwargs)

    # Test value beyond data range
    result = sensor.convert_voltage(4.0)
    assert isinstance(result, float)
    assert np.isnan(result)


# pylint: disable=redefined-outer-name
def test_invalid_data_shape():
    """Test initialization with invalid data shape."""
    invalid_data = np.array([1, 2, 3])  # 1D array instead of 2D
    for sensor_class in sensor_classes:
        with pytest.raises(ValueError):
            if sensor_class == CubicSplineInterpolatorSensor:
                sensor_class("test_sensor", invalid_data, bc="not-a-knot")
            else:
                sensor_class("test_sensor", invalid_data)


if __name__ == "__main__":
    pytest.main()
