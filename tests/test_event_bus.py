import pytest
from unittest.mock import Mock, MagicMock, patch, call
from src.event_bus.event_bus import Event_Bus, mqtt

# __innit__ logic
@patch('src.event_bus.event_bus.mqtt.Client')
def test_event_bus_can_be_instantiated(mock_mqtt_client):
    """Test that we can create an Event_Bus instance without errors"""
    eb = Event_Bus()
    assert eb is not None


def test_event_bus_is_correct_type():
    """Test that Event_Bus instance is of type Event_Bus"""
    patcher = patch('src.event_bus.event_bus.mqtt.Client')
    patcher.start()
    eb = Event_Bus()
    assert isinstance(eb, Event_Bus)
    patcher.stop()

# __innit__ connection

@patch('src.event_bus.event_bus.mqtt.Client')
def test_event_bus_initializes_mqtt_client_correctly(mock_mqtt_client):
    """Test that the Event_Bus creates and starts the MQTT client."""
    eb = Event_Bus()

    mock_mqtt_client.return_value.loop_start.assert_called_once()
    assert eb.mqttc.connect.call_count == 1

# __innit__ function
@patch('src.event_bus.event_bus.mqtt.Client')
def test_event_bus_returns_subscribers_list(mock_mqtt_client):
    eb = Event_Bus()
    assert len(eb.subscribers) == 0
    print(eb.subscribers)
    assert eb.subscribers == []
    assert isinstance(eb.subscribers, list)

# on_connect 
def test_event_bus_on_connect_fail():
    eb = Event_Bus()
    mock_client = MagicMock()
    rc = 1
    with patch("builtins.print") as mock_print:
        eb.on_connect(mock_client, None, None, rc, None)
        mock_client.subscribe.assert_not_called()
        mock_print.assert_called_with(f"Failed to connect, return code {rc}")

def test_event_bus_on_connect_called(mocker):
    """Test that the on_connect callback successfully subscribes and prints."""
    
    # Arrange
    # Use mocker to patch mqtt.Client and builtins.print
    mock_mqtt_client_cls = mocker.patch('src.event_bus.event_bus.mqtt.Client')
    mock_print = mocker.patch("builtins.print")
    
    eb = Event_Bus()
    
    # Get a mock instance of the mqtt.Client class
    mock_client_instance = mock_mqtt_client_cls.return_value

    # Act
    # Simulate a successful connection event
    eb.on_connect(mock_client_instance, None, None, 0, None)

    # Assert
    # Check that the subscribe method was called on the mock client instance
    mock_client_instance.subscribe.assert_called_with("device/telemetry/heartrate")
    
    # Check that the built-in print function was called correctly
    mock_print.assert_called_with("Connected with result code 0")

# on_disconnect
def test_event_bus_on_disconnect_fail():
    eb = Event_Bus()
    mock_client = MagicMock()
    reason_code = 1
    with patch("builtins.print") as mock_print:
        eb.on_disconnect(mock_client, None, None, reason_code, None)
        mock_print.assert_called_with(f"Disconnected with result code {reason_code}")

def test_event_bus_on_disconnect_raise_error():
    eb = Event_Bus()
    mock_client = MagicMock()
    mock_client.reconnect.side_effect = Exception("Reconnection attempt failed.")
    with patch("builtins.print") as mock_print:
        eb.on_disconnect(mock_client, None, None, None, None)
        mock_print.assert_any_call("Reconnection failed: Reconnection attempt failed.")

# on_message
@patch('src.event_bus.event_bus.mqtt.Client')
def test_event_bus_on_message_empty(mock_mqtt_client):
    """Test that the on_message callback is set and can be called with correct arguments."""
    eb = Event_Bus()
    
    # Create a mock for the client instance, which is an argument to on_message.
    mock_client_instance = mock_mqtt_client.return_value
    
    # Create a mock message object.
    mock_msg = MagicMock()
    mock_msg.topic = ""
    mock_msg.payload = ""

    assert eb.on_message(mock_client_instance, None, mock_msg) == None


@patch('src.event_bus.event_bus.mqtt.Client')
def test_event_bus_on_message_called_single(mock_mqtt_client):
    """Test that the on_message callback is set and can be called with correct arguments."""
    eb = Event_Bus()
    
    # Create a mock for the client instance, which is an argument to on_message.
    mock_client_instance = mock_mqtt_client.return_value
    
    # Create a mock message object.
    mock_msg = MagicMock()
    mock_msg.topic = "test/topic"
    mock_msg.payload = b"test payload"

    # Patch the on_message method of the specific Event_Bus instance.
    with patch.object(eb, "on_message") as mock_on_message:
        # Call the method under test.
        eb.on_message(mock_client_instance, None, mock_msg)
        
        mock_on_message.assert_called_once()
        # Assert that the mocked method was called with the correct *mock* arguments.
        mock_on_message.assert_called_with(mock_client_instance, None, mock_msg)


def test_event_bus_on_message_called_multiple():
    """Test that on_message is called correctly with multiple messages."""
    eb = Event_Bus()
    
    # Create a mock for the client instance, which is an argument to on_message.
    mock_client_instance = MagicMock()
    
    # Create mock message objects.
    mock_msg_1 = MagicMock()
    mock_msg_1.topic = "test/topic"
    mock_msg_1.payload = b"test payload 1" # Different payload to distinguish calls

    mock_msg_2 = MagicMock()
    mock_msg_2.topic = "test/topic"
    mock_msg_2.payload = b"test payload 2" # Different payload

    # Patch the on_message method of the specific Event_Bus instance.
    with patch.object(eb, "on_message") as mock_on_message:
        # Call the method under test with the mock messages.
        eb.on_message(mock_client_instance, None, mock_msg_1)
        eb.on_message(mock_client_instance, None, mock_msg_2)

        # Create a list of 'call' objects representing the expected calls.
        expected_calls = [
            call(mock_client_instance, None, mock_msg_1),
            call(mock_client_instance, None, mock_msg_2)
        ]
        
        # Assert that the mocked method was called with the correct arguments and order.
        mock_on_message.assert_has_calls(expected_calls)


# @patch('src.event_bus.event_bus.mqtt.Client')
# def test_event_bus_subscribe_event(mock_mqtt_client):
#     topic = "Hello"
#     eb = Event_Bus()
#     eb.subscribe(topic)
#     eb.subscribe.return_value.assert_called_once_with(topic)

    

    
    

