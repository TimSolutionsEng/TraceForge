
import sqlite3

import database.database as database_module


def create_sample_event():
    return {
        "timestamp": "Nov 17 13:20:00",
        "hostname": "traceforge-lab",
        "process": "sshd",
        "pid": 1016,
        "event_type": "login_failed",
        "username": "admin",
        "source_ip": "192.168.1.20",
        "port": 52216,
        "raw": (
            "Nov 17 13:20:00 traceforge-lab sshd[1016]: "
            "Failed password for admin from "
            "192.168.1.20 port 52216 ssh2"
        )
    }


def setup_test_database(tmp_path, monkeypatch):
    monkeypatch.setattr(database_module, "DATA_DIR", tmp_path)
    monkeypatch.setattr(
        database_module, "DB_PATH", tmp_path / "test.db"
    )


def test_init_db_creates_events_table(tmp_path, monkeypatch):
    setup_test_database(tmp_path, monkeypatch)

    database_module.init_db()

    connection = database_module.get_connection()

    tables = connection.execute("""
        SELECT name FROM sqlite_master
        WHERE type='table' AND name='events'
    """).fetchall()

    connection.close()

    assert len(tables) == 1


def test_save_events_inserts_event(tmp_path, monkeypatch):
    setup_test_database(tmp_path, monkeypatch)

    database_module.init_db()

    event = create_sample_event()
    inserted = database_module.save_events([event])

    assert inserted == 1


def test_save_events_prevents_duplicates(tmp_path, monkeypatch):
    setup_test_database(tmp_path, monkeypatch)

    database_module.init_db()

    event = create_sample_event()

    first_insert = database_module.save_events([event])
    second_insert = database_module.save_events([event])

    assert first_insert == 1
    assert second_insert == 0


def test_save_multiple_events(tmp_path, monkeypatch):
    setup_test_database(tmp_path, monkeypatch)

    database_module.init_db()

    event1 = create_sample_event()

    event2 = create_sample_event()
    event2["pid"] = 1017
    event2["username"] = "root"
    event2["raw"] = event2["raw"].replace("sshd[1016]", "sshd[1017]")

    inserted = database_module.save_events([event1, event2])

    assert inserted == 2


def test_saved_event_can_be_retrieved(tmp_path, monkeypatch):
    setup_test_database(tmp_path, monkeypatch)

    database_module.init_db()

    event = create_sample_event()
    database_module.save_events([event])

    connection = database_module.get_connection()

    record = connection.execute("""
        SELECT event_type, username, source_ip
        FROM events
    """).fetchone()

    connection.close()

    assert record == (
        "login_failed",
        "admin",
        "192.168.1.20"
    )
