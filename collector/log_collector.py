
from pathlib import Path


def collect_logs(log_file):
    log_path = Path(log_file)

    if not log_path.exists():
        print(f"Log file not found: {log_path}")
        return []

    with open(log_path, "r", encoding="utf-8") as file:
        logs = file.readlines()

    return [log.strip() for log in logs if log.strip()]
