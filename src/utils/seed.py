from src.utils.connection import connect_to_db, close_db_connection
import json


def seed():
    conn = connect_to_db()

    try:
        conn.run("""
            CREATE TABLE IF NOT EXISTS Events (
                id SERIAL PRIMARY KEY,
                event_type VARCHAR(40),
                source_id INT,
                target_id INT,
                payload TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        conn.run(
            "CREATE TABLE IF NOT EXISTS Devices (\
                device_id SERIAL PRIMARY KEY,\
                type VARCHAR(40) NOT NULL,\
                status VARCHAR(40),\
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP\
            );"
        )
        conn.run(
            "CREATE TABLE IF NOT EXISTS Historical_Data (\
                id SERIAL PRIMARY KEY,\
                device_id INT NOT NULL REFERENCES Devices(device_id),\
                reading INT,\
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,\
                type VARCHAR(40) NOT NULL,\
                status VARCHAR(40)\
            );"
        )

        result = list(conn.run("SELECT COUNT(*) FROM Devices;"))
        if result[0][0] > 0:
            print("Devices table already seeded. Exiting seeding process.")
            return
        
        devices_path = "src/data/device_details.json"
        with open(devices_path, "r") as file:
            data = json.load(file)
            devices = data["devices"]
        for row in devices:
            conn.run(
                "INSERT INTO Devices (device_id, type, status) VALUES (:device_id, :type, :status)",
                device_id=row["device_id"],
                type=row["type"],
                status=row["status"]
            )

    finally:
        print("Seeding Complete.")
        close_db_connection(conn)

seed()