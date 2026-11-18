
from pathlib import Path

from collector.log_collector import collect_logs
from parser.log_parser import parse_log
from detection.detection_engine import detect_failed_logins
from database.database import init_db, save_events


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_LOG_FILE = PROJECT_ROOT / "logs" / "sample_auth.log"


def process_logs(log_file):
    # Step 1: Collect raw logs
    raw_logs = collect_logs(log_file)

    # Step 2: Parse raw logs into structured events
    events = []

    for log in raw_logs:
        event = parse_log(log)

        if event:
            events.append(event)

    # Step 3: Detect suspicious activity
    alerts = detect_failed_logins(events)

    # Step 4: Initialize the database and save events
    init_db()
    inserted_events = save_events(events)

    # Step 5: Return processing results
    results = {
        "total_logs": len(raw_logs),
        "parsed_events": len(events),
        "inserted_events": inserted_events,
        "alerts": alerts
    }

    return results


def main():
    results = process_logs(DEFAULT_LOG_FILE)

    print("\n========== TRACEFORGE REPORT ==========")
    print(f"Raw logs collected: {results['total_logs']}")
    print(f"Events parsed: {results['parsed_events']}")
    print(f"Events saved: {results['inserted_events']}")
    print(f"Alerts detected: {len(results['alerts'])}")

    if results["alerts"]:
        print("\nSUSPICIOUS ACTIVITY:")

        for alert in results["alerts"]:
            print(f"\nAlert: {alert['alert_type']}")
            print(f"Source IP: {alert['source_ip']}")
            print(f"Failed attempts: {alert['failed_attempts']}")
            print(f"Severity: {alert['severity']}")
            print(f"Description: {alert['description']}")
    else:
        print("\nNo suspicious activity detected.")

    print("=======================================\n")


if __name__ == "__main__":
    main()
