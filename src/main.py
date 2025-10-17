import logging
import datetime as dt
import os
from devices.heart_rate_monitor import HeartRateMonitor
from devices.smartwatch_alerts import alert
from devices.blood_pressure_device import bp_device

from src.event_bus.event_bus import Event_Bus

os.makedirs("data/logs", exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler(f"src/data/logs/system_{dt.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')}.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def run():
    logger.info("Application starting up.")
    # Example logging message
    # hr = Event_Bus.publish("wearables/heart_rate/data", str(hrm_sensor.read_heart_rate()), hostname="mqtt.eclipseprojects.io")
    # hr = HeartRateMonitor()
    # hr.read_heart_rate()
    # logger.info(f"Published heart rate data. Subscribers: {hr.subscribers}")
    msg = alert.trigger_alert(90)
    bp_device.read_blood_pressure(msg)   
    logger.info(f"Published blood pressure data. Subscribers: {bp_device.subscribers}")

# get variables
# insert into device_details
# devices.append({"device_id": 1, "type": "sensor", "status": "active", "user_id": "user_1"})
# historical_data.append({"device_id": 1, "reading": 23, "timestamp": "2023-01-01T00:00:00Z", "type": "sensor", "status": "active", "user_id": "user_1"})

if __name__ == "__main__":
    run()