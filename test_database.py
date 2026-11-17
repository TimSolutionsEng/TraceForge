
from database.database import init_db, get_connection, save_events

# Initialise the database
init_db()

# Create a sample security event
sample_events = [
    {
        "timestamp": "Nov 17 13:20:00",
        "hostname": "traceforge-lab",
        "process": "sshd",
        "pid": 1016,
        "event_type": "login_failed",
        "username": "admin",
        "source_ip": "192.168.1.20",
        "port": 52216,
        "raw": "Nov 17 13:20:00 traceforge-lab sshd[1016]: Failed password for admin from 192.168.1.20 port 52216 ssh2"
    }
]

# Save the event
inserted = save_events(sample_events)

print("New events inserted:", inserted)

# Check the database
connection = get_connection()

records = connection.execute("""
    SELECT id, event_type, username, source_ip
    FROM events
""").fetchall()

print("Stored events:", records)

connection.close()
