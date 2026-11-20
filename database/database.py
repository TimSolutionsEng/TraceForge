
from pathlib import Path
import sqlite3
import hashlib

# Find the root directory of TraceForge
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Define where our database will be stored
DATA_DIR = PROJECT_ROOT / "data"
DB_PATH = DATA_DIR / "traceforge.db"


def get_connection():
    # Create the data folder if it doesn't exist
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    # Connect to the SQLite database
    connection = sqlite3.connect(DB_PATH)

    return connection


def init_db():
    connection = get_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_key TEXT NOT NULL UNIQUE,
            timestamp TEXT NOT NULL,
            hostname TEXT,
            process TEXT,
            pid INTEGER,
            event_type TEXT NOT NULL,
            username TEXT,
            source_ip TEXT,
            port INTEGER,
            raw TEXT NOT NULL
        )
    """)
    connection.execute("""
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            alert_key TEXT NOT NULL UNIQUE,
            alert_type TEXT NOT NULL,
            source_ip TEXT NOT NULL,
            failed_attempts INTEGER NOT NULL,
            severity TEXT NOT NULL,
            description TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()

    print("Events and alerts tables created successfully!")


def save_events(events):
    connection = get_connection()
    inserted = 0

    try:
        for event in events:
            event_key = hashlib.sha256(
                event["raw"].encode("utf-8")
            ).hexdigest()

            cursor = connection.execute("""
                INSERT OR IGNORE INTO events (
                    event_key, timestamp, hostname, process,
                    pid, event_type, username, source_ip,
                    port, raw
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                event_key,
                event["timestamp"],
                event["hostname"],
                event["process"],
                event["pid"],
                event["event_type"],
                event["username"],
                event["source_ip"],
                event["port"],
                event["raw"]
            ))

            if cursor.rowcount == 1:
                inserted += 1

        connection.commit()
        return inserted
    

    finally:
        connection.close()


def save_alerts(alerts):
    connection = get_connection()
    inserted = 0

    try:
        for alert in alerts:

            alert_key = hashlib.sha256(
                (
                    alert["alert_type"]
                    + alert["source_ip"]
                    + str(alert["failed_attempts"])
                    + alert["severity"]
                    + alert["description"]
                ).encode("utf-8")
            ).hexdigest()

            cursor = connection.execute("""
                INSERT OR IGNORE INTO alerts (
                    alert_key,
                    alert_type,
                    source_ip,
                    failed_attempts,
                    severity,
                    description
                )
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                alert_key,
                alert["alert_type"],
                alert["source_ip"],
                alert["failed_attempts"],
                alert["severity"],
                alert["description"]
            ))

            if cursor.rowcount == 1:
                inserted += 1

        connection.commit()
        return inserted

    finally:
        connection.close()
