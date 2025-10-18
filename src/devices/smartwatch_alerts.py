from time import sleep

class Smartwatch:
    def __init__(self, bus):
        self.bus = bus

    def trigger_alert(self, reading):
        """Simulates sending a warning if heart rate exceeds threshold."""
        sleep(1)
        if reading > 80:
            self.bus.subscribe("wearables/heart_rate/data")
            self.bus.publish("wearables/smartwatch/notification", "Warning: High Heart Rate")
            return "Warning: High Heart Rate"
        return "Normal Heart Rate"
