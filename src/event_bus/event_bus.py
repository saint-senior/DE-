import paho.mqtt.client as mqtt
from paho.mqtt.client import CallbackAPIVersion

class Event_Bus:
    def __init__(self, server=None):
        # Create MQTT client with the new API version
        self.mqttc = mqtt.Client(
            callback_api_version=CallbackAPIVersion.VERSION2,
            client_id="Python"
        )
        self.mqttc.connect("broker.emqx.io", 1883)
        self.mqttc.loop_start()
        self.mqttc.subscribers = {}
    

    

