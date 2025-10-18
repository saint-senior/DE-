import paho.mqtt.client as mqtt
from paho.mqtt.client import CallbackAPIVersion
from src.utils.connection import connect_to_db, close_db_connection
import datetime as dt
import logging
logger = logging.getLogger(__name__)

CURRENT_TIMESTAMP = dt.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')

class Event_Bus:
    def __init__(self, broker="broker.emqx.io", port=1883, keepalive=60):
        # Create MQTT client with the new API version
        self.mqttc = mqtt.Client(
            callback_api_version=CallbackAPIVersion.VERSION2,
            client_id="Python"  
        )
        self.mqttc.on_connect = self.on_connect
        self.mqttc.on_message = self.on_message
        self.mqttc.on_disconnect = self.on_disconnect  
        self.subscribers = []
        self.mqttc.connect(broker, port, keepalive)
        self.mqttc.loop_start()
        logger.info("MQTT client initialized and loop started.")

    def on_connect(self, client, _userdata, _flags, reason_code, _properties):
        if reason_code == 0:
            print("Connected to MQTT broker")
            logger.info("Connected to MQTT broker")
            client.subscribe("wearables/heart_rate/data")
            client.subscribe("wearables/smartwatch/notification")
            client.subscribe("wearables/blood_pressure/data/")
            logger.info("Subscribed to telemetry topics")
            print("Subscribed to telemetry topics")
        else:
            logger.error(f"Failed to connect to MQTT broker, return code {reason_code}")
            print(f"Failed to connect, return code {reason_code}")

    def on_disconnect(self, client, _userdata, _flags, reason_code, _properties):
        try:
            client.reconnect()
        except Exception as e:
            logger.error(f"Reconnection failed: {e}")
            print(f"Reconnection failed: {e}")
        logger.info(f"Disconnected from MQTT broker with result code {reason_code}")
        print(f"Disconnected with result code {reason_code}")

    def on_message(self, client, _userdata, msg):
        logger.info(f"Message received | {msg.topic} → {msg.payload.decode()}")
        print(f"Message received | {msg.topic} → {msg.payload.decode()}")
        conn = connect_to_db()

        timestamp = dt.datetime.now()

        try:
            # Map topics to device info
            topic_map = {
                "wearables/heart_rate/data": 1,
                "wearables/smartwatch/notification": 2,
                "wearables/blood_pressure/data": 3
            }

            device_id = None
            for prefix, dev_id in topic_map.items():
                if msg.topic.startswith(prefix):
                    device_id = dev_id
                    break

            if device_id is None:
                print(f"Unknown topic: {msg.topic}")
                return

            payload = msg.payload.decode()

            if msg.topic.startswith("wearables/heart_rate/data") or msg.topic.startswith("wearables/blood_pressure/data"):
                conn.run(
                    """
                    INSERT INTO Historical_Data (device_id, reading, timestamp, type, status)
                    VALUES (:device_id, :reading, :timestamp, :type, :status)
                    """,
                    device_id=device_id,
                    reading=payload,
                    timestamp=timestamp,
                    type=msg.topic.split("/")[1],
                    status="active"
                )
                logger.info("Stored numeric telemetry in Historical_Data")
                print("Stored numeric telemetry in Historical_Data")
            else:
                logger.warning(f"Skipping Historical_Data insert for non-numeric topic: {msg.topic}")
                print(f"Skipping Historical_Data insert for non-numeric topic: {msg.topic}")

            # Check if the message represents an alert condition
            if msg.topic == "wearables/heart_rate/data":
                try:
                    hr_value = int(msg.payload.decode())
                    if hr_value > 100:
                        conn.run(
                            """
                            INSERT INTO Events (event_type, source_id, target_id, payload, timestamp)
                            VALUES (:event_type, :source_id, :target_id, :payload, :timestamp)
                            """,
                            event_type="ALERT",
                            source_id=1,  # Heart Rate Monitor
                            target_id=2,  # Smartwatch
                            payload=f"High Heart Rate: {hr_value}",
                            timestamp=timestamp
                        )
                        print("Alert inserted into Events table.")
                except ValueError:
                    print("Could not parse heart rate value as integer.")

            if msg.topic.startswith("wearables/blood_pressure/data"):
                conn.run(
                    """
                    INSERT INTO Events (event_type, source_id, target_id, payload, timestamp)
                    VALUES (:event_type, :source_id, :target_id, :payload, :timestamp)
                    """,
                    event_type="READING",
                    source_id=3,
                    target_id=2,
                    payload=msg.payload.decode(),
                    timestamp=timestamp
                )
                logger.info("Blood pressure reading logged in Events table.")
                print("Blood pressure reading logged in Events table.")

            logger.info("Data stored successfully.")
            print("Data stored successfully.")
        except Exception as e:
            logger.error(f"Error inserting data: {e}")
            print(f"Error inserting data: {e}")
        finally:
            close_db_connection(conn)

    def subscribe(self, event):
        self.subscribers.append(event)
        # if not in there, add it
        self.mqttc.subscribe(event)
        logger.info(f"Subscribed to event: {event}")
        print(f"Subscribed to event: {event}")

    def publish(self, event, message = ""):
        self.mqttc.publish(event, message)
        logger.info(f"Published message to event: {event} with message: {message}")
        print(f"Published message to event: {event} with message: {message}")

