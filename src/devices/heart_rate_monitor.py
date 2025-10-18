import random
from time import sleep

class HeartRateMonitor:
    def __init__(self, bus):
        self.bus = bus

    def read_heart_rate(self):
        """Simulates reading a heart rate value from a sensor."""
        sleep(1)
        reading = random.randint(60, 120)
        self.bus.publish("wearables/heart_rate/data", str(reading))
        return reading
