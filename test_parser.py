
from parser.log_parser import parse_log


def test_parse_failed_login():
    log = (
        "Nov 17 13:20:00 traceforge-lab sshd[1016]: "
        "Failed password for admin from 192.168.1.20 port 52216 ssh2"
    )

    event = parse_log(log)

    assert event is not None
    assert event["event_type"] == "login_failed"
    assert event["username"] == "admin"
    assert event["source_ip"] == "192.168.1.20"
    assert event["port"] == 52216


def test_parse_successful_login():
    log = (
        "Nov 17 13:22:05 traceforge-lab sshd[1020]: "
        "Accepted password for timothy from 192.168.1.15 port 52220 ssh2"
    )

    event = parse_log(log)

    assert event is not None
    assert event["event_type"] == "login_success"
    assert event["username"] == "timothy"
    assert event["source_ip"] == "192.168.1.15"


def test_parse_invalid_user():
    log = (
        "Nov 17 13:20:00 traceforge-lab sshd[1016]: "
        "Failed password for invalid user hacker from 192.168.1.20 port 52216 ssh2"
    )

    event = parse_log(log)

    assert event is not None
    assert event["event_type"] == "login_failed"
    assert event["username"] == "hacker"


def test_parse_ignores_unrecognized_message():
    log = (
        "Nov 17 13:20:00 traceforge-lab sshd[1016]: "
        "Connection closed by 192.168.1.20 port 52216"
    )

    event = parse_log(log)

    assert event is None


def test_parse_invalid_log_format():
    log = "This is not a valid SSH authentication log"

    event = parse_log(log)

    assert event is None


def test_parsed_event_contains_expected_fields():
    log = (
        "Nov 17 13:20:00 traceforge-lab sshd[1016]: "
        "Failed password for admin from 192.168.1.20 port 52216 ssh2"
    )

    event = parse_log(log)

    expected_fields = {
        "timestamp", "hostname", "process", "pid",
        "raw", "event_type", "username", "source_ip", "port"
    }

    assert expected_fields.issubset(event.keys())
