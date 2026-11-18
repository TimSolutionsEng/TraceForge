
from collections import defaultdict


def detect_failed_logins(events, threshold=3):
    """
    Detect IP addresses with repeated failed login attempts.

    Args:
        events: A list of parsed authentication events.
        threshold: Minimum failed attempts required to trigger an alert.

    Returns:
        A list of detection alerts.
    """

    failed_attempts = defaultdict(list)

    for event in events:

        if event.get("event_type") == "login_failed":
            source_ip = event.get("source_ip")

            if source_ip:
                failed_attempts[source_ip].append(event)

    alerts = []

    for source_ip, attempts in failed_attempts.items():

        if len(attempts) >= threshold:

            alert = {
                "alert_type": "brute_force_attempt",
                "source_ip": source_ip,
                "failed_attempts": len(attempts),
                "severity": "high",
                "description": (
                    f"Detected {len(attempts)} failed login attempts "
                    f"from IP address {source_ip}"
                )
            }

            alerts.append(alert)

    return alerts
