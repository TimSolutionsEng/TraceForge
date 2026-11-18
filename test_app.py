
import database.database as database_module
from backend.app import process_logs


def test_process_logs_end_to_end(tmp_path, monkeypatch):
    # Use a temporary database so we don't affect the real one
    monkeypatch.setattr(database_module, "DATA_DIR", tmp_path)
    monkeypatch.setattr(
        database_module, "DB_PATH", tmp_path / "test.db"
    )

    # Create a sample log file with three failed attempts
    log_file = tmp_path / "sample_auth.log"

    log_file.write_text(
        "Nov 18 10:00:00 traceforge-lab sshd[1001]: "
        "Failed password for admin from 192.168.1.20 port 52216 ssh2\n"
        "Nov 18 10:01:00 traceforge-lab sshd[1002]: "
        "Failed password for root from 192.168.1.20 port 52218 ssh2\n"
        "Nov 18 10:02:00 traceforge-lab sshd[1003]: "
        "Failed password for test from 192.168.1.20 port 52220 ssh2\n"
    )

    # Run the pipeline
    results = process_logs(log_file)

    # Check the processing results
    assert results["total_logs"] == 3
    assert results["parsed_events"] == 3
    assert results["inserted_events"] == 3

    # Three failed attempts should trigger one alert
    assert len(results["alerts"]) == 1
    assert results["alerts"][0]["source_ip"] == "192.168.1.20"
    assert results["alerts"][0]["failed_attempts"] == 3

    # Run the same logs again to test duplicate protection
    second_run = process_logs(log_file)

    assert second_run["inserted_events"] == 0
    assert len(second_run["alerts"]) == 1
