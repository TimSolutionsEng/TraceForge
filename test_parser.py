
from collector.log_collector import collect_logs
from parser.log_parser import parse_log

logs = collect_logs("logs/sample_auth.log")

print("Testing parser...\n")

for log in logs:
    event = parse_log(log)

    if event:
        print(event)
        print()
    else:
        print("Could not parse:", log)

