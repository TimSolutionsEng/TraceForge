
from detection.detection_engine import detect_failed_logins
from parser.log_parser import parse_log


def create_event(event_type, source_ip):
    """Create a sample authentication event for testing."""
    return {
        "event_type": event_type,
        "source_ip": source_ip
    }


def test_one_failed_login():
    events = [
        create_event("login_failed", "192.168.1.10")
    ]

    alerts = detect_failed_logins(events)

    assert len(alerts) == 0


def test_two_failed_logins():
    events = [
        create_event("login_failed", "192.168.1.10"),
        create_event("login_failed", "192.168.1.10")
    ]

    alerts = detect_failed_logins(events)

    assert len(alerts) == 0


def test_three_failed_logins():
    events = [
        create_event("login_failed", "192.168.1.10"),
        create_event("login_failed", "192.168.1.10"),
        create_event("login_failed", "192.168.1.10")
    ]

    alerts = detect_failed_logins(events)

    assert len(alerts) == 1
    assert alerts[0]["source_ip"] == "192.168.1.10"
    assert alerts[0]["failed_attempts"] == 3
    assert alerts[0]["severity"] == "high"


def test_five_failed_logins():
    events = [
        create_event("login_failed", "192.168.1.10")
        for _ in range(5)
    ]

    alerts = detect_failed_logins(events)

    assert len(alerts) == 1
    assert alerts[0]["failed_attempts"] == 5


def test_different_ips_are_counted_separately():
    events = [
        create_event("login_failed", "192.168.1.10"),
        create_event("login_failed", "192.168.1.10"),
        create_event("login_failed", "192.168.1.20"),
        create_event("login_failed", "192.168.1.20"),
    ]

    alerts = detect_failed_logins(events)

    assert len(alerts) == 0


def test_successful_logins_are_ignored():
    events = [
        create_event("successful_login", "192.168.1.10"),
        create_event("successful_login", "192.168.1.10"),
        create_event("successful_login", "192.168.1.10"),
    ]

    alerts = detect_failed_logins(events)

    assert len(alerts) == 0


def test_custom_threshold():
    events = [
        create_event("login_failed", "192.168.1.10"),
        create_event("login_failed", "192.168.1.10"),
    ]

    alerts = detect_failed_logins(events, threshold=2)

    assert len(alerts) == 1
    assert alerts[0]["failed_attempts"] == 2
def test_detection_with_parsed_events():

    raw_logs = [
        "Nov 18 10:15:01 ubuntu sshd[1234]: Failed password for admin from 192.168.1.10 port 54321 ssh2",
        "Nov 18 10:15:05 ubuntu sshd[1235]: Failed password for root from 192.168.1.10 port 54322 ssh2",
        "Nov 18 10:15:09 ubuntu sshd[1236]: Failed password for user from 192.168.1.10 port 54323 ssh2"
    ]

    events = []

    for log in raw_logs:
        event = parse_log(log)

        if event:
            events.append(event)

    alerts = detect_failed_logins(events)

    assert len(events) == 3
    assert len(alerts) == 1
    assert alerts[0]["source_ip"] == "192.168.1.10"
    assert alerts[0]["failed_attempts"] == 3