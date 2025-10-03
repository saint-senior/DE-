import pytest
from unittest.mock import Mock, MagicMock, patch, call
from src.event_bus.event_bus import Event_Bus


# Fixtures
@pytest.fixture
def mock_mqtt_client():
    """Mock MQTT client to avoid real network connections"""
    with patch('src.event_bus.event_bus.mqtt.Client') as mock_client:
        mock_instance = MagicMock()
        mock_client.return_value = mock_instance
        yield mock_instance


@pytest.fixture
def event_bus(mock_mqtt_client):
    """Create Event_Bus instance with mocked MQTT client"""
    return Event_Bus()


