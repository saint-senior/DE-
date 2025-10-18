import logging
import datetime as dt
import os
from src.devices.heart_rate_monitor import HeartRateMonitor
from src.devices.smartwatch_alerts import Smartwatch
from src.devices.blood_pressure_device import BloodPressureDevice
from src.utils.seed import seed
from event_bus.event_bus import Event_Bus

# Logging Configuration
os.makedirs("src/data/logs", exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler(
            f"src/data/logs/system_{dt.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"
        ),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Main Run
def run():
    logger.info("Application starting up.")
    seed()

    # One shared Event Bus
    bus = Event_Bus()

    # Create device instances with shared bus
    hrm_sensor = HeartRateMonitor(bus)
    alert = Smartwatch(bus)
    bp_device = BloodPressureDevice(bus)

    # Simulate heart rate sensor reading
    hr_reading = hrm_sensor.read_heart_rate()
    logger.info(f"Heart rate reading: {hr_reading}")

    # Trigger smartwatch alert if needed
    msg = alert.trigger_alert(hr_reading)
    logger.info(f"Smartwatch alert message: {msg}")

    # Simulate blood pressure reading
    bp_device.read_blood_pressure(msg)
    logger.info("Blood pressure reading complete.")

    logger.info("Data flow complete — check your database for updates!")

if __name__ == "__main__":
    run()
