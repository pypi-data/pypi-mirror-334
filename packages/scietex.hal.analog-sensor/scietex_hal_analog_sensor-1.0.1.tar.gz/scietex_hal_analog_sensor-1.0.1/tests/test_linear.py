"""Tests for linear sensor."""

import pytest
import numpy as np

try:
    from src.scietex.hal.analog_sensor import LinearSensor, LinearLimitedSensor
except ModuleNotFoundError:
    from scietex.hal.analog_sensor import LinearSensor, LinearLimitedSensor


class TestLinearSensor:
    """Linear sensor testing."""

    @pytest.fixture
    def sensor(self):
        """Sensor fixture."""
        return LinearSensor(model_name="TestSensor", gain=2.0, offset=1.0)

    def test_init(self):
        """test constructor."""
        sensor = LinearSensor(model_name="TestSensor", gain=2.0, offset=1.0)
        assert sensor.model_name == "TestSensor"
        assert sensor.gain == 2.0
        assert sensor.offset == 1.0

    def test_convert_voltage_float(self, sensor):
        """test voltage conversion for a float argument."""
        assert sensor.convert_voltage(1.0) == 3.0  # 1.0 * 2.0 + 1.0 = 3.0
        assert sensor.convert_voltage(0.0) == 1.0  # 0.0 * 2.0 + 1.0 = 1.0
        assert sensor.convert_voltage(-1.0) == -1.0  # -1.0 * 2.0 + 1.0 = -1.0

    def test_convert_voltage_array(self, sensor):
        """test voltage conversion for an array argument."""
        input_array = np.array([0.0, 1.0, 2.0], dtype=np.float64)
        expected = np.array([1.0, 3.0, 5.0], dtype=np.float64)
        result = sensor.convert_voltage(input_array)
        np.testing.assert_array_equal(result, expected)


class TestLinearLimitedSensor:
    """Linear limited sensor testing."""

    @pytest.fixture
    def limited_sensor(self):
        """Sensor fixture."""
        return LinearLimitedSensor(
            v_min=0.0, v_max=2.0, model_name="TestLimitedSensor", gain=2.0, offset=1.0
        )

    def test_init(self):
        """Test constructor."""
        sensor = LinearLimitedSensor(
            v_min=2.0,  # Testing v_min > v_max case
            v_max=0.0,
            model_name="TestLimitedSensor",
            gain=2.0,
            offset=1.0,
        )
        assert sensor.model_name == "TestLimitedSensor"
        assert sensor.gain == 2.0
        assert sensor.offset == 1.0
        assert sensor.v_min == 0.0  # Should be min of input values
        assert sensor.v_max == 2.0  # Should be max of input values

    def test_convert_voltage_float_within_limits(self, limited_sensor):
        """Test voltage conversion with limits."""
        assert limited_sensor.convert_voltage(1.0) == 3.0  # 1.0 * 2.0 + 1.0 = 3.0

    def test_convert_voltage_float_below_limit(self, limited_sensor):
        """Test voltage conversion below limit."""
        assert (
            limited_sensor.convert_voltage(-1.0) == 1.0
        )  # Clamped to 0.0 * 2.0 + 1.0 = 1.0

    def test_convert_voltage_float_above_limit(self, limited_sensor):
        """Test voltage conversion above limit."""
        assert (
            limited_sensor.convert_voltage(3.0) == 5.0
        )  # Clamped to 2.0 * 2.0 + 1.0 = 5.0

    def test_convert_voltage_array(self, limited_sensor):
        """Test voltage conversion for an array."""
        input_array = np.array([-1.0, 0.0, 1.0, 2.0, 3.0], dtype=np.float64)
        expected = np.array([1.0, 1.0, 3.0, 5.0, 5.0], dtype=np.float64)
        result = limited_sensor.convert_voltage(input_array)
        np.testing.assert_array_equal(result, expected)

    def test_convert_voltage_type_preservation(self, limited_sensor):
        """Test voltage conversion type preserve."""
        # Test float input returns float
        assert isinstance(limited_sensor.convert_voltage(1.0), float)

        # Test array input returns array
        array_input = np.array([1.0, 2.0], dtype=np.float64)
        assert isinstance(limited_sensor.convert_voltage(array_input), np.ndarray)

    def test_zero_gain(self):
        """Test voltage conversion with zero gain."""
        sensor = LinearLimitedSensor(
            v_min=0.0, v_max=2.0, model_name="ZeroGainSensor", gain=0.0, offset=1.0
        )
        assert sensor.convert_voltage(-1.0) == 1.0  # Should just return offset
        assert sensor.convert_voltage(3.0) == 1.0  # Should just return offset


# Assuming AnalogSensorInterface has a model_name property
def test_inheritance():
    """Test inheritance."""
    sensor = LinearSensor(model_name="Test", gain=1.0)
    limited_sensor = LinearLimitedSensor(
        v_min=0.0, v_max=1.0, model_name="TestLimited", gain=1.0
    )
    assert hasattr(sensor, "model_name")
    assert hasattr(limited_sensor, "model_name")


if __name__ == "__main__":
    pytest.main()
