import pytest
from unittest.mock import Mock, MagicMock, patch, call
from event_bus.event_bus import Event_Bus, mqtt

# __innit__ logic
@patch('event_bus.event_bus.mqtt.Client')
def test_event_bus_can_be_instantiated(mock_mqtt_client):
    eb = Event_Bus()
    assert eb is not None


def test_event_bus_is_correct_type():
    patcher = patch('event_bus.event_bus.mqtt.Client')
    patcher.start()
    eb = Event_Bus()
    assert isinstance(eb, Event_Bus)
    patcher.stop()

# __innit__ connection

@patch('event_bus.event_bus.mqtt.Client')
def test_event_bus_initializes_mqtt_client_correctly(mock_mqtt_client):
    eb = Event_Bus()

    mock_mqtt_client.return_value.loop_start.assert_called_once()
    assert eb.mqttc.connect.call_count == 1

# __innit__ function
@patch('event_bus.event_bus.mqtt.Client')
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

def test_event_bus_on_connect_success(mocker):
    eb = Event_Bus()
    mock_client = MagicMock()
    mock_print = mocker.patch("builtins.print")

    eb.on_connect(mock_client, None, None, 0, None)

    mock_client.subscribe.assert_any_call("wearables/heart_rate/data")
    mock_client.subscribe.assert_any_call("wearables/smartwatch/notification")
    mock_print.assert_any_call("Connected to MQTT broker")
    mock_print.assert_any_call("Subscribed to telemetry topics")

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
@patch('event_bus.event_bus.mqtt.Client')
def test_event_bus_on_message_empty(mock_mqtt_client):
    eb = Event_Bus()
    
    mock_client_instance = mock_mqtt_client.return_value
    
    mock_msg = MagicMock()
    mock_msg.topic = ""
    mock_msg.payload.decode() == ""

    assert eb.on_message(mock_client_instance, None, mock_msg) == None


@patch('event_bus.event_bus.mqtt.Client')
def test_event_bus_on_message_called_single(mock_mqtt_client):
    eb = Event_Bus()
    
    mock_client_instance = mock_mqtt_client.return_value
    
    mock_msg = MagicMock()
    mock_msg.topic = "test/topic"
    mock_msg.payload = b"test payload"

    with patch.object(eb, "on_message") as mock_on_message:
        # Call the method under test.
        eb.on_message(mock_client_instance, None, mock_msg)
        
        mock_on_message.assert_called_once()
        mock_on_message.assert_called_with(mock_client_instance, None, mock_msg)


def test_event_bus_on_message_called_multiple():
    eb = Event_Bus()
    
    mock_client_instance = MagicMock()
    
    mock_msg_1 = MagicMock()
    mock_msg_1.topic = "test/topic"
    mock_msg_1.payload = b"test payload 1" # Different payload to distinguish calls

    mock_msg_2 = MagicMock()
    mock_msg_2.topic = "test/topic"
    mock_msg_2.payload = b"test payload 2" # Different payload

    with patch.object(eb, "on_message") as mock_on_message:
        # Call the method under test with the mock messages.
        eb.on_message(mock_client_instance, None, mock_msg_1)
        eb.on_message(mock_client_instance, None, mock_msg_2)

        expected_calls = [
            call(mock_client_instance, None, mock_msg_1),
            call(mock_client_instance, None, mock_msg_2)
        ]
        
        mock_on_message.assert_has_calls(expected_calls)

@patch("event_bus.event_bus.close_db_connection")
@patch("event_bus.event_bus.connect_to_db")
def test_on_message_numeric_data(mock_connect, mock_close):

    mock_conn = Mock()
    mock_connect.return_value = mock_conn

    eb = Event_Bus()
    mock_msg = MagicMock()
    mock_msg.topic = "wearables/heart_rate/data"
    mock_msg.payload = b"110"  # triggers high HR alert

    eb.on_message(None, None, mock_msg)

    assert mock_conn.run.call_count >= 2

    sql_calls = [args[0] for args, _ in mock_conn.run.call_args_list]
    assert any("INSERT INTO Historical_Data" in sql for sql in sql_calls)
    assert any("INSERT INTO Events" in sql for sql in sql_calls)

    mock_close.assert_called_once()


@patch("event_bus.event_bus.connect_to_db")
@patch("event_bus.event_bus.close_db_connection")
def test_on_message_notification_skipped(mock_close, mock_connect):

    mock_conn = Mock()
    mock_connect.return_value = mock_conn

    eb = Event_Bus()
    mock_msg = MagicMock()
    mock_msg.topic = "wearables/smartwatch/notification"
    mock_msg.payload = b"Warning: High Heart Rate"

    eb.on_message(None, None, mock_msg)

    sql_calls = [c[0][0] for c in mock_conn.run.call_args_list]
    assert not any("Historical_Data" in sql for sql in sql_calls)
    mock_close.assert_called_once()


@patch("event_bus.event_bus.connect_to_db")
@patch("event_bus.event_bus.close_db_connection")
def test_on_message_handles_invalid_data(mock_close, mock_connect):
    mock_conn = Mock()
    mock_connect.return_value = mock_conn

    eb = Event_Bus()
    mock_msg = MagicMock()
    mock_msg.topic = "wearables/heart_rate/data"
    mock_msg.payload = b"not_a_number"

    eb.on_message(None, None, mock_msg)

    sql_calls = [c[0][0] for c in mock_conn.run.call_args_list]
    assert any("INSERT INTO Historical_Data" in sql for sql in sql_calls)
    assert not any("ALERT" in str(call) for call in sql_calls)
    mock_close.assert_called_once()

@patch('event_bus.event_bus.mqtt.Client')
def test_event_bus_subscribe_event(mock_mqtt_client):
    topic = "Hello"
    eb = Event_Bus()
    eb.subscribe(topic)
    assert len(eb.subscribers) > 0
    assert topic in eb.subscribers

@patch('event_bus.event_bus.mqtt.Client')
def test_event_bus_publish_event(mock_mqtt_client):
    message = "Hello"
    eb = Event_Bus()

    with patch.object(eb.mqttc, "publish") as mock_publish:
        eb.publish("test/topic", message)
        mock_publish.assert_called_once_with("test/topic", message)

    with patch("builtins.print") as mock_print:
        eb.publish("test/topic", message)
        mock_print.assert_any_call(
            f"Published message to event: test/topic with message: {message}"
        )