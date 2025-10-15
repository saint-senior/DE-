import paho.mqtt.client as mqtt
from paho.mqtt.client import CallbackAPIVersion
import logging
logger = logging.getLogger(__name__)

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
        # self.mqttc.on_subscribe = self.on_subscribe
        # self.mqttc.on_unsubscribe = self.on_unsubscribe
        # self.mqttc.on_publish = self.on_publish
        self.subscribers = []
        self.mqttc.connect(broker, port, keepalive)
        self.mqttc.loop_start()
        logger.info("MQTT client initialized and loop started.")

    def on_connect(self, client, _userdata, _flags, reason_code, _properties):
        if reason_code == 0:
            print(f"Connected with result code {reason_code}")
            client.subscribe("device/telemetry/heartrate")
        else:
            print(f"Failed to connect, return code {reason_code}")
        
    def on_disconnect(self, client, _userdata, _flags, reason_code, _properties):
        try:
            client.reconnect()
        except Exception as e:
            print(f"Reconnection failed: {e}")
        print(f"Disconnected with result code {reason_code}")

    # The callback for when a PUBLISH message is received from the server.
    def on_message(self, client, _userdata, msg):
        print(msg.topic+" "+str(msg.payload))
        # Parsing the message payload (likely JSON).
        # Storing the data in the database.
        # Checking for predefined conditions (e.g., high heart rate).
        # Publishing new messages in response (e.g., notifying the smartwatch).

    def subscribe(self, event):
        self.subscribers.append(event)
        # if not in there, add it
        self.mqttc.subscribe(event)
        print(f"Subscribed to event: {event}")

    def publish(self, event, message = ""):
        self.mqttc.publish(event, message)
        print(f"Published message to event: {event} with message: {message}")


    # def on_subscribe(self, client, _userdata, mid, granted_qos, _properties):
    #     print(f"Subscribed: {mid} {granted_qos}")

    # def on_publish(self, client, userdata, mid):
    #     print(f"Message {mid} published.")

    # def on_unsubscribe(self, client, userdata, mid):
    #     print(f"Unsubscribed: {mid}")
    #     client.disconnect()

    # def loop_start():
    #   pass