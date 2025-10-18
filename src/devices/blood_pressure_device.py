import random
from time import sleep

class BloodPressureDevice:
    def __init__(self, bus):
        self.bus = bus

    def read_blood_pressure(self, message):
        """Simulates reading a blood pressure value."""
        sleep(1)
        systolic = random.randint(90, 140)
        diastolic = random.randint(60, 90)
        self.bus.subscribe("wearables/heart_rate/data")
        if message == "Warning: High Heart Rate":
            topic = f"wearables/blood_pressure/data/{systolic}/{diastolic}"
            self.bus.publish(topic, f"{systolic}/{diastolic}")
            return (systolic, diastolic)
        return None
