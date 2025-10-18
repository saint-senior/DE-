# Health Devices Monitoring System

This project simulates a network of wearable health devices and monitors their data in real time. Devices include heart rate monitors, smartwatches, and blood pressure monitors. The system demonstrates how devices communicate via an Event Bus and store historical readings and events in a PostgreSQL database. It is designed for educational purposes, testing event-driven architectures, and practicing database interactions in Python.

---

## Features

- **Heart Rate Monitor**: Generates random heart rate readings to simulate a real sensor.  
- **Smartwatch**: Monitors heart rate data and sends alerts when thresholds are exceeded.  
- **Blood Pressure Device**: Publishes blood pressure readings if a smartwatch alert is triggered.  
- **Database Logging**: Stores device data and events in PostgreSQL tables (`Devices`, `Historical_Data`, `Events`).  
- **Event Bus**: Simulates communication between devices (mocked in tests).  

---

## Requirements

- Python 3.12+  
- PostgreSQL 14+  
- Python dependencies listed in `requirements.txt`  

---

## Setup

1. Clone the repository:

    ```bash
    git clone <repo-url>
    cd <repo-folder>

2. Create a .env file for database connection credentials:
    
    ```bash
    DB_HOST=localhost
    DB_PORT=5432
    DB_NAME=health_devices
    DB_USER=your_user
    DB_PASSWORD=your_password

3. Install Python dependencies:

    ```bash
    pip install -r requirements.txt

4. Set up PostgreSQL database:

    ```bash
    sudo -u postgres psql

    Then run the setup SQL script:

    ```bash
    \i src/db/setup-db.sql

5. Verify database tables:

    ```bash
    \c health_devices
    SELECT * FROM devices;
    SELECT * FROM historical_data ORDER BY timestamp DESC LIMIT 10;
    SELECT * FROM events ORDER BY id DESC LIMIT 10;

---

Usage

Run the main program:

python main.py

The program will:

1. Generate simulated heart rate readings.
2. Trigger smartwatch alerts if readings exceed thresholds.
3. Trigger blood pressure measurements when alerts occur.
4. Log all events and readings into PostgreSQL tables.
5. Write messages to the application log for auditing.

---

Database Schema Overview

Tables:

- Devices: Stores information about each device (ID, type, status).
- Historical_Data: Stores sensor readings (timestamp, device_id, reading values).
- Events: Stores event logs (event type, device, timestamp, details).

Example Queries:

-- Last 10 heart rate readings
```bash
SELECT * FROM historical_data WHERE device_type='heart_rate_monitor' ORDER BY timestamp DESC LIMIT 10;

-- Recent events
```bash
SELECT * FROM events ORDER BY id DESC LIMIT 10;


References

- PostgreSQL Documentation: https://www.postgresql.org/docs/
- Python psycopg2 library: https://www.psycopg.org/
- Event-driven architecture concepts: https://martinfowler.com/articles/201701-event-driven.html
- Logging in Python: https://docs.python.org/3/library/logging.html