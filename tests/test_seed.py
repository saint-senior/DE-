import pytest
from src.utils.connection import connect_to_db, close_db_connection
from src.utils.seed import seed

def test_seed_devices():
    conn = connect_to_db()
    seed()
    result = list(conn.run("SELECT COUNT(*) FROM Devices;"))
    assert result[0][0] > 0