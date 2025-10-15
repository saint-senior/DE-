import random
from time import sleep
from event_bus.event_bus import Event_Bus

class BloodPressureDevice(Event_Bus):
    def read_blood_pressure(self, message):
        """Simulates reading a blood pressure value from a sensor."""
        sleep(1)
        # Return a random systolic/diastolic pair, a more realistic range
        # if a high hr, does that mean high bp
        systolic = random.randint(90, 140)
        diastolic = random.randint(60, 90)
        self.subscribe("wearables/heart_rate/data/")
        if message == "Warning: High Blood Pressure":
            self.subscribe(f"wearables/blood_pressure/data/{systolic}/{diastolic}")
            return (systolic, diastolic)
        else:
            pass

# The sensor object is an instance of the class
bp_device = BloodPressureDevice()

