import random
from time import sleep
from event_bus.event_bus import Event_Bus

class Smartwatch(Event_Bus):
    def trigger_alert(self, reading):
        """Simulates reading a heart rate value from a sensor."""
        sleep(1)
        if reading > 80:
            self.subscribe("wearables/heart_rate/alert")
            self.publish("wearables/smartwatch/notification", "Warning: High Blood Pressure")
            return self.on_message
        # log warning

# The sensor object is an instance of the class
alert = Smartwatch()



