import random
from time import sleep
from event_bus.event_bus import Event_Bus

class HeartRateMonitor(Event_Bus):
    def read_heart_rate(self):

        """Simulates reading a heart rate value from a sensor."""
        sleep(1)
        # Return a random integer between 60 and 120, a more realistic range
        self.publish("wearables/heart_rate/alert", str(random.randint(60, 120)))
        return random.randint(60, 120)

# The sensor object is an instance of the class
hrm_sensor = HeartRateMonitor()
