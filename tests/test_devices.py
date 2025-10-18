import pytest
from unittest.mock import MagicMock, patch
from src.devices.heart_rate_monitor import HeartRateMonitor
from src.devices.smartwatch_alerts import Smartwatch
from src.devices.blood_pressure_device import BloodPressureDevice

@pytest.fixture
def mock_bus():
    bus = MagicMock()
    bus.publish = MagicMock()
    bus.subscribe = MagicMock()
    return bus

@patch("time.sleep", return_value=None)
def test_heart_rate_publishes(mock_sleep, mock_bus):
    device = HeartRateMonitor(mock_bus)
    reading = device.read_heart_rate()
    mock_bus.publish.assert_called_once()
    assert 60 <= reading <= 120


@patch("random.randint", return_value=100)
@patch("time.sleep", return_value=None)
def test_heart_rate_monitor_publishes(mock_sleep, mock_randint, mock_bus):
    device = HeartRateMonitor(mock_bus)
    reading = device.read_heart_rate()
    mock_bus.publish.assert_called_once_with("wearables/heart_rate/data", "100")
    assert reading == 100


@patch("time.sleep", return_value=None)
def test_smartwatch_triggers_alert(mock_sleep, mock_bus):
    device = Smartwatch(mock_bus)
    result = device.trigger_alert(90)
    mock_bus.publish.assert_called_once_with(
        "wearables/smartwatch/notification",
        "Warning: High Heart Rate"
    )
    assert result == "Warning: High Heart Rate"


@patch("time.sleep", return_value=None)
def test_smartwatch_no_alert(mock_sleep, mock_bus):
    device = Smartwatch(mock_bus)
    result = device.trigger_alert(70)
    mock_bus.publish.assert_not_called()
    assert result == "Normal Heart Rate"


@patch("random.randint", side_effect=[120, 80])
@patch("time.sleep", return_value=None)
def test_blood_pressure_device_publishes_on_warning(mock_sleep, mock_randint, mock_bus):
    device = BloodPressureDevice(mock_bus)
    result = device.read_blood_pressure("Warning: High Heart Rate")
    systolic, diastolic = result
    topic = f"wearables/blood_pressure/data/{systolic}/{diastolic}"
    mock_bus.publish.assert_called_once_with(topic, f"{systolic}/{diastolic}")
    assert isinstance(systolic, int)
    assert isinstance(diastolic, int)