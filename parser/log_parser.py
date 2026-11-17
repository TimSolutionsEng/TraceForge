
import re


def parse_log(log):

    pattern = (
        r"^(?P<timestamp>\w+\s+\d+\s+\d+:\d+:\d+)\s+"
        r"(?P<hostname>\S+)\s+"
        r"(?P<process>\w+)\[(?P<pid>\d+)\]:\s+"
        r"(?P<message>.*)$"
    )

    match = re.match(pattern, log)

    if not match:
        return None

    event = match.groupdict()

    event["pid"] = int(event["pid"])
    event["raw"] = log

    message = event["message"]

    failed_login = re.search(
        r"Failed password for (?:invalid user )?(?P<username>\S+) "
        r"from (?P<source_ip>\S+) port (?P<port>\d+)",
        message
    )

    successful_login = re.search(
        r"Accepted password for (?P<username>\S+) "
        r"from (?P<source_ip>\S+) port (?P<port>\d+)",
        message
    )

    if failed_login:
        details = failed_login.groupdict()
        event["event_type"] = "login_failed"

    elif successful_login:
        details = successful_login.groupdict()
        event["event_type"] = "login_success"

    else:
        return None

    event.update(details)
    event["port"] = int(event["port"])

    event.pop("message")

    return event
